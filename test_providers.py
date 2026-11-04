import os
import unittest
from unittest.mock import patch
from providers import ask,ProviderError
from workflow import Workflow
class ProviderTests(unittest.TestCase):
 def test_openai_payload(self):
  def transport(url,headers,payload):
   self.assertEqual(url,"https://api.openai.com/v1/responses")
   self.assertEqual(payload["input"],"hello")
   return {"output":[{"content":[{"type":"output_text","text":"answer"}]}]}
  with patch.dict(os.environ,{"OPENAI_API_KEY":"test-token"}):
   self.assertEqual(ask("openai","hello",transport)["text"],"answer")
 def test_anthropic_payload(self):
  def transport(url,headers,payload):
   self.assertEqual(url,"https://api.anthropic.com/v1/messages")
   return {"content":[{"type":"text","text":"reply"}]}
  with patch.dict(os.environ,{"ANTHROPIC_API_KEY":"test-token"}):
   self.assertEqual(ask("anthropic","hello",transport)["text"],"reply")
 def test_missing_key(self):
  with patch.dict(os.environ,{},clear=True):
   with self.assertRaises(ProviderError): ask("openai","hello")
 def test_fallback(self):
  def call(provider,prompt):
   if provider=="openai": raise ProviderError("temporary failure")
   return {"provider":provider,"text":"recovered"}
  w=Workflow(call=call,sleeper=lambda _:None)
  self.assertEqual(w.run("hello",fallback="anthropic",retries=1)["provider"],"anthropic")
  self.assertEqual(len(w.audit),3)
 def test_no_prompt_logged(self):
  w=Workflow(call=lambda provider,prompt:{"provider":provider,"text":"ok"})
  w.run("sensitive text")
  self.assertNotIn("sensitive text",str(w.audit))
