import numpy as np
from typing import Tuple , List

class Dic:
    def __init__(self,mapping_file):
        self.mapping_file=mapping_file
        self.dictionaries: List[Tuple[int, str]] = []
        self.read_from_map(self.mapping_file)

    def read_from_map(self,mapping_file):
        with open(mapping_file,"r")as ifile:
            for lines in ifile:
                num,word=lines.strip().split(maxsplit=1)
                self.dictionaries.append((int(num),word))#读取映射文件，将其加入字典中

    def string_to_num(self,a:str)->int:
        assert any(a==item[1] for item in self.dictionaries) ,f"The string '{a}' is not in the list."
        return next(item[0] for item in self.dictionaries if item[1] == a)

    def num_to_string(self,b:int)->str:
        assert any(b==item[0] for item in self.dictionaries),f"The number '{b}' is not in the list."
        return next(item[1] for item in self.dictionaries if item[0] == b)