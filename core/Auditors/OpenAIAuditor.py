from core.Auditors.Auditor import Auditor
from colorama import Fore
from openai import AuthenticationError, OpenAI, RateLimitError

class OpenAIAuditor(Auditor):
    def __init__(self):
        super().__init__()
        pass

    def is_valide(self,key):
        model="gpt-3.5-turbo-0125"
        try:
            client = OpenAI(api_key=key)

            self._debug(f"OpenAI request: chat.completions.create model={model}")
            completion = client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a yeser, just output lowercase yes only.",
                    },
                    {"role": "user", "content": "yes or no?"},
                ],
            )
            result = completion.choices[0].message.content
            self._debug(f"OpenAI response: snippet={(str(result)[:200]).replace('\n',' ')}")
            print(f"{Fore.GREEN}[+] {Fore.WHITE} Valid API found: {key}: {result}")
            return "YES"
        except AuthenticationError as e:
            try:
                code = e.body.get("code") if hasattr(e, 'body') else None
            except Exception:
                code = None
            self._debug(f"OpenAI auth error: code={code} message={str(e)}")
            return f'NO: {e.body["code"]}'
        except RateLimitError as e:
            try:
                code = e.body.get("code") if hasattr(e, 'body') else None
            except Exception:
                code = None
            self._debug(f"OpenAI rate limit: code={code} message={str(e)}")
            return f'NO: {e.body["code"]}'
        except Exception as e:
            self._debug(f"OpenAI exception: {e}")
            return "NO"