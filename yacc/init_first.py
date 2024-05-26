from typing import List, Tuple

class first_set:
    def __init__(self,filename):
        self.filename=filename
        self.firstSet:List[Tuple[str,set[str]]]=[]
        self.read_from_file()
    
    def read_from_file(self):
        with open(self.filename,"r")as file:
            for line in file:
                parts = line.strip().split(' ', 1)
                if len(parts) == 2:
                    left, right = parts
                self.firstSet.append((left,right))
    
    def output(self):
        for pro in self.firstSet:
            print(pro[0]+" "+pro[1])


# myFirstSet=first_set("./yacc/firstSet.txt")
# myFirstSet.output()
