from YyLexReader import *

def main():
    yyl = YyLexReader("./lex/c99.l")
    print(yyl.userProgramHeaders)
    print("-----------------")

    print(yyl.userProgram)
    print("-----------------")

    for key,val in yyl.supportDefinitions.items():
        print(key,' ',val)
    print("-----------------")

    for element in yyl.rules:
        print(element)
    print("-----------------")


if __name__=="__main__":
    main()
