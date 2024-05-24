from typing import List, Tuple

# from yacc.main import Producer


class YaccParser:
    
    def __init__(self,filename):
        self.terminal = []
        self.start = ""
        self.producer_list: List[Tuple[str, List[str]]] = []
        self.program2 = ""
        self.init_all(filename)

    def define_rules(self,ln):
        global start,terminal
        len_ln = len(ln)
        i = 0
        left = ""
        right = ""
        
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
                    if ln[i] != " " and ln[i] != "\n":
                        right += ln[i]
                    else:
                        if right:
                            self.terminal.append(right)
                            right = ""
                    i += 1
                if right:
                    self.terminal.append(right)
                    right = ""

            else:
                raise Exception("Unrecognized directive: " + left)

    def parse_production(self,ln, current_production):
        ln = ln.strip()
        rights =ln[1:]
        rights = rights.strip()
        self.producer_list.append((current_production,rights))

    def init_all(self,filename):
        current_production = None
        with open(filename, "r") as ifile:
            lines=ifile.readlines()
            i,k=0,0
            while i<len(lines):
                j=1
                if lines[i]=="\n":

                    i+=1
                    continue
                elif lines[i].strip()==";":

                    i+=1
                    continue
                elif lines[i].strip()=="":

                    i+=1
                    continue
                elif lines[i].startswith("%%"):

                    i+=1
                    k+=1
                    continue
                elif lines[i].startswith("%token"):

                    self.define_rules(lines[i])
                    i+=1
                    continue
                elif lines[i].startswith("%start"):
                    start = lines[i][len("%start"):].strip()
                    self.start=start
                    i+=1
                    continue
                elif len(lines[i].split())==1:

                    current_production=lines[i].strip()
                    while lines[j+i].strip()!=';':

                        self.parse_production(lines[j+i],current_production)
                        j+=1
                i=i+j