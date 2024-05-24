# RegToDFA.py
# Author: Furina-Focalors
# Date: 2024.05.23

from NFA import NFA
from RegexNormalizer import ascii_dict, EPSILON, DOT

charset = []
for _, value in ascii_dict.items():
    charset.append(value)


def reg_to_nfa(regex: []) -> NFA:
    """
    将正则表达式转化成NFA
    :param regex: 所有的正则表达式
    :return: 生成的NFA
    """
    i = 0
    while i < len(regex):
        # 取出当前字符
        if regex[i] == '\\':  # 转义字符
            if regex[i + 1] != 'x':  # 长度为2
                step = 2
                cur_char = regex[i:i + step]
                i += 1
            else:  # 长度为4
                step = 4
                cur_char = regex[i:i + step]
                i += 3
        else:
            cur_char = regex[i]
        if cur_char == '|':
            pass
