from core.Auditors.Auditor import Auditor
from colorama import Fore
from openai import AuthenticationError, OpenAI, RateLimitError

class PerplexityAuditor(Auditor):
    def __init__(self):
        super().__init__()
        pass

    def is_valide(self,key):
        model="llama-3-sonar-large-32k-online"
        try:
            client = OpenAI(api_key=key, base_url="https://api.perplexity.ai")

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