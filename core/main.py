import argparse
import os
from colorama import init, Fore
from core.Utils.Cookies import Cookies

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


    def run(self):
        github_cookies = Cookies()
        pass