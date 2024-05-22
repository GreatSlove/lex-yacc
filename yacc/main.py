from typing import List, Tuple
from yaccParser import *
                

def main():
    yyl = YaccParser("./yacc/c99.y")
    
    print("Terminals:", yyl.terminal)
    print("Start Symbol:", yyl.start)
    print("Productions:")
    for production in yyl.producer_list:
        print(production)
    

main()