from core.Dorks.Dorks import Dorks
import re

class StripeDorks(Dorks):
    def __init__(self):
        super().__init__()
        self.keywords = [
            "stripe",
            "api",
            "stripe_api_key",
            "key",
            "apikey",
        ]

        self.languages = [
            '"Jupyter Notebook"',
            "Python",
            "Shell",
            "JavaScript",
            "TypeScript",
            "Java",
            "Go",
            "C%2B%2B",
            "PHP",
            "Markdown",
            "Text",
            "Ruby",
        ]

        self.regex_list = [
            re.compile(r"sk_live_[0-9a-zA-Z]{24}"),  # Standard API Key
            re.compile(r"rk_live_[0-9a-zA-Z]{24}"),  # Restricted API Key
        ]