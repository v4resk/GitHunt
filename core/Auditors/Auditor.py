from abc import ABC, abstractmethod
import os
from colorama import Fore

class Auditor(ABC):
    def __init__(self):
        # Debug is only enabled when GITHUNT_DEBUG environment variable is explicitly set to '1'
        # Default is '0', so debug is False by default
        self.debug = os.environ.get('GITHUNT_DEBUG', '0') == '1'

        def _debug(msg):
            if self.debug:
                print(f"{Fore.YELLOW}[debug]{Fore.WHITE} {msg}")
        self._debug = _debug

    """Return YES if valide"""
    @abstractmethod
    def is_valide(self):
         pass
