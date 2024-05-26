from typing import List, Tuple
from yaccParser import *
from init_Dic import *

    
def main():
    yyl = YaccParser("./yacc/c99.y")
    Dict=Dic("./yacc/result.txt")
    print("Terminals:", yyl.terminal)
    print("Start Symbol:", yyl.start)
    print("Productions:")
    
    for dic in Dict.dictionaries:
        print (str(dic[0])+" "+dic[1]+" ")
    
    for production in yyl.producer_list:
        print(str(production[0])+" "+production[1]+" "+production[2])
    
    print(" ")

    # with open("./yacc/first_set.txt","r")as ifile:
    #     for lines in ifile:
    #         print(lines)
    


main()