# RegexNormalizer.py
# Author: Furina-Focalors
# Date: 2024.05.21

ascii_dict = {} # ascii字符的原始表示形式和对应的字符，有\n和\xhh两种格式
for iteration in range(128):
    char = chr(iteration)
    if char == '\\':
        ascii_dict['\\\\'] = char
    elif char == '\a':
        ascii_dict['\\a'] = char
    elif char == '\b':
        ascii_dict['\\b'] = char
    elif char == '\f':
        ascii_dict['\\f'] = char
    elif char == '\n':
        ascii_dict['\\n'] = char
    elif char == '\r':
        ascii_dict['\\r'] = char
    elif char == '\t':
        ascii_dict['\\t'] = char
    elif char == '\v':
        ascii_dict['\\v'] = char
    elif char == '\'':
        ascii_dict['\\\''] = char
    elif char == '\"':
        ascii_dict['\\\"'] = char
    elif char == '\0':
        ascii_dict['\\0'] = char
    # 正则表达式中的保留字也需要转义
    elif char == '(':
        ascii_dict['\('] = char
    elif char == ')':
        ascii_dict['\)'] = char
    elif char == '|':
        ascii_dict['\|'] = char
    elif char == '*':
        ascii_dict['\*'] = char
    else:
        if 32 <= iteration <= 126:  # 可打印字符
            ascii_dict[char] = char
        else:  # 非可打印字符，使用十六进制表示
            ascii_dict['\\x' + format(iteration, '02x')] = char
EPSILON = chr(128) # 用一个非法ascii字符表示空串


