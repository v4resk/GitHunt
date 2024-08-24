from core.Dorks.Dorks import Dorks
import re

class PerplexityDorks(Dorks):
    def __init__(self):
        super().__init__()
        self.keywords = [
            "agent",
            "ai",
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
        ]

        self.regex_list = [
            re.compile(r"pplx-[a-zA-Z0-9]{40,}"),  # Perplexity API Key
        ]