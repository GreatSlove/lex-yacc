from typing import List, Tuple

class YaccParser:
    def __init__(self,filename):
        self.terminal = []
        self.start = ""
        self.Producer = Tuple[str, List[str]]
        self.producer_list: List[Producer] = []
        self.program2 = ""
        self.init_all(filename)

    def define_rules(self, ln):
        left = ""
        right = ""
        len_ln = len(ln)
        i = 0
        flag = True
        if ln[i] == "%" and ln[i + 1] != "%":
            i += 1
            while i < len_ln and ln[i] == " ":
                i += 1
            while i < len_ln and ln[i] != " ":
                left += ln[i]
                i += 1
            while i < len_ln and ln[i] == " ":
                i += 1

            if left == "token":
                while i < len_ln:
                    if ln[i] != " ":
                        right += ln[i]
                        if i == len_ln - 1:
                            self.terminal.append(right)
                    else:
                        self.terminal.append(right)
                        right = ""
                    i += 1
            elif left == "start":
                self.start = ln[i:].strip()
            else:
                raise Exception("")
            
            
    def init_all(self, filename):
        with open(filename, "r") as ifile:
            self.read_from_stream(ifile)
        self.last_deal()