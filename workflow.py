"""Provider-independent workflow with retry, optional fallback, and redacted audit."""
import time
from providers import ask, ProviderError

class Workflow:
 def __init__(self, call=ask, sleeper=time.sleep):
  self.call=call
  self.sleeper=sleeper
  self.audit=[]
 def run(self,prompt,primary="openai",fallback=None,retries=1):
  if retries<0 or retries>3: raise ValueError("retries must be 0..3")
  providers=[primary]+([fallback] if fallback and fallback!=primary else [])
  for provider in providers:
   for attempt in range(retries+1):
    try:
     response=self.call(provider,prompt)
     self.audit.append({"provider":provider,"attempt":attempt+1,"status":"success"})
     return response
    except ProviderError:
     self.audit.append({"provider":provider,"attempt":attempt+1,"status":"error"})
     if attempt<retries: self.sleeper(min(2**attempt,4))
  raise ProviderError("All configured providers failed")
