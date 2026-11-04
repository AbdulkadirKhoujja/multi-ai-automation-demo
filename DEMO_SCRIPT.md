# Demonstration recording script (approximately 75 seconds)

**Disclosure:** Test responses are mocked; live API requests require the operator's own credentials and have not been verified.

1. Show `providers.py`: OpenAI Responses and Anthropic Messages HTTPS endpoints, environment-based keys, no hard-coded secrets.
2. Show `workflow.py`: primary provider, bounded retries, fallback provider, audit events.
3. Run `python -m unittest discover -s . -p 'test_*.py' -v` and show actual results.
4. Highlight the fallback test: simulated primary provider failure followed by success from the second provider.
5. Show the README's optional live-call command without exposing credentials or pretending a live call occurred.
6. Close with production limitations and recommended next steps.

Suggested narration: “This demo separates model-provider integrations from workflow control. The adapters target the real OpenAI and Anthropic APIs, while deterministic tests mock network calls. The orchestrator retries transient provider errors and can fall back to another provider, recording attempts without logging the prompt. This is a portfolio demonstration, not an existing customer deployment.”
