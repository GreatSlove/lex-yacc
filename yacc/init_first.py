from typing import List, Tuple,Set,Dict
from init_Dic import *
class first_set:
    def __init__(self,filename):
        self.filename=filename
        self.firstSet:List[Tuple[str,List[str]]]=[]
        self.read_from_file()
        self.firstMap:Dict[int,Set[int]]={}
        self.Dic=Dic("./yacc/result.txt")
        self.read_txt1()
    
    def read_txt1(self):
        with open("./yacc/first_set.txt", 'r') as file:
            for line in file:
                numbers = list(map(int, line.strip().split()))
                key = numbers[0]
                values = set(numbers[1:])
                self.firstMap[key] = values
                    

    def read_from_file(self):
        with open(self.filename,"r")as file:
            for line in file:
                parts = line.strip().split(' ', 1)
                if len(parts) == 2:
                    left, right = parts
                self.firstSet.append((left,right))
    
    def output(self):
        for key, values in self.firstMap.items():
            for value in values:
                print(f"right:{key}->{value}")


# myFirstSet=first_set("./yacc/firstSet.txt")
# myFirstSet.output()
