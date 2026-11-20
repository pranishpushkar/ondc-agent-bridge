#!/usr/bin/env python3
"""
ondc_probe.py - explore the real API contracts of ONDC sellers (BPPs).

Sends signed Beckn/ONDC requests as a buyer app (BAP), collects the
asynchronous on_* callbacks that real sellers send back, saves every raw
payload, and produces a report of what fields sellers actually send.

The saved captures double as replay fixtures for unit tests / CI.

Commands
  keygen     generate signing (Ed25519) and encryption (X25519) key pairs
  selftest   check signing + verification locally (no network)
  lookup     list subscribers (e.g. BPPs) from the registry
  serve      run only the callback receiver
  search     send /search via the gateway, collect on_search for N seconds
  select     send /select for one item from a captured on_search, collect on_select
  analyze    build a contract report (markdown) from the captures

Requirements: Python 3.10+, `pip install cryptography`.

Before `search` / `select` work you need, on ONDC staging:
  * a subscribed BAP (subscriber_id, unique_key_id, keys registered), and
  * a public HTTPS URL that forwards to this script's callback port and
    matches the subscriber_url you registered (e.g. via cloudflared/ngrok).

Not covered on purpose: /init and /confirm (they move toward a real order).
Endpoints, codes and message shapes follow the ONDC retail 1.2.x contract as
best known; verify them against the current ONDC docs before relying on them.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import re
import sys
import threading
import time
import urllib.error
import urllib.request
import uuid
from collections import defaultdict
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
    Ed25519PublicKey,
)
from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey

# ---------------------------------------------------------------- config ---

DEFAULTS = {
    # Staging defaults as best known; override with env vars or flags.
    "ONDC_REGISTRY_URL": "https://staging.registry.ondc.org",
    "ONDC_GATEWAY_URL": "https://staging.gateway.proteantech.in",
    "ONDC_DOMAIN": "ONDC:RET10",  # RET10 = grocery
    "ONDC_CITY": "std:080",  # Bengaluru
    "ONDC_CORE_VERSION": "1.2.0",
    "ONDC_CAPTURES": "captures",
    "ONDC_PORT": "8090",
}


def cfg(name: str, override: str | None = None) -> str:
    if override:
        return override
    return os.environ.get(name) or DEFAULTS.get(name, "")


def require(name: str, override: str | None = None) -> str:
    value = cfg(name, override)
    if not value:
        sys.exit(f"error: {name} is not set (env var or flag)")
    return value


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")


def safe(text: str) -> str:
    return re.sub(r"[^A-Za-z0-9._-]+", "_", text)[:80] or "unknown"


# --------------------------------------------------------------- signing ---
# ONDC signing: digest = base64(BLAKE2b-512(body)); sign
#   "(created): <c>\n(expires): <e>\ndigest: BLAKE-512=<digest>"
# with Ed25519, and send it in the Authorization header.


def load_private_key(b64: str) -> Ed25519PrivateKey:
    raw = base64.b64decode(b64)
    if len(raw) == 64:  # libsodium format: seed (32) + public key (32)
        raw = raw[:32]
    if len(raw) != 32:
        sys.exit("error: signing private key must be base64 of 32 or 64 bytes")
    return Ed25519PrivateKey.from_private_bytes(raw)


def body_digest(body: bytes) -> str:
    return base64.b64encode(hashlib.blake2b(body, digest_size=64).digest()).decode()


def signing_string(created: int, expires: int, digest: str) -> str:
    return f"(created): {created}\n(expires): {expires}\ndigest: BLAKE-512={digest}"


def auth_header(body: bytes, key: Ed25519PrivateKey, subscriber_id: str, unique_key_id: str,
                ttl_seconds: int = 3600) -> str:
    created = int(time.time())
    expires = created + ttl_seconds
    signature = base64.b64encode(
        key.sign(signing_string(created, expires, body_digest(body)).encode())
    ).decode()
    return (
        f'Signature keyId="{subscriber_id}|{unique_key_id}|ed25519",algorithm="ed25519",'
        f'created="{created}",expires="{expires}",headers="(created) (expires) digest",'
        f'signature="{signature}"'
    )


def parse_auth_header(header: str) -> dict[str, str]:
    return dict(re.findall(r'(\w+)="([^"]*)"', header or ""))


def verify_auth(header: str, body: bytes, public_key_b64: str) -> tuple[bool, str]:
    parts = parse_auth_header(header)
    try:
        created, expires = int(parts["created"]), int(parts["expires"])
        signature = base64.b64decode(parts["signature"])
    except (KeyError, ValueError):
        return False, "malformed Authorization header"
    if time.time() > expires:
        return False, "signature expired"
    try:
        Ed25519PublicKey.from_public_bytes(base64.b64decode(public_key_b64)).verify(
            signature, signing_string(created, expires, body_digest(body)).encode()
        )
    except (InvalidSignature, ValueError):
        return False, "bad signature"
    return True, "ok"


# ------------------------------------------------------------------ http ---


def http_post(url: str, body: bytes, headers: dict[str, str], timeout: float = 15.0) -> tuple[int, Any]:
    req = urllib.request.Request(url, data=body, method="POST",
                                 headers={"Content-Type": "application/json", **headers})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read()
            status = resp.status
    except urllib.error.HTTPError as err:
        raw, status = err.read(), err.code
    except urllib.error.URLError as err:
        return 0, {"error": str(err.reason)}
    try:
        return status, json.loads(raw or b"null")
    except json.JSONDecodeError:
        return status, {"raw": raw.decode(errors="replace")}


def dump(obj: Any) -> bytes:
    """Serialize once; the exact bytes are both signed and sent."""
    return json.dumps(obj, separators=(",", ":"), ensure_ascii=False).encode()


# -------------------------------------------------------------- registry ---


class Registry:
    def __init__(self, url: str):
        self.url = url.rstrip("/")
        self._keys: dict[str, str | None] = {}
        self._lock = threading.Lock()

    def lookup(self, query: dict[str, Any]) -> list[dict[str, Any]]:
        status, data = http_post(f"{self.url}/lookup", dump(query), {})
        if status != 200 or not isinstance(data, list):
            raise RuntimeError(f"registry lookup failed: HTTP {status}: {str(data)[:300]}")
        return data

    def signing_key(self, subscriber_id: str, unique_key_id: str) -> str | None:
        cache_key = f"{subscriber_id}|{unique_key_id}"
        with self._lock:
            if cache_key in self._keys:
                return self._keys[cache_key]
        key = None
        try:
            for entry in self.lookup({"subscriber_id": subscriber_id}):
                if not unique_key_id or entry.get("ukId") == unique_key_id:
                    key = entry.get("signing_public_key")
                    break
        except RuntimeError:
            key = None
        with self._lock:
            self._keys[cache_key] = key
        return key


# ------------------------------------------------------ callback receiver ---


class Collector:
    """Receives on_* callbacks and writes each one, raw, to the captures folder."""

    def __init__(self, captures: Path, registry: Registry | None):
        self.captures = captures
        self.registry = registry
        self.lock = threading.Lock()
        self.received: list[dict[str, Any]] = []

    def store(self, path: str, headers: dict[str, str], body: bytes) -> None:
        received_at = now_iso()
        try:
            payload = json.loads(body)
        except json.JSONDecodeError:
            payload = {"_unparseable": body.decode(errors="replace")}
        ctx = payload.get("context") or {} if isinstance(payload, dict) else {}
        action = ctx.get("action") or path.strip("/").replace("/", "_") or "unknown"
        txn = ctx.get("transaction_id") or "no-transaction"
        bpp = ctx.get("bpp_id") or "unknown-bpp"

        verification = "not checked"
        auth = headers.get("authorization", "")
        if self.registry and auth:
            sub, _, rest = parse_auth_header(auth).get("keyId", "").partition("|")
            ukid = rest.split("|")[0] if rest else ""
            key = self.registry.signing_key(sub, ukid)
            verification = verify_auth(auth, body, key)[1] if key else "key not found in registry"
        elif not auth:
            verification = "no Authorization header"

        record = {
            "_meta": {
                "received_at": received_at,
                "path": path,
                "action": action,
                "bpp_id": bpp,
                "signature": verification,
                "headers": {k: v for k, v in headers.items()
                            if k in ("authorization", "x-gateway-authorization", "content-type")},
            },
            "payload": payload,
        }
        folder = self.captures / safe(txn)
        with self.lock:
            folder.mkdir(parents=True, exist_ok=True)
            n = len(list(folder.glob(f"{safe(action)}--*.json"))) + 1
            (folder / f"{safe(action)}--{safe(bpp)}--{n:03d}.json").write_text(
                json.dumps(record, indent=2, ensure_ascii=False))
            self.received.append(record["_meta"])
        print(f"  <- {action:<11} from {bpp}  [signature: {verification}]")


def start_server(collector: Collector, port: int) -> ThreadingHTTPServer:
    class Handler(BaseHTTPRequestHandler):
        def do_POST(self) -> None:  # noqa: N802
            body = self.rfile.read(int(self.headers.get("Content-Length") or 0))
            headers = {k.lower(): v for k, v in self.headers.items()}
            collector.store(self.path, headers, body)
            reply = dump({"message": {"ack": {"status": "ACK"}}})
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(reply)))
            self.end_headers()
            self.wfile.write(reply)

        def do_GET(self) -> None:  # noqa: N802  (health check for the tunnel)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"ondc_probe callback receiver")

        def log_message(self, *args: Any) -> None:
            pass

    server = ThreadingHTTPServer(("0.0.0.0", port), Handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server


# ------------------------------------------------------------- messages ---


def context(args: argparse.Namespace, action: str, transaction_id: str | None = None,
            bpp_id: str | None = None, bpp_uri: str | None = None) -> dict[str, Any]:
    ctx = {
        "domain": cfg("ONDC_DOMAIN", args.domain),
        "action": action,
        "country": "IND",
        "city": cfg("ONDC_CITY", args.city),
        "core_version": cfg("ONDC_CORE_VERSION"),
        "bap_id": require("ONDC_SUBSCRIBER_ID", args.subscriber_id),
        "bap_uri": require("ONDC_BAP_URI", args.bap_uri),
        "transaction_id": transaction_id or str(uuid.uuid4()),
        "message_id": str(uuid.uuid4()),
        "timestamp": now_iso(),
        "ttl": "PT30S",
    }
    if bpp_id:
        ctx["bpp_id"] = bpp_id
        ctx["bpp_uri"] = bpp_uri
    return ctx


def search_message(args: argparse.Namespace) -> dict[str, Any]:
    intent: dict[str, Any] = {
        "fulfillment": {"type": "Delivery"},
        "payment": {
            "@ondc/org/buyer_app_finder_fee_type": "percent",
            "@ondc/org/buyer_app_finder_fee_amount": str(args.finder_fee),
        },
    }
    if args.query:
        intent["item"] = {"descriptor": {"name": args.query}}
    if args.category:
        intent["category"] = {"id": args.category}
    if args.gps:
        intent["fulfillment"]["end"] = {"location": {"gps": args.gps,
                                                     "address": {"area_code": args.area_code}}}
    return {"intent": intent}


# ------------------------------------------------------------- commands ---


def send_signed(args: argparse.Namespace, url: str, request: dict[str, Any]) -> None:
    body = dump(request)
    header = auth_header(body, load_private_key(require("ONDC_SIGNING_PRIVATE_KEY", args.private_key)),
                         require("ONDC_SUBSCRIBER_ID", args.subscriber_id),
                         require("ONDC_UNIQUE_KEY_ID", args.unique_key_id))
    ctx = request["context"]
    folder = Path(cfg("ONDC_CAPTURES", args.captures)) / safe(ctx["transaction_id"])
    folder.mkdir(parents=True, exist_ok=True)
    sent_at = now_iso()
    print(f"  -> {ctx['action']:<11} to {url}")
    status, ack = http_post(url, body, {"Authorization": header})
    print(f"     sync response: HTTP {status} {json.dumps(ack)[:200]}")
    (folder / f"{ctx['action']}--request.json").write_text(json.dumps(
        {"_meta": {"sent_at": sent_at, "url": url, "http_status": status, "sync_response": ack},
         "payload": request}, indent=2, ensure_ascii=False))


def collect(args: argparse.Namespace, url: str, request: dict[str, Any]) -> None:
    captures = Path(cfg("ONDC_CAPTURES", args.captures))
    registry = None if args.no_verify else Registry(cfg("ONDC_REGISTRY_URL", args.registry))
    collector = Collector(captures, registry)
    server = start_server(collector, int(cfg("ONDC_PORT", args.port)))
    try:
        send_signed(args, url, request)
        print(f"  waiting {args.wait}s for callbacks...")
        time.sleep(args.wait)
    finally:
        server.shutdown()
    bpps = {m["bpp_id"] for m in collector.received}
    print(f"\n{len(collector.received)} callbacks from {len(bpps)} seller apps. "
          f"Saved under {captures / safe(request['context']['transaction_id'])}")
    if not collector.received:
        print("No callbacks: check that ONDC_BAP_URI is public, forwards to this port, "
              "and matches your registered subscriber_url.")


def cmd_search(args: argparse.Namespace) -> None:
    request = {"context": context(args, "search"), "message": search_message(args)}
    collect(args, cfg("ONDC_GATEWAY_URL", args.gateway).rstrip("/") + "/search", request)


def cmd_select(args: argparse.Namespace) -> None:
    record = json.loads(Path(args.capture).read_text())
    payload = record.get("payload", record)
    ctx = payload["context"]
    provider = item = None
    for p in (payload.get("message") or {}).get("catalog", {}).get("bpp/providers", []):
        if p.get("id") == args.provider:
            provider = p
            item = next((i for i in p.get("items", []) if i.get("id") == args.item), None)
    if not provider or not item:
        sys.exit("error: provider/item not found in that capture")
    location_id = item.get("location_id") or (provider.get("locations") or [{}])[0].get("id")
    order = {
        "provider": {"id": provider["id"], "locations": [{"id": location_id}]},
        "items": [{"id": item["id"], "location_id": location_id,
                   "quantity": {"count": args.quantity}}],
        "fulfillments": [{"end": {"location": {"gps": args.gps,
                                               "address": {"area_code": args.area_code}}}}],
    }
    request = {
        "context": context(args, "select", ctx["transaction_id"], ctx["bpp_id"], ctx["bpp_uri"]),
        "message": {"order": order},
    }
    collect(args, ctx["bpp_uri"].rstrip("/") + "/select", request)


def cmd_serve(args: argparse.Namespace) -> None:
    registry = None if args.no_verify else Registry(cfg("ONDC_REGISTRY_URL", args.registry))
    port = int(cfg("ONDC_PORT", args.port))
    start_server(Collector(Path(cfg("ONDC_CAPTURES", args.captures)), registry), port)
    print(f"Receiving callbacks on :{port} (Ctrl-C to stop)")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass


def cmd_lookup(args: argparse.Namespace) -> None:
    query = {"country": "IND", "type": args.type, "domain": cfg("ONDC_DOMAIN", args.domain),
             "city": cfg("ONDC_CITY", args.city)}
    entries = Registry(cfg("ONDC_REGISTRY_URL", args.registry)).lookup(query)
    out = Path(cfg("ONDC_CAPTURES", args.captures))
    out.mkdir(parents=True, exist_ok=True)
    path = out / f"lookup--{args.type}--{safe(query['domain'])}--{safe(query['city'])}.json"
    path.write_text(json.dumps(entries, indent=2))
    for e in entries:
        print(f"{e.get('subscriber_id', '?'):<45} {e.get('status', '?'):<12} {e.get('subscriber_url', '')}")
    print(f"\n{len(entries)} entries, saved to {path}")


def cmd_keygen(_: argparse.Namespace) -> None:
    sign = Ed25519PrivateKey.generate()
    seed = sign.private_bytes(serialization.Encoding.Raw, serialization.PrivateFormat.Raw,
                              serialization.NoEncryption())
    sign_pub = sign.public_key().public_bytes(serialization.Encoding.Raw, serialization.PublicFormat.Raw)
    enc = X25519PrivateKey.generate()
    enc_priv = enc.private_bytes(serialization.Encoding.DER, serialization.PrivateFormat.PKCS8,
                                 serialization.NoEncryption())
    enc_pub = enc.public_key().public_bytes(serialization.Encoding.DER,
                                            serialization.PublicFormat.SubjectPublicKeyInfo)
    b64 = lambda b: base64.b64encode(b).decode()  # noqa: E731
    print("# Keep the private keys secret. Register the public keys when subscribing.")
    print(f"ONDC_SIGNING_PRIVATE_KEY={b64(seed + sign_pub)}")
    print(f"signing_public_key={b64(sign_pub)}")
    print(f"encryption_private_key={b64(enc_priv)}")
    print(f"encryption_public_key={b64(enc_pub)}")


def cmd_selftest(_: argparse.Namespace) -> None:
    key = Ed25519PrivateKey.generate()
    pub = base64.b64encode(key.public_key().public_bytes(
        serialization.Encoding.Raw, serialization.PublicFormat.Raw)).decode()
    body = dump({"context": {"action": "search"}, "message": {}})
    header = auth_header(body, key, "bap.example.com", "key-1")
    checks = [
        ("valid signature verifies", verify_auth(header, body, pub)[0] is True),
        ("tampered body fails", verify_auth(header, body + b" ", pub)[0] is False),
        ("keyId is parsed", parse_auth_header(header)["keyId"] == "bap.example.com|key-1|ed25519"),
        ("64-byte libsodium key loads", load_private_key(base64.b64encode(
            key.private_bytes(serialization.Encoding.Raw, serialization.PrivateFormat.Raw,
                              serialization.NoEncryption()) + b"\0" * 32).decode()) is not None),
    ]
    for name, ok in checks:
        print(f"{'PASS' if ok else 'FAIL'}  {name}")
    sys.exit(0 if all(ok for _, ok in checks) else 1)


# -------------------------------------------------------------- analyze ---


def walk(node: Any, path: str, out: dict[str, list[Any]]) -> None:
    if isinstance(node, dict):
        out.setdefault(path or "$", []).append(node)
        for key, value in node.items():
            walk(value, f"{path}.{key}" if path else key, out)
    elif isinstance(node, list):
        out.setdefault(path, []).append(node)
        for value in node:
            walk(value, f"{path}[]", out)
    else:
        out.setdefault(path, []).append(node)


def type_name(value: Any) -> str:
    return {dict: "object", list: "array", str: "string", bool: "boolean",
            int: "number", float: "number", type(None): "null"}[type(value)]


def tag_codes(payload: Any, out: dict[str, set[str]]) -> None:
    """Collect ONDC tag codes: tags: [{code, list: [{code, value}]}]."""
    if isinstance(payload, dict):
        for key, value in payload.items():
            if key == "tags" and isinstance(value, list):
                for group in value:
                    if isinstance(group, dict):
                        gcode = group.get("code") or (group.get("descriptor") or {}).get("code") or "?"
                        for tag in group.get("list") or []:
                            if isinstance(tag, dict):
                                out[gcode].add(tag.get("code") or (tag.get("descriptor") or {}).get("code") or "?")
            tag_codes(value, out)
    elif isinstance(payload, list):
        for value in payload:
            tag_codes(value, out)


def cmd_analyze(args: argparse.Namespace) -> None:
    captures = Path(cfg("ONDC_CAPTURES", args.captures))
    by_action: dict[str, list[dict[str, Any]]] = defaultdict(list)
    sent: dict[tuple[str, str], str] = {}
    for file in sorted(captures.glob("*/*.json")):
        record = json.loads(file.read_text())
        meta = record.get("_meta", {})
        if file.name.endswith("--request.json"):
            sent[(file.parent.name, record["payload"]["context"]["action"])] = meta.get("sent_at", "")
            continue
        by_action[meta.get("action", "unknown")].append({**record, "_txn": file.parent.name})
    if not by_action:
        sys.exit(f"no callbacks found under {captures}")

    lines = [f"# ONDC contract report", "",
             f"Generated {now_iso()} from `{captures}`.", ""]
    for action, records in sorted(by_action.items()):
        bpps = sorted({r["_meta"].get("bpp_id", "?") for r in records})
        lines += [f"## {action}", "",
                  f"{len(records)} callbacks from {len(bpps)} seller apps: {', '.join(bpps)}", ""]

        # Latency and signature results per seller.
        lines += ["| Seller app | Latency after request | Signature |", "|---|---|---|"]
        request_action = action.removeprefix("on_")
        for r in records:
            meta = r["_meta"]
            latency = "?"
            start = sent.get((r["_txn"], request_action))
            if start and meta.get("received_at"):
                delta = (datetime.fromisoformat(meta["received_at"].replace("Z", "+00:00"))
                         - datetime.fromisoformat(start.replace("Z", "+00:00")))
                latency = f"{delta.total_seconds():.1f}s"
            lines.append(f"| {meta.get('bpp_id', '?')} | {latency} | {meta.get('signature', '?')} |")
        lines.append("")

        # Field coverage: in how many callbacks does each path appear, and with which types.
        per_record = []
        for r in records:
            paths: dict[str, list[Any]] = {}
            walk(r["payload"], "", paths)
            per_record.append(paths)
        all_paths = sorted({p for paths in per_record for p in paths})
        lines += ["| Field path | In callbacks | Types | Example |", "|---|---|---|---|"]
        for path in all_paths:
            present = [paths[path] for paths in per_record if path in paths]
            values = [v for vs in present for v in vs]
            types = sorted({type_name(v) for v in values})
            example = next((v for v in values if not isinstance(v, (dict, list))), None)
            example_text = "" if example is None else json.dumps(example, ensure_ascii=False)[:60]
            example_text = example_text.replace("|", "\\|")
            lines.append(f"| `{path}` | {len(present)}/{len(records)} | {', '.join(types)} | {example_text} |")
        lines.append("")

        tags: dict[str, set[str]] = defaultdict(set)
        for r in records:
            tag_codes(r["payload"], tags)
        if tags:
            lines += ["Tag groups seen:", ""]
            lines += [f"- `{g}`: {', '.join(sorted(codes))}" for g, codes in sorted(tags.items())]
            lines.append("")

    report = captures / "contract-report.md"
    report.write_text("\n".join(lines))
    print(f"Report written to {report}")


# ------------------------------------------------------------------ cli ---


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = parser.add_subparsers(dest="command", required=True)

    def common(p: argparse.ArgumentParser) -> None:
        p.add_argument("--captures", help="captures folder (default ./captures)")
        p.add_argument("--registry", help="registry base URL")
        p.add_argument("--domain", help="e.g. ONDC:RET10")
        p.add_argument("--city", help="e.g. std:080")

    def network(p: argparse.ArgumentParser) -> None:
        common(p)
        p.add_argument("--subscriber-id")
        p.add_argument("--unique-key-id")
        p.add_argument("--private-key", help="base64 Ed25519 signing key (prefer the env var)")
        p.add_argument("--bap-uri", help="your public callback URL")
        p.add_argument("--port", help="local callback port (default 8090)")
        p.add_argument("--wait", type=int, default=20, help="seconds to collect callbacks")
        p.add_argument("--no-verify", action="store_true", help="skip callback signature checks")
        p.add_argument("--gps", default="12.9716,77.5946")
        p.add_argument("--area-code", default="560001")

    p = sub.add_parser("search", help="send /search, collect on_search")
    network(p)
    p.add_argument("--gateway", help="gateway base URL")
    p.add_argument("--query", default="milk", help="item name to search for")
    p.add_argument("--category", help="category id instead of / as well as a query")
    p.add_argument("--finder-fee", default="3", help="buyer app finder fee, percent")
    p.set_defaults(func=cmd_search)

    p = sub.add_parser("select", help="send /select for an item from a captured on_search")
    network(p)
    p.add_argument("--capture", required=True, help="path to an on_search capture file")
    p.add_argument("--provider", required=True)
    p.add_argument("--item", required=True)
    p.add_argument("--quantity", type=int, default=1)
    p.set_defaults(func=cmd_select)

    p = sub.add_parser("serve", help="run only the callback receiver")
    common(p)
    p.add_argument("--port")
    p.add_argument("--no-verify", action="store_true")
    p.set_defaults(func=cmd_serve)

    p = sub.add_parser("lookup", help="list registry subscribers")
    common(p)
    p.add_argument("--type", default="BPP", choices=["BPP", "BAP", "BG"])
    p.set_defaults(func=cmd_lookup)

    p = sub.add_parser("analyze", help="write a contract report from captures")
    p.add_argument("--captures")
    p.set_defaults(func=cmd_analyze)

    sub.add_parser("keygen", help="generate key pairs").set_defaults(func=cmd_keygen)
    sub.add_parser("selftest", help="local signing check").set_defaults(func=cmd_selftest)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
