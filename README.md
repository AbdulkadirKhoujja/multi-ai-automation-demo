# Multi-AI Automation Demo

Original pre-contract portfolio demonstration. Contains **real HTTPS provider adapters** for OpenAI Responses API and Anthropic Messages API, a provider-independent workflow with bounded retries, optional fallback, and structured audit events that do not record prompt text.

No live API calls have been claimed or performed in this repository. CI tests mock HTTP and do not require credentials. The earlier `demo.py` is an explicitly synthetic offline illustration.

## Run tests
```bash
python -m unittest discover -s . -p 'test_*.py' -v
```

## Optional live call (requires your own credentials and incurs provider charges)
```bash
export OPENAI_API_KEY=...
export ANTHROPIC_API_KEY=...
python -c "from workflow import Workflow; print(Workflow().run('Say hello',fallback='anthropic'))"
```

Provider model IDs are configurable with `OPENAI_MODEL` and `ANTHROPIC_MODEL`. Never commit API keys. The fallback is only used on provider transport errors, not on arbitrary programming errors. For production use, add request correlation IDs, rate limiting, circuit breakers, persisted traces, consented data governance, and per-provider billing controls.
