class DFANode:
    def __init__(self):
        self.id = 0
        self.flag = 0
        self.ptrs = {}

DFANodes = [DFANode() for _ in range(65536)]
minDFA = [DFANode() for _ in range(65536)]