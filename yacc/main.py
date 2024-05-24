from typing import List, Tuple
from yaccParser import *
                

def main():
    yyl = YaccParser("./yacc/c99.y")
    
    print("Terminals:", yyl.terminal)
    print("Start Symbol:", yyl.start)
    print("Productions:")
    
    i=0
    for production in yyl.producer_list:
        i+=1
        print(production[0]+" "+production[1]+" ")
    print(i)
main()