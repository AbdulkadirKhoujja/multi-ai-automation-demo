# Multi-AI Automation Demo

Original synthetic portfolio demonstration of provider routing, controlled retries, structured responses, and audit events. **No live OpenAI or Anthropic API calls occur**; provider adapters are deterministic mocks. No credentials or client data required.

Run `python -m unittest discover -s . -v` and `python demo.py`.

Production work would require official SDK integrations, server-side secret storage, per-provider rate limits, observability, and consented data handling.
