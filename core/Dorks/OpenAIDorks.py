from core.Dorks.Dorks import Dorks
import re

class OpenAIDorks(Dorks):
    def __init__(self):
        super().__init__()
        self.keywords = [
            "AI ethics",
            "agent"
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
            re.compile(r"sk-proj-\S{74}T3BlbkFJ\S{73}A"),  # Named Project API Key
            re.compile(r"sk-proj-\S{58}T3BlbkFJ\S{58}"),  # Default Project API Key
            re.compile(r"sk-proj-[A-Za-z0-9]{20}T3BlbkFJ[A-Za-z0-9]{20}"),
            re.compile(r"sk-[a-zA-Z0-9]{48}"),  # Deprecated by OpenAI
        ]