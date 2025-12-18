
from core.Auditors.Auditor import Auditor

class CensysAuditor(Auditor):
    def __init__(self):
        super().__init__()
        pass

    def is_valide(self,key):
        return "YES"