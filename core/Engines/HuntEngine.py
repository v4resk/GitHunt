from core.Utils.HuntSession import HuntSession
from pydoc import locate
from tqdm import tqdm
from bs4 import BeautifulSoup
import time

class HuntEngine():
    def __init__(self,hunt_session,module="OpenAI"):
        self.hunt_session = hunt_session
        self.module = module 


        # Load hunt module
        self.keywords = None
        self.languages = None
        self.regex_list = None
        self.init_hunt_module()
    

        # Load hunt auditor
        self.auditor = self.init_hunt_auditor()

        self.candidate_urls = [
            (f"https://github.com/search?q=/{regex.pattern}/+language:{language}&type=code&ref=advsearch", regex)
            for regex in self.regex_list
            for language in self.languages
            for keyword in self.keywords
        ]
    
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

    
    def hunt(self):
        # Github search here
        apis = []
        for url, pattern in self.candidate_urls:
            try:
                # 1. Search URL
                # 2. For each code block --> go to url 
                # 3. Regex api on content
                # 4. When finished --> Go next page

                print(f"Hunting for: {url}")
                response = self.hunt_session.session.get(url)
                if "You have exceeded a secondary rate limit" in soup.text:
                    for _ in tqdm(range(30), desc="⏳ Rate limit reached, waiting ..."):
                        time.sleep(1)
                    continue

                # Add APIs to list
                apis.extend(pattern.findall(response.text))
                

            except Exception as e:
                break
        return apis
        

    def db_key_exists(self, api_key):
        # Implement the database check for existing API keys here
        pass

    def db_insert(self, api_key, result):
        # Implement the database insert operation here
        pass