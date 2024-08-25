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

        subparsers = parser.add_subparsers(dest='command', required=True, help='Available commands')
        hunt_parser = subparsers.add_parser('hunt', help='Hunt for sensitive data',  formatter_class=CustomArgFormatter)
        hunt_parser.add_argument('-m', '--module', dest='module', required=True, choices=self.available_modules,
                            help='Hunting module to run')

        db_parser = subparsers.add_parser('db', help='Export the database',  formatter_class=CustomArgFormatter)
        db_parser.add_argument('-m', '--module', dest='module', required=True, choices=self.available_modules,
                            help='Module to manage in the database')
        db_parser.add_argument('-f', '--format', dest='format', choices=['json', 'csv','txt'], default="json",
                            help='Export output format (default: json)')
        db_parser.add_argument('-o', '--output', dest='output', default="githunt_db_export.out",
                            help='Output file')
        db_parser.add_argument('--all', action='store_true', help='If specified, invalide values will also be exported')                            

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

        # Init Database
        self.databaseEngine = DatabaseEngine(self.available_modules)


        if args.command == 'hunt':
            print(f'{Fore.CYAN}Starting the hunt for {self.module} module...{Fore.WHITE}')

            ## Get hunting session / Github cookies
            self.hunt_session = HuntSession()
            
            ## Start hunting
            self.huntEngine = HuntEngine(databaseEngine=self.databaseEngine, hunt_session=self.hunt_session, module=self.module)
            self.huntEngine.hunt()
            
        
        elif args.command == 'db':
            print(f'{Fore.CYAN}Managing the database for {self.module} module...{Fore.WHITE}')
            exportAll = args.all
            format = args.format
            output = args.output

            # Export database
            self.databaseEngine.exportDB(module=self.module,format=format, output=output, exportAll=exportAll)




        self.databaseEngine.close()


            
