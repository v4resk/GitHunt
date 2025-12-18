from core.Dorks.Dorks import Dorks
import re

class ShodanDorks(Dorks):
    def __init__(self):
        super().__init__()
        self.keywords = [
            "shodan",
            "shodan_api",
            "shodan_api_key",
            "shodan_key",
        ]

        self.languages = [
            "Python",
            "Shell",
            "Go",
            "Markdown",
            "Text",
            "Ruby",
        ]

        self.regex_list = [
            re.compile(r"\"[A-Za-z0-9]{32}\""),  # Shodan API Key
        ]