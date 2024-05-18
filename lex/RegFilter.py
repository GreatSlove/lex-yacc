class RegFfilter:
    Brace_left = 1
    Brace_right = 2
    Bracket_left = 3
    Bracket_right = 4
    CHAR_link = 5

    @staticmethod
    def spchar_filter(src):
        special_characters = {
            'p': ' ',
            'r': '\r',
            'n': '\n',
            't': '\t',
            'v': '\v',
            'f': '\f'
        }
        ans = ""
        i = 0
        src_len = len(src)
        while i < src_len:
            c = src[i]
            if c == "\\" and i + 1 < src_len:
                i += 1
                c = src[i]
                if c in special_characters:
                    ans += special_characters[c]
                else:
                    ans += '\\'
                    ans += c
            elif c == '{':
                ans += chr(RegFilter.Brace_left)
            elif c == '}':
                ans += chr(RegFilter.Brace_right)
            elif c == '[':
                ans += chr(RegFilter.Bracket_left)
            elif c == ']':
                ans += chr(RegFilter.Bracket_right)
            else:
                ans += c
            i += 1
        return ans
    
    @staticmethod
    def stringing_replace(string_big, string_src, string_dst):
        pos = 0
        while (pos := string_big.find(string_src, pos)) != -1:
            string_big = string_big[:pos] + string_dst + string_big[pos + len(string_src):]
            pos += len(string_dst)
        return string_big
    
    @staticmethod
    def replace_brace_pairs(string_content, string_map):
        string_result = string_content
        string_old = ""
        while string_result != string_old:
            string_old = string_result
            for pattern in string_map:
                string_result = RegFilter.stringing_replace(
                    string_result, chr(RegFilter.Brace_left) + pattern + chr(RegFilter.Brace_right), string_map[pattern]
                )
        return string_result

    @staticmethod
    def single_bracket_replace(string):
        tmp = ""
        len_ = len(string)
        i = 0
        while i < len_:
            c = string[i]
            if c == "\\":
                i += 1
                c = string[i]
                tmp += c
                i += 1
                continue
            if c == '-':
                tmp += chr(RegFilter.CHAR_link)
            else:
                tmp += c
            i += 1
        string = tmp
        array = [0] * 127
        new_string = ""
        if string[0] != '^':
            i = 0
            while i < len(string):
                if string[i] == chr(RegFilter.CHAR_link):
                    if i + 1 != len(string):
                        for k in range(ord(string[i - 1]), ord(string[i + 1]) + 1):
                            array[k] = 1
                    i += 2
                else:
                    array[ord(string[i])] = 1
                    i += 1
        else:
            for i in range(9, 127):
                array[i] = 1
            i = 0
            while i < len(string):
                if string[i] == chr(RegFilter.CHAR_link):
                    for k in range(ord(string[i - 1]), ord(string[i + 1]) + 1):
                        array[k] = 0
                    i += 2
                else:
                    array[ord(string[i])] = 0
                    i += 1
        for j in range(len(array)):
            if array[j] == 1:
                target = chr(j)
                if target in ['(', '|', ')', '+', '?', '*', '.', '\\']:
                    new_string += '\\' + target + '|'
                else:
                    new_string += target + '|'
        new_string = new_string[:-1]  
        return new_string 

    @staticmethod
    def replace_bracket_pairs(string):
        string1 = chr(RegFilter.Bracket_left)
        string2 = chr(RegFilter.Bracket_right)
        pos1 = 0
        pos2 = 0

        while (
            (pos1 := string.find(string1, pos1)) != -1
            and (pos2 := string.find(string2, pos1)) != -1
        ):
            pos1 = string.find(string1, pos1)
            pos2 = string.find(string2, pos2)
            len_ = pos2 - pos1

            string3 = "(" + RegFilter.single_bracket_replace(string[pos1 + 1 : pos2]) + ")"

            string = string[:pos1] + string3 + string[pos2 + 1 :]
            pos1 += len(string3)
            pos2 += len(string3)
        return string

    @staticmethod
    def set_dots(src):
        pos = -1
        while pos != -1:
            pos = -1
            in_bracket = False
            i = 0
            while i < len(src):
                if src[i] == "\\":
                    i += 2
                if in_bracket:
                    if src[i] == chr(RegFilter.Bracket_right):
                        in_bracket = False
                    i += 1
                    continue
                if src[i] == chr(RegFilter.Bracket_left):
                    in_bracket = True
                if src[i] == '.':
                    pos = i
                    break
                i += 1
            if pos != -1:
                src = src[:pos] + chr(RegFilter.Bracket_left) + chr(9) + "-" + chr(
                    126
                ) + chr(RegFilter.Bracket_right) + src[pos + 1 :]
        return src

    @staticmethod
    def total_filter(src, string_map):
        src = RegFilter.spchar_filter(src)
        src = RegFilter.replace_brace_pairs(src, string_map)
        src = RegFilter.set_dots(src)
        src = RegFilter.replace_bracket_pairs(src)
        return src


    @staticmethod
    def quoteFilter(src):
        ans = ""
        src = src[1 : len(src) - 1]
        #去除引号
        for c in src:
            if c in ['(', '|', ')', '+', '?', '*', '.', '\\']:
                ans += '\\'
                #在特殊符号前加转义字符
            ans += c
        return ans
    
    