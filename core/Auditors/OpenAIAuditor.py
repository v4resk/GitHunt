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
            print(f"{Fore.GREEN}[+] {Fore.WHITE} Valid API found: {key}: {result}")
            return "YES"
        except AuthenticationError as e:
            return f'NO: {e.body["code"]}'
        except RateLimitError as e:
            return f'NO: {e.body["code"]}'
        except Exception as e:
            return "NO"