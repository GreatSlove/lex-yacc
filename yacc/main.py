terminal = []
start = ""
Producer = tuple[str, list[str]]
producer_list: list[Producer] = []
program2 = ""

def define_rules(ln):
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
    ln_=ln[1:]
    ln_=ln_strip()

    rights = ln_
    rights = rights.strip()
    for right in rights.split(' '):
        right = right.strip()
        Producer.append((current_production, right.split()))

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
                continue
            # else:
            #     if ' ' not in lines[i]:
            #         current_production=lines[i]
            #         j+=1
            #     parse_production(lines[j+i],current_production)
            #     i=i+j+1

def main():
    filename = "./yacc/test.txt"
    init_all(filename)
    print("Terminals:", terminal)
    print("Start Symbol:", start)
    print("Productions:")
    for production in producer_list:
        print(production)


main()