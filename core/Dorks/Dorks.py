from abc import ABC, abstractmethod

class Dorks(ABC):
    def __init__(self):
        self.languages = None
        self.keywords = None
        self.regex_list = None
        pass

    def get_regex_list(self):
         return self.regex_list

    def get_keywords(self):
        return self.keywords

    def get_languages(self):
        return self.languages 