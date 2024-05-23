from typing import List, Tuple
from yaccParser import *
                

def main():
    yyl = YaccParser("./yacc/c99.y")
    
    print("Terminals:", yyl.terminal)
    print("Start Symbol:", yyl.start)
    print("Productions:")
    print(yyl.producer_list[0])
    # for production in yyl.producer_list:
    #     print(production[0]+" "+production[1]+" ")
    

main()