import time
from colorama import Fore
import os

class ProgressManager:
    def __init__(self, progress_file=".githunt_session"):
        self.progress_file = progress_file

    def save(self, from_iter: int, total: int):
        with open(self.progress_file, "w") as file:
            file.write(f"{from_iter}/{total}/{time.time()}")

    def load(self, total: int) -> int:
        if not os.path.exists(self.progress_file):
            return 0

        with open(self.progress_file, "r") as file:
            last, totl, tmst = file.read().strip().split("/")
            last, totl = int(last), int(totl)

        if time.time() - float(tmst) < 3600 and totl == total:
            action = input(f"{Fore.YELLOW}[+] {Fore.WHITE} Progress found, do you want to continue from the last progress ({last}/{totl})? [yes] | no: ").lower()
            if action in {"yes", "y", ""}:
                return last

        return 0