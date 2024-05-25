# from typing import List, Tuple
# from yaccParser import *
# from init_Dic import *

# class first:
#     def __init__(self,Dict:Dic,yyl:YaccParser):
#         self.first_set:List[Tuple[str,set]]=[]
#         self.Dict=Dict
#         self.yyl=yyl

#     def calculate_first_set(self):

#         for producer in self.yyl.producer_list:#遍历每一个产生式
#             left=producer[0]
#             #先算形如A->aB的式子
#             if (self.Dict.string_to_num(producer[1][0])<0):
#                 self.first_set.append(left,producer[1][0])
#             else:
#                 continue
#         #再算形如A->BC的产生式
#         for producer in self.yyl.producer_list:
#             left=producer[0]
#             if(self.Dict.string_to_num(producer[1][0])>0):
#                 if()
            
