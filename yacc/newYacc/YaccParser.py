import numpy as np
from typing import Tuple , List

class YaccParser:
    def __init__(self,mapping_file,Yfile):
        self.array=np.zeros(10,250)
        self.Yfile=Yfile
        self.mapping_file=mapping_file
        #self.dictionary:Tuple[int,str] = (0, "")
        self.dictionaries: List[Tuple[int, str]] = []

    def read_from_map(self,mapping_file):
        with open(mapping_file,"r")as ifile:
            for lines in ifile:
                num,word=lines.strip().split(maxsplit=1)
                print(f"将({num}{word})放入字典中")
                self.dictionaries.append((int(num),word))#读取映射文件，将其加入字典中

    def string_to_num(self,a:str)->int:
        assert any(a==item[1] for item in self.dictionaries) ,f"The string '{a}' is not in the list."
        return next(item[0] for item in self.dictionaries if item[1] == a)

    def num_to_string(self,b:int)->str:
        assert any(b==item[0] for item in self.dictionaries),f"The number '{b}' is not in the list."
        return next(item[1] for item in self.dictionaries if item[0] == b)
    
    # def read_from_yfile(this,Yfile):
    #     with open(Yfile,"r")as yfile:
    #         i=0
    #         while 



