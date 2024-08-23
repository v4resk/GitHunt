import argparse
import os
from colorama import init, Fore
from core.Utils.HuntSession import HuntSession
from core.Utils.CustomArgFormatter import CustomArgFormatter
from core.Engines.HuntEngine import HuntEngine

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
        parser.add_argument('-m', '--module', dest='module', required=True, choices=["OpenAI"],
                            help='Hunting model to run')

        args = parser.parse_args()

        return args

    def run(self):
        ## Parse Arguments
        args = self.parse_arguments()
        self.module = args.module
        print(f'{Fore.GREEN}Running {self.module} module{Fore.WHITE}')

        ## Get hunting session / Github cookies
        self.hunt_session = HuntSession()

        ## Start hunting
        self.huntEngine = HuntEngine(self.hunt_session, self.module)