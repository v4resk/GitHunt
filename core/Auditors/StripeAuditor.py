from core.Auditors.Auditor import Auditor
from colorama import Fore
import requests 
from requests.auth import HTTPBasicAuth
import time
from tqdm import tqdm

class StripeAuditor(Auditor):
    def __init__(self):
        super().__init__()
        pass

    def is_valide(self,key):
        url = "https://api.stripe.com/v1/tokens"
        data = {
        'card[number]': '4888230002612218',
        'card[exp_month]': '12',
        'card[exp_year]': '2026',
        'card[cvc]': '994'

        }
        try:
            time.sleep(0.5)
            respons = requests.post(url=url, data=data, auth=HTTPBasicAuth(f'{key}', ''))

            if (respons.json()).get("error") and not (respons.json()).get("error").get("code") == "card_declined":
                #print(f"{Fore.RED}[-] {Fore.WHITE} Invalide API found: {respons.json()}")
                return "NO"
            elif (respons.json()).get("error") and (respons.json()).get("error").get("code") == "rate_limit":
                for _ in tqdm(range(40), desc=f"{Fore.RED}[-] {Fore.WHITE} Stripe rate limit reached, waiting ...", leave=False):
                    time.sleep(1)
                return "CHECK FAILED"
            else:
                print(f"{Fore.GREEN}[+] {Fore.WHITE} Valid API found: {key}")
                #print(respons.text)
                return "YES"
        except Exception as e:
            return "NO"