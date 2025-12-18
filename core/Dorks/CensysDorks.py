from core.Dorks.Dorks import Dorks
import re

class CensysDorks(Dorks):
    def __init__(self):
        super().__init__()
        self.keywords = [
            "censys",
            "censys_api",
            "censys_api_key",
            "censys_api_id",
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
            re.compile(r'\b[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}\b'),  # Standard API ID
        ]