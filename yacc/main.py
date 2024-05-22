def main():
    # 打开名为 "example.txt" 的文件
    with open('./yacc/test.txt', 'r') as file:
    # 逐行读取文件内容
      for line in file:
        # 输出每一行
        print(line.strip())  # 使用 strip() 方法去除每行末尾的换行符

def out():
   with open('./yacc/test.txt', 'r') as file:
      for ln in file:
         for i in ln[i]:
            print(ln[i])
        

def out1():
   with open('./yacc/test.txt', 'r') as file:  # 添加编码格式
      for ln in file:  # 遍历文件中的每一行
         for char in ln:  # 遍历当前行中的每个字符
            print(char)

def out2():
   with open('./yacc/test.txt', 'r', encoding='utf-8') as file:
      for ln in file:
         words = ln.split()  # 将行按空格分割成单词
         for i in range(len(words)):  # 使用索引遍历单词列表
            print(words[i])  # 输出索引和对应的单词


terminal = []
start = ""
Producer = tuple[str, list[str]]
producer_list: list[Producer] = []
program2 = ""

def define_rules(ln):
    global start
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
                        terminal.append(right)
                        right = ""
                i += 1
            if right:
                terminal.append(right)
        elif left == "start":
            start = ln[i:].strip()
        else:
            raise Exception("Unrecognized directive: " + left)

def parse_production(ln, current_production):
    ln = ln.strip()
    if not ln:
        return current_production, False
    
    if ':' in ln:
        left, rights = ln.split(':', 1)
        left = left.strip()
        #current_production = left
        rights = rights.strip()
        for right in rights.split(' '):
            right = right.strip()
            Producer.append(current_production, right.split())
    # elif ln[0] == '|':
    #     rights = ln[1:].strip()
    #     for right in rights.split('|'):
    #         right = right.strip()
    #         producer_list.append((current_production, right.split()))
    # elif ln == ';':
    #     current_production = None
    # return current_production, True

def init_all(filename):
    current_production = None
    with open(filename, "r") as ifile:
        lines=ifile.readlines()
        i=0
        while i<len(lines):
            j=0
            if lines[i].startswith("%"):
                define_rules(lines[i])
                i+=1
            elif '%%' in lines[i]:
                i+=1
                break
            else:
                if ' ' not in lines[i]:
                    current_production=lines[i]
                    j+=1
                parse_production(lines[j+i],current_production)
            
            

        

def main():
    filename = "./yacc/test.txt"
    init_all(filename)
    print("Terminals:", terminal)
    print("Start Symbol:", start)
    print("Productions:")
    for production in producer_list:
        print(production)


main()