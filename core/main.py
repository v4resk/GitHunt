import argparse
from colorama import init, Fore
from core.Utils.HuntSession import HuntSession
from core.Utils.CustomArgFormatter import CustomArgFormatter
from core.Engines.HuntEngine import HuntEngine
from core.Config.Config import get_project_root
from core.Engines.DatabaseEngine import DatabaseEngine
import os

def banner():
    init(autoreset=True)

    ascii_art = f"""
    {Fore.CYAN} ██████{Fore.GREEN}╗ {Fore.CYAN}██{Fore.GREEN}╗{Fore.CYAN}████████{Fore.GREEN}╗{Fore.CYAN}██{Fore.GREEN}╗  {Fore.CYAN}██{Fore.GREEN}╗{Fore.CYAN}██{Fore.GREEN}╗   {Fore.CYAN}██{Fore.GREEN}╗{Fore.CYAN}███{Fore.GREEN}╗   {Fore.CYAN}██{Fore.GREEN}╗{Fore.CYAN}████████{Fore.GREEN}╗
    {Fore.CYAN}██{Fore.GREEN}╔════╝ {Fore.CYAN}██{Fore.GREEN}║╚══{Fore.CYAN}██{Fore.GREEN}╔══╝{Fore.CYAN}██{Fore.GREEN}║  {Fore.CYAN}██{Fore.GREEN}║{Fore.CYAN}██{Fore.GREEN}║   {Fore.CYAN}██{Fore.GREEN}║{Fore.CYAN}████{Fore.GREEN}╗  {Fore.CYAN}██{Fore.GREEN}║╚══{Fore.CYAN}██{Fore.GREEN}╔══╝
    {Fore.CYAN}██{Fore.GREEN}║  {Fore.CYAN}███{Fore.GREEN}╗{Fore.CYAN}██{Fore.GREEN}║   {Fore.CYAN}██{Fore.GREEN}║   {Fore.CYAN}███████{Fore.GREEN}║{Fore.CYAN}██{Fore.GREEN}║   {Fore.CYAN}██{Fore.GREEN}║{Fore.CYAN}██{Fore.GREEN}╔{Fore.CYAN}██{Fore.GREEN}╗ {Fore.CYAN}██║   {Fore.CYAN}██{Fore.GREEN}║   
    {Fore.CYAN}██{Fore.GREEN}║  {Fore.CYAN} ██{Fore.GREEN}║{Fore.CYAN}██{Fore.GREEN}║   {Fore.CYAN}██{Fore.GREEN}║   {Fore.CYAN}██{Fore.GREEN}╔══{Fore.CYAN}██{Fore.GREEN}║{Fore.CYAN}██{Fore.GREEN}║   {Fore.CYAN}██{Fore.GREEN}║{Fore.CYAN}██{Fore.GREEN}║╚{Fore.CYAN}██{Fore.GREEN}╗{Fore.CYAN}██{Fore.GREEN}║   {Fore.CYAN}██{Fore.GREEN}║   
    {Fore.GREEN}╚{Fore.CYAN}██████{Fore.GREEN}╔╝{Fore.CYAN}██{Fore.GREEN}║   {Fore.CYAN}██{Fore.GREEN}║   {Fore.CYAN}██{Fore.GREEN}║  {Fore.CYAN}██{Fore.GREEN}║╚{Fore.CYAN}██████{Fore.GREEN}╔╝{Fore.CYAN}██{Fore.GREEN}║ ╚{Fore.CYAN}████{Fore.GREEN}║   {Fore.CYAN}██{Fore.GREEN}║   
    {Fore.GREEN}╚═════╝ ╚═╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝   ╚═╝   
    {Fore.CYAN}                                             @v4resk 
    """

    print(ascii_art)    


class GitHunt:
    def __init__(self):
        pass

    def parse_arguments(self):
        parser = argparse.ArgumentParser(description='Hunt for sensitive data exposure on GitHub.', formatter_class=CustomArgFormatter)
        parser.add_argument('-m', '--module', dest='module', required=True, choices=self.available_modules,
                            help='Hunting model to run')

        args = parser.parse_args()
        return args
    
    def get_available_modules(self):
        dorks_dir = f"{get_project_root()}/Dorks"
        module_names = set()
        for file_name in os.listdir(dorks_dir):
            if file_name.endswith('Dorks.py'):
                base_name = file_name[:-8]
                if len(base_name) > 2:
                    module_names.add(base_name)
        return list(module_names)

    def run(self):
        ## Parse Arguments
        self.available_modules = self.get_available_modules()
        args = self.parse_arguments()
        self.module = args.module
        print(f'{Fore.CYAN}Running {self.module} module{Fore.WHITE}')

        # Init Database
        self.databaseEngine = DatabaseEngine(self.available_modules)

        ## Get hunting session / Github cookies
        self.hunt_session = HuntSession()

        ## Start hunting
        self.huntEngine = HuntEngine(databaseEngine=self.databaseEngine, hunt_session=self.hunt_session, module=self.module)
        self.huntEngine.hunt()

        #for api in apis:
        #    print(api)
        self.databaseEngine.close()