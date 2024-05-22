from typing import List, Tuple

terminal = []
start = ""
Producer = Tuple[str, List[str]]
producer_list: List[Producer] = []
program2 = ""

def define_rules(ln):
    global start,terminal
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
    rights =ln[1:]
    rights = rights.strip()
    for right in rights.split(' '):
        right = right.strip()
        producer_list.append((current_production,right))

def init_all(filename):
    current_production = None
    with open(filename, "r") as ifile:
        lines=ifile.readlines()
        i=0
        while i<len(lines):
            if lines[i].strip()=="\n":
                print('blank line')
                i+=1
                continue
            if lines[i].strip()=="":
                print('blank line')
                i+=1
                continue
            if lines[i].startswith("%"):
                print('阶段1')
                define_rules(lines[i])
                i+=1
                continue
            if ' ' not in lines[i]:
                print('阶段2')
                current_production=lines[i].strip()
                j=i+1
                while lines[j].strip()!=';':
                    print(current_production)

                    parse_production(lines[j],current_production)
                    j+=1
            i=j+i-1
         

                
                

def main():
    filename = "./yacc/c99.y"
    init_all(filename)
    print("Terminals:", terminal)
    print("Start Symbol:", start)
    print("Productions:")
    for production in producer_list:
        print(production)


main()