class RegexNormalizer:
    @staticmethod
    def eliminate_brace(regex: str, support_definitions: dict)->str:
        """
        消除{}：其中的内容在辅助定义部分定义过，直接替换
        :param regex: 正则表达式
        :param support_definitions: 辅助定义
        :return: 消除后的正则表达式
        """
        i = 0
        in_bracket = False
        while i in range(len(regex)):
            # 中括号内双引号"不被转义，需要单独处理
            if regex[i]=='[' and (i==0 or regex[i-1]!='\\'):
                in_bracket = True
                i+=1
                continue
            if in_bracket and regex[i]==']' and regex[i-1]!='\\':
                in_bracket = False
                i+=1
                continue
            # 处理转义字符
            if regex[i]=='\\':
                if i+1>=len(regex):
                    raise Exception("Unclosed escape character.")
                else:
                    i+=2 # 跳过被转义的字符
                    continue
            # 处理引号内容
            if not in_bracket and regex[i]=='"': # 跳过引号中的内容
                i+=1
                if i >= len(regex):
                    raise Exception("Unclosed quotation mark.")
                #result += regex[i]
                while regex[i]!='"' or (regex[i]=='"' and regex[i-1]=='\\'):
                    i+=1
                    if i >= len(regex):
                        raise Exception("Unclosed quotation mark.")
                    #result += regex[i]
                #result += regex[i+1]
                i+=1 # 跳过右引号"
                continue

            if regex[i]=='{':
                start=i
                # 获取左部
                symbol=""
                while regex[i]!="}":
                    symbol += regex[i]
                    i+=1
                    if i >= len(regex):
                        raise Exception("Unclosed '{'.")
                symbol=symbol[1:]
                end=i
                # 将原字符串中[start:end+1]的部分替换为support_definition[symbol]
                regex = regex[:start] + support_definitions[symbol] + regex[end+1:]
                i=start # 替换后可能产生新的大括号
                continue
            i+=1
        return regex

    @staticmethod
    def eliminate_question_addition(regex: str)->str:
        """
        去除正则表达式中的+和?
        :param regex:
        :return:
        """
        stack = [] # 用于括号匹配
        i = 0
        in_bracket = False # 方括号内的+?没有转义，需要单独考虑
        while i in range(len(regex)):
            # 跳过转义字符
            if regex[i] == '\\':
                if i + 1 >= len(regex):
                    raise Exception("Unclosed escape character.")
                else:
                    i += 2  # 跳过被转义的字符
                    continue
            # 跳过引号中的内容
            if not in_bracket and regex[i] == '"':
                i += 1
                if i >= len(regex):
                    raise Exception("Unclosed quotation mark.")
                while regex[i] != '"' or regex[i] == '"' and regex[i - 1] == '\\':
                    i += 1
                    if i >= len(regex):
                        raise Exception("Unclosed quotation mark.")
                i += 1  # 跳过右引号"
                continue

            if regex[i] == '(': # 左括号，入栈
                stack.append(('(',i))
                i+=1
            elif regex[i] == '[':
                stack.append(('[',i))
                in_bracket = True
                i+=1
            elif (regex[i] == ')' or regex[i] == ']') and regex[i-1]!='\\': # 右括号
                bracket, left_i = stack.pop()
                if regex[i] == ')' and bracket!='(':
                    raise Exception("Unmatched ')'.")
                elif regex[i] == ']':
                    in_bracket = False
                    if bracket!='[':
                        raise Exception("Unmatched ']'.")

                if not in_bracket and i+1<len(regex) and regex[i+1]=='+': # 将(a)+处理成(a)(a)*
                    regex = regex[:left_i] + regex[left_i:i+1] + regex[left_i:i+1] + '*' + regex[i+2:]
                    i += i - left_i + 2 # 多出来的(a)*不需要处理
                elif not in_bracket and i+1<len(regex) and regex[i+1]=='?': # 将(a)?处理成((a)|EPSILON)
                    regex = regex[:left_i] + '(' + regex[left_i:i+1] + '|' + EPSILON + ')' + regex[i+2:]
                    i += 5 # |和EPSILON不需要处理
                else: # 括号后面没有需要处理的符号
                    i += 1
            elif not in_bracket and regex[i] == '+': # 将a+处理成aa*
                regex = regex[:i] + regex[i-1] + '*'
                i+=2 # *不需要处理
            elif not in_bracket and regex[i] == '?': # 将a?处理成(a|EPSILON)
                regex = regex[:i-1] + '(' + regex[i-1] + '|' + EPSILON + ')' + regex[i+1:]
                i+=4 # EPSILON不需要处理
            else: # 普通字符
                i+=1
        return regex


    @staticmethod
    def eliminate_dots(regex: str)->str:
        """
        消除正规表达式中的.
        :param regex: 正则表达式
        :return: 消除后的结果
        """
        i = 0
        in_bracket = False
        while i in range(len(regex)):
            # 中括号内双引号"不被转义，需要单独处理
            if regex[i] == '[' and (i == 0 or regex[i - 1] != '\\'):
                in_bracket = True
                i += 1
                continue
            if in_bracket and regex[i] == ']' and regex[i - 1] != '\\':
                in_bracket = False
                i += 1
                continue
            if regex[i] == '\\':  # 转义符
                if i + 1 >= len(regex):
                    raise Exception("Unclosed escape character.")
                else:
                    i += 2  # 跳过被转义的字符
                    continue

            if not in_bracket and regex[i] == '"':  # 跳过引号中的内容
                i += 1
                if i >= len(regex):
                    raise Exception("Unclosed quotation mark.")
                while regex[i] != '"' or regex[i] == '"' and regex[i - 1] == '\\':
                    i += 1
                    if i >= len(regex):
                        raise Exception("Unclosed quotation mark.")
                i += 1  # 跳过右引号"
                continue

            if regex[i] == '.':
                all_chars="("
                for key,_ in ascii_dict.items(): # 除\n外的所有字符
                    if key != '\\n':
                        all_chars += key + '|'
                all_chars = all_chars[:len(all_chars)-1] + ')'
                regex = regex[:i] + all_chars + regex[i+1:]
                i += len(all_chars)
                continue
            i+=1
        return regex

    @staticmethod
    def convert_bracket_content(content: str)->str:
        """
        将中括号内的内容转换成非扩展形式的正则表达式
        :param content: 提取出的中括号内容
        :return: 转换结果
        """
        i = 0
        invert = False
        if content[0]=='^': # 取反
            invert = True
            i += 1

        result = ""
        cur_chars = set()
        while i<len(content):
            # print('current char: ',content[i])
            # if i+1<len(content):
            #     print('next char:',content[i+1])

            # 处理转义字符
            if content[i]=='\\':
                cur_chars.add(content[i:i+2])
                i += 2
            # 处理x-y的情况
            elif content[i]=='-':
                if i+1>=len(content): # 以-结尾表示只是普通的减号
                    cur_chars.add(content[i])
                    i+=1
                    continue
                start = ord(content[i-1])
                end = ord(content[i+1])
                for j in range(start, end+1):
                    cur_chars.add(chr(j))
                i += 2 # 跳过结束符y
            # 处理普通字符
            else:
                cur_chars.add(content[i])
                i+=1
        # 对于正则表达式中需要转义但在python表示中未转义的字符，需要添加转义符
        modified_chars = set()
        for character in cur_chars:
            if character in ['\'','\"','(',')','|','*']:
                modified_chars.add('\\'+character)
            else:
                modified_chars.add(character)

        # print('elements of chars in original set of"',content,'": ')
        # for element in cur_chars:
        #     print(element)
        # print('---------------')
        # print('elements of chars in "',content,'": ')
        # for element in modified_chars:
        #     print(element)
        # print('---------------')

        if invert:
            for key,value in ascii_dict.items():
                if key not in modified_chars:
                    result+=key+'|'
        else:
            for key in modified_chars:
                result +=ascii_dict[key]+'|'
        return '('+result[:len(result)-1]+')'



    @staticmethod
    def eliminate_bracket(regex: str)->str:
        """
        消除[]：多字符，有四种情况需要处理：（包含两个保留字-和^）
            [xyz]: 表示x|y|z
            [^xyz]: 表示xyz以外的所有字符
            [a-z]: 表示x和z之间的所有字符，即a|b|...|z
            [^a-z]
        :param regex: 正则表达式
        :return: 消除后的正则表达式
        """
        i = 0
        while i in range(len(regex)):
            if regex[i]=='\\': # 转义符
                if i+1>=len(regex):
                    raise Exception("Unclosed escape character.")
                else:
                    i+=2 # 跳过被转义的字符
                    continue

            if regex[i]=='"': # 跳过引号中的内容
                i+=1
                if i >= len(regex):
                    raise Exception("Unclosed quotation mark.")
                while regex[i]!='"' or regex[i]=='"' and regex[i-1]=='\\':
                    i+=1
                    if i >= len(regex):
                        raise Exception("Unclosed quotation mark.")
                i+=1 # 跳过右引号"
                continue
            # 处理中括号
            if regex[i]=='[':
                pre = i
                start = i+1
                i+=1
                if i >= len(regex):
                    raise Exception("Unclosed '['.")
                # 获取[]内的内容
                symbol = ""
                while regex[i] != ']' or (regex[i]==']' and regex[pre]=='\\'):
                    symbol += regex[i]
                    i += 1
                    pre += 1
                    if i >= len(regex):
                        raise Exception("Unclosed '['.")
                end = i # regex[start:end]是中括号里的内容
                # print(regex[start:end])
                converted = RegexNormalizer.convert_bracket_content(regex[start:end])
                # print(converted)
                # 将[content]替换为converted
                regex = regex[:start-1] + converted + regex[i+1:]
                # print(len(converted),' ',len(regex[start:end]),' ',regex[i])
                i += len(converted)-len(regex[start:end])-1

                # print("i=",i)
                # print(regex)
                # if i<len(regex):
                #     print('regex[i]=',regex[i])
                # print('--------------------')
                continue
            i+=1
        return regex

    @staticmethod
    def convert_quotation_content(content: str)->str:
        """
        将引号中的内容转换为正则表达式
        :param content: 引号中的内容
        :return: 转换结果
        """
        reserved = ['|', '*', '(', ')', '\\'] # 如果引号中包含这些保留字，需要加上\转义
        result = ""
        i = 0
        while i<len(content):
            if content[i] in reserved:
                result += '\\' + content[i]
            else:
                result += content[i]
            i += 1
        return result


    @staticmethod
    def eliminate_quotations(regex: str)->str:
        """
        消除正则表达式中的双引号
        :param regex: 正则表达式
        :return: 消除引号后的正则表达式
        """
        i = 0
        while i in range(len(regex)):
            if regex[i]=='\\': # 转义符
                if i+1>=len(regex):
                    raise Exception("Unclosed escape character.")
                else:
                    i+=2 # 跳过被转义的字符
                    continue

            if regex[i]=='"':
                i += 1
                if i>=len(regex):
                    raise Exception("Unclosed quotation mark.")
                start=i
                while regex[i] != '"' or regex[i] == '"' and regex[i - 1] == '\\':
                    i += 1
                    if i >= len(regex):
                        raise Exception("Unclosed quotation mark.")
                end=i
                # regex[start:end]是引号中的内容
                # print('original: ',regex[start:end])
                converted = RegexNormalizer.convert_quotation_content(regex[start:end])
                # print('converted: ',converted)
                # 将regex[start-1:end+1]替换为converted
                regex = regex[:start-1] + converted + regex[end+1:] # "]"->]
                i += len(converted) - len(regex[start:end]) - 1
                continue
            i+=1
        return regex

    @staticmethod
    def normalize(regex: str, support_definitions: dict)->str:
        """
        将输入的正则表达式进行规范化
        :param regex: 正则表达式
        :param support_definitions: 辅助定义
        :return: 规范化后的正则表达式
        """
        # 以下操作过程必须**按序**进行
        # 消去{}
        eli_brace = RegexNormalizer.eliminate_brace(regex, support_definitions)
        # 消去?和+
        eli_question_addition = RegexNormalizer.eliminate_question_addition(eli_brace)
        # 消去.
        eli_dots = RegexNormalizer.eliminate_dots(eli_question_addition)
        # 消去[]
        eli_bracket = RegexNormalizer.eliminate_bracket(eli_dots)
        # 消去""
        eli_quotation = RegexNormalizer.eliminate_quotations(eli_bracket)
        return eli_quotation

    @staticmethod
    def add_dots(regex: str)-> []:
        """
        为正则表达式加“点”，划分连缀关系
        :param regex:
        :return:
        """
        i=0
        cur_item = ""
        last_left_parenthesis=-1
        result=[]
        parenthesis_stack = [] # 用一个栈存放左括号的下标，仅当栈空时才表示构成完整的一项
        while i<len(regex):
            #print('current regex[i]=',regex[i])
            if regex[i] == '\\': # 读到转义字符，跳过下面的判断
                pass
            elif regex[i] == '(': # 非转义(
                parenthesis_stack.append(i)

                #print('parenthesis_stack pushed at i=',i,', regex[i]=',regex[i])

                cur_item += regex[i]
                i+=1
                continue
            elif regex[i] == '|': # 非转义|
                cur_item += regex[i]
                i+=1
                continue
            elif regex[i] == '*': # 非转义*
                cur_item += regex[i]
                i += 1
            elif regex[i] == ')': # 非转义)
                if len(parenthesis_stack)==0:
                    print('At regex: ',regex)
                    print('i=',i)
                    print('cur_item = ',cur_item)
                    print('parenthesis_stack: ', parenthesis_stack)
                    print('current result: ',result)
                    raise Exception("Unclosed ')'.")

                last_left_parenthesis = parenthesis_stack.pop()

                #print('parenthesis_stack popped at i=', i, ', regex[i]=', regex[i])

                cur_item += regex[i]
                i+=1
                # 将后续的所有*读入
                while i<len(regex) and regex[i]=='*':
                    cur_item += regex[i]
                    i+=1

            if i>=len(regex):
                break

            # 栈空，有两种可能：刚读完)或*，或者本来就没有括号
            if len(parenthesis_stack)==0:
                if last_left_parenthesis!=-1: # 读进了一个完整的括号，将它提出
                    result.append(cur_item)
                    cur_item=""
                    last_left_parenthesis=-1
                if regex[i] == '(':  # 如果在这里读到括号，说明刚读完)或者*，后面又是新的括号
                    continue
                # 当前常规字符后面是什么？
                cur_item += regex[i]
                if i==len(regex)-1: # 最后一个字符，加入数组后直接结束
                    result.append(cur_item)
                    cur_item=""
                    i+=1
                    continue
                elif regex[i]=='\\': # 转义字符
                    if regex[i+1]!='x': # 长度为2
                        cur_item += regex[i+1]
                        i += 1
                    else: # 长度为4
                        cur_item += regex[i + 1] + regex[i + 2] + regex[i + 3]
                        i += 3
                    if i==len(regex)-1: # 当前转义字符是最后一个字符
                        result.append(cur_item)
                        cur_item=""
                        i+=1
                        continue

                if regex[i+1] not in [')','|','*']: # 下一位也是字符或者是新的括号，说明当前位需要被分割
                    result.append(cur_item)
                    cur_item=""
                    i+=1
                    continue
                i+=1
            else: # 栈非空，读到的是某个括号里的东西
                if regex[i] in ['(',')','|','*']: # 如果读到了保留字，需要重新判断处理
                    continue
                else: # 普通字符，直接写入
                    cur_item += regex[i]
                    i+=1


        if len(cur_item)!=0:
            result.append(cur_item)
        return result



    @staticmethod
    def infix_to_postfix(regex: str)->str:
        """
        将中缀表达式转化为后缀表达式
        :param regex: 中缀正则表达式
        :return: 对应的后缀正则表达式
        """
        # 将每个连缀区域进行后缀表达即可，整个正则表达式的后缀形式就是这些连缀区域直接相连
        end_mark = chr(129) # 用一个非法字符作为结束符
        regex = regex + end_mark
        stack = [end_mark]
        result = ""
        in_stack_pri = { # 栈内优先级
            end_mark: 0,
            "(": 1,
            "|": 3,
            "*": 5,
            ")": 6,
        }
        in_coming_pri = { # 栈外优先级
            end_mark: 0,
            "(": 6,
            "|": 2,
            "*": 4,
            ")": 1,
        }
        operators = ['(',')','*','|',end_mark]
        i=0
        while regex[i]!=end_mark or stack[-1]!=end_mark:
            if regex[i]=='\\': # 转义字符，输出
                if regex[i + 1] != 'x':  # 长度为2
                    result += regex[i] + regex[i + 1]
                    i += 2
                else:  # 长度为4
                    result += regex[i] + regex[i + 1] + regex[i + 2] + regex[i + 3]
                    i += 4
            elif i<len(regex)-1 and regex[i:i+2] in ['<%','%>','<:',':>']: # 中括号和大括号的特殊表示
                result += regex[i] + regex[i+1]
                i += 2
            elif regex[i] not in operators: # 普通字符，输出
                result += regex[i]
                i += 1
            else: # 操作符
                if in_coming_pri[regex[i]]>in_stack_pri[stack[-1]]: # 栈外优先级高
                    stack.append(regex[i])
                    i += 1
                elif in_coming_pri[regex[i]]<in_stack_pri[stack[-1]]: # 栈内优先级高
                    result += stack.pop()
                else: # 优先级相等
                    item = stack.pop()
                    if item=='(':
                        i+=1
        return result
