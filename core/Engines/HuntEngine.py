from core.Utils.HuntSession import HuntSession
from core.Utils.ProgressManager import ProgressManager
from pydoc import locate
from tqdm import tqdm
from bs4 import BeautifulSoup
import time
from colorama import init, Fore
import re
import json

class HuntEngine():
    def __init__(self,hunt_session,module="OpenAI", resume=None):
        self.progress_manager = ProgressManager()
        self.hunt_session = hunt_session
        self.module = module 
        self.resume = resume

        # Load hunt module
        self.keywords = None
        self.languages = None
        self.regex_list = None
        self.init_hunt_module()

        # Load hunt auditor
        self.auditor = self.init_hunt_auditor()
        candidate_urls_with_keywords = [
            (f"https://github.com/search?q={keyword}+AND+(/{regex.pattern}/)+language:{language}&type=code&ref=advsearch", regex)
            for regex in self.regex_list
            for language in self.languages
            for keyword in self.keywords
        ]

        # Define the second type of candidate URLs without keywords
        candidate_urls_without_keywords = [
            (f"https://github.com/search?q=/{regex.pattern}/+language:{language}&type=code&ref=advsearch", regex)
            for regex in self.regex_list
            for language in self.languages
        ]

        # Combine both lists
        self.candidate_urls = candidate_urls_with_keywords + candidate_urls_without_keywords
        pass

    def init_hunt_module(self):
        try:
            hunt_module_str = f"core.Dorks.{self.module}Dorks.{self.module}Dorks"
            hunt_module_class = locate(hunt_module_str)
            hunt_module_instance = hunt_module_class()
            #print(f"Found hunt module: {hunt_module_str}")

            self.keywords = hunt_module_instance.get_keywords()
            self.languages = hunt_module_instance.get_languages()
            self.regex_list = hunt_module_instance.get_regex_list()

            return True
        except Exception as ex:
            print(ex)
            return False

    def init_hunt_auditor(self):
        try:
            hunt_module_str = f"core.Auditors.{self.module}Auditor.{self.module}Auditor"
            hunt_module_class = locate(hunt_module_str)
            hunt_module_instance = hunt_module_class()
            #print(f"Found auditor module: {hunt_module_str}")

            return True
        except Exception as ex:
            print(ex)
            return False

    def rate_limit_check(self,response):
        if "You have exceeded a secondary rate limit" in response.text:
                    for _ in tqdm(range(30), desc=f"{Fore.RED}[-] {Fore.WHITE} Rate limit reached, waiting ..."):
                        time.sleep(1)
    
    def hunt(self):
        # Github search here
        apis = set()
        expand_urls = []
        
        for url, pattern in self.candidate_urls:
            next_page = 1
            while next_page < 6:
                try:
                    # 0. Perform a GitHub search
                    print(f"{Fore.GREEN}[+] {Fore.WHITE}Hunting for: {url}")
                    response = self.hunt_session.session.get(url)
                    self.rate_limit_check(response)

                    # 1. Get all GitHub files that matched our searcg
                    data = json.loads(response.text)
                    matching_files = [
                        f"https://github.com/{result['repo_nwo']}/blob/{result['commit_sha']}/{result['path']}"
                        for result in data['payload']['results']
                    ]                    
                    expand_urls.extend(matching_files)

                    # 2. Request all files and extract secrets with corresponding regex 
                    for e_url in expand_urls:
                        response_e = self.hunt_session.session.get(e_url)
                        #print(e_url)
                        self.rate_limit_check(response_e)
                        apis.update(pattern.findall(response_e.text))

                        #Check API Here ?
                        #Insert in DB, dedup db

                    expand_urls = []

                    # 4. Go next page:
                    next_page = next_page+1
                    page_pattern = r"&p=[1-4]"
                    if re.search(page_pattern, url):
                        url = re.sub(page_pattern, f"&p={next_page}", url)
                    else:
                        url = f"{url}&p=2"

                    #for api in apis:
                    #    print(api)

                except Exception as e:
                    print(e)
                    continue
        return apis
        

    def db_key_exists(self, api_key):
        # Implement the database check for existing API keys here
        pass

    def db_insert(self, api_key, result):
        # Implement the database insert operation here
        pass