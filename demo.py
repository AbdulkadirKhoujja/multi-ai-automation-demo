"""Synthetic OpenAI/Anthropic workflow simulation, with no external calls."""
from dataclasses import dataclass, field

class TransientError(Exception):
    pass

@dataclass
class Workflow:
    audit: list = field(default_factory=list)

    def run(self, provider, prompt, fail_first=False):
        if provider not in ('openai', 'anthropic'):
            raise ValueError('Unsupported provider')
        if not isinstance(prompt, str) or not prompt.strip():
            raise ValueError('Prompt must be nonempty')
        for attempt in range(1, 3):
            try:
                if fail_first and attempt == 1:
                    raise TransientError('simulated timeout')
                result = {'provider': provider, 'text': 'Synthetic response', 'attempts': attempt}
                self.audit.append({'provider': provider, 'attempt': attempt, 'status': 'success'})
                return result
            except TransientError:
                self.audit.append({'provider': provider, 'attempt': attempt, 'status': 'retry'})
        raise RuntimeError('Retries exhausted')

if __name__ == '__main__':
    w = Workflow()
    print(w.run('openai', 'Summarize synthetic issue 18', fail_first=True))
    print(w.run('anthropic', 'Review synthetic test result'))
    print('audit', w.audit)
