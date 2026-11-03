import unittest
from demo import Workflow

class WorkflowTests(unittest.TestCase):
    def test_openai(self):
        self.assertEqual(Workflow().run('openai', 'hello')['provider'], 'openai')
    def test_anthropic(self):
        self.assertEqual(Workflow().run('anthropic', 'hello')['provider'], 'anthropic')
    def test_retry(self):
        self.assertEqual(Workflow().run('openai', 'hello', True)['attempts'], 2)
    def test_invalid_provider(self):
        with self.assertRaises(ValueError): Workflow().run('unknown', 'hello')
    def test_empty_prompt(self):
        with self.assertRaises(ValueError): Workflow().run('openai', '')
