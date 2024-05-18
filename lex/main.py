from yylparser import *

def main():
    yyl = YylParser("./lex/c99.l")

    print("Define Rules:")
    for key, value in yyl.define_rules.items():
        print(f"{key}: {value}")

    print("\nRegex Rules:")
    for pattern, action in yyl.regex_rules:
        print(f"{pattern} -> {action}")

    print("\nProgram1:")
    print(yyl.program1)

    print("\nProgram2:")
    for line in yyl.program2.split('\n'):
        # 输出每行程序2的内容，并保持原始缩进
        print(line)


main()
