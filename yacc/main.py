from typing import List, Tuple
from yaccParser import *
                

def main():
    yyl = YaccParser("D:/lex-yacc/yacc/c99.y")
    
    print("Terminals:", yyl.terminal)
    print("Start Symbol:", yyl.start)
    print("Productions:")

    for production in yyl.producer_list:
     print(production[0]+" "+production[1]+" ")
main()