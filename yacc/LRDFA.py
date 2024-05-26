from typing import List, Tuple
from yaccParser import *
from init_Dic import *
from init_first import *

class LRItem:
    def __init__(self,production:Tuple[str,List[str]],lookahead:int):
        self.Pposition=0#点的位置
        self.production=production#产生式
        self.lookahead=lookahead#向前搜索符


class LRState:
    def __init__(self,stateNumb:int,LRItemsSet:List[LRItem]):
        self.stateNumb=stateNumb#状态号
        self.edgesMap=()#Tuple[int,int]#通过边到达另一个状态
        self.LRItemsSet=LRItemsSet#状态里的产生式项目

class LRDFA:
    def __init__(self):
        self.startNum = 0
        self.LRStateSet=[]#:List[LRState]
        self.yyl = YaccParser("./yacc/c99.y")#读取文法
        self.Dict = Dic("./yacc/result.txt")#读取字典
        self.first=first_set("./yacc/firstSet.txt")#读取first集

    def init_state_0(self):#设置拓广文法
        # self.LRStateSet.append(LRState() for _ in range(0))
        # self.LRStateSet[0].LRItemsSet.add()
        # self.LRStateSet[0].stateNumb=0
        # Item_0:LRItem
        # Item_0.Pposition=0
        # Item_0.production=((start,'translation_unit'))
        # Item_0.lookahead=-88#-88代表$
        # self.LRStateSet[0].LRItemsSet.add(Item_0)
        state_0 = LRState(stateNumb=0, LRItemsSet=[])  # 创建状态0
        item_0 = LRItem(production=("start",["translation_unit"]), lookahead=-88)  # 创建LR项
        state_0.LRItemsSet.append(item_0)  # 将LR项添加到状态0的LR项集合中
        self.LRStateSet.append(state_0)  # 将状态0添加到LRDFA的LRStateSet列表中


    def print_LRItems(self):
        for state in self.LRStateSet:
            print(f"State Number: {state.stateNumb}")
            print("LR Items:")
            for item in state.LRItemsSet:
                print(f"Pposition: {item.Pposition}")
                print(f"Production: {item.production}")
                print(f"Lookahead: {item.lookahead}")
                print()
    #def state_internal_extension(self,LRState:LRState):
        
myLRDFA=LRDFA()
myLRDFA.init_state_0()
myLRDFA.print_LRItems()