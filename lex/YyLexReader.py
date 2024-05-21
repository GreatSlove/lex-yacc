# YyLexReader.py
# Author: Furina-Focalors
# Date: 2024.05.21
from typing import List


class YyLexReader:
    """
        读取lex文件，转化成可处理的形式
        ---
        Attributes:
        userProgramHeaders: str 由%{ %}括起来的直接放入c代码的部分程序

        supportDefinitions: dict 辅助定义部分，每一个条目是一个产生式

        rules: List[(str,str)] 每一项是一个pair(str,str)，左边是匹配的正则表达式，右边是执行的c代码操作，由识别规则部分得到

        userProgram: str 用户子程序
    """
    def __init__(self, filename: str):
        self.userProgramHeaders: str = ""
        self.supportDefinitions: dict = {}
        self.rules: List[(str,str)] = []
        self.userProgram: str = ""
        # 读取文件
        with open(filename, "r") as file:
            self.read_file(file)

    def str_to_pair(self, line: str) -> (str, str):
        """
        将一行字符串转化为一个pair
        :param line: str
        :return: (str, str)
        """
        # 右侧的所有串都以下面这六个中的一种起始
        splits = [
            line.find(' ('),
            line.find(' ['),
            line.find(' {'),
            line.find('\t('),
            line.find('\t['),
            line.find('\t{')
        ]
        # split1 = line.find(' ')
        # split2 = line.find('\t{')
        # # 找到前后的分隔位置
        # if split1>=0 and split2>=0:
        #     split = min(split1, split2)
        # elif split1<0:
        #     split = split2
        # else:
        #     split = split1
        split = max(splits)
        return line[:split].strip(),line[split+1:].strip()

    def read_file(self, file):
        step = 0
        in_header = False
        for line in file:
            line = line.strip() # 去除头尾的空白字符
            # print(line)
            # header中的部分将直接被写入最后的c程序
            if in_header:
                if line=="%}":
                    in_header = False
                else:
                    self.userProgramHeaders += line + '\n'
            elif line=="%{":
                in_header = True
            elif line=="%%": # 分隔符
                step += 1
            elif line=="":
                continue
            elif step==0: # 辅助定义部分
                left, right = self.str_to_pair(line)
                self.supportDefinitions[left] = right
            elif step==1: # 识别规则部分
                left, right = self.str_to_pair(line)
                self.rules.append((left, right))
            elif step==2: # 用户子程序部分
                self.userProgram += line + '\n'
            else:
                raise Exception("An error occurred when reading .l file.\n")

