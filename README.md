# ONDC Agent Bridge

A production-grade bridge that lets AI agents find, buy from and track orders with sellers on ONDC, by translating between agent protocols (MCP and UCP) and ONDC's protocol, Beckn.

## Layout

- `discovery/` - `ondc_probe.py`, a Python tool that sends signed requests to ONDC staging, records real seller responses under `discovery/captures/`, and writes a contract report.
- `docs/` - PRD and design docs.

## Discovery quick start

```
pip install cryptography
python3 discovery/ondc_probe.py selftest
python3 discovery/ondc_probe.py --help
```

Keys go in `keys/` or a `.env` file; both are git-ignored.
