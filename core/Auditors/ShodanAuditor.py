from core.Auditors.Auditor import Auditor
from colorama import Fore
import shodan
import time
from tqdm import tqdm

class ShodanAuditor(Auditor):
    def __init__(self):
        super().__init__()
        pass

    def is_valide(self,key):

        try:
            time.sleep(1)
            self._debug("Shodan request: api.info()")
            api = shodan.Shodan(key)
            info = api.info()
            self._debug(f"Shodan response: plan={info.get('plan')}")

            if info['plan'] == 'dev' or info['plan'] == 'edu':
                print(f"{Fore.GREEN}[+] {Fore.WHITE} Valid API found: {key} ")
                return "YES"
            else:
                return "NO"
        except Exception as e:
            #print(e)
            if "Rate limit reached" in str(e):
                for _ in tqdm(range(40), desc=f"{Fore.RED}[-] {Fore.WHITE} Shodan rate limit reached, waiting ...", leave=False):
                    time.sleep(1)
                return "CHECK FAILED"
            self._debug(f"Shodan exception: {e}")
            return "NO"