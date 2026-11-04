"""Real HTTPS adapters for OpenAI and Anthropic; offline tests mock transport."""
import json
import os
import urllib.request
import urllib.error

class ProviderError(RuntimeError): pass

def post_json(url, headers, payload, timeout=20):
    request=urllib.request.Request(url,data=json.dumps(payload).encode(),headers={"Content-Type":"application/json",**headers},method="POST")
    try:
        with urllib.request.urlopen(request,timeout=timeout) as response:
            return json.load(response)
    except (urllib.error.HTTPError,urllib.error.URLError,TimeoutError) as exc:
        raise ProviderError(str(exc)) from exc

def ask(provider,prompt,transport=post_json):
    if not isinstance(prompt,str) or not prompt.strip(): raise ValueError("Nonempty prompt required")
    if provider=="openai":
        key=os.getenv("OPENAI_API_KEY")
        if not key: raise ProviderError("OPENAI_API_KEY missing")
        result=transport("https://api.openai.com/v1/responses",{"Authorization":f"Bearer {key}"},{"model":os.getenv("OPENAI_MODEL","gpt-4.1-mini"),"input":prompt})
        text="".join(c.get("text","") for item in result.get("output",[]) for c in item.get("content",[]) if c.get("type")=="output_text")
        return {"provider":provider,"text":text}
    if provider=="anthropic":
        key=os.getenv("ANTHROPIC_API_KEY")
        if not key: raise ProviderError("ANTHROPIC_API_KEY missing")
        result=transport("https://api.anthropic.com/v1/messages",{"x-api-key":key,"anthropic-version":"2023-06-01"},{"model":os.getenv("ANTHROPIC_MODEL","claude-sonnet-4-5"),"max_tokens":256,"messages":[{"role":"user","content":prompt}]})
        text="".join(c.get("text","") for c in result.get("content",[]) if c.get("type")=="text")
        return {"provider":provider,"text":text}
    raise ValueError("Unsupported provider")
