from typing import List, Tuple
from yaccParser import *
from init_Dic import *



class LRItem:
    def __init__(self,Pposition:int,GrammerInt:int,lookahead:int):
        self.Pposition=Pposition#点的位置
        self.GrammerInt=GrammerInt#对应的产生式
        self.lookahead=lookahead#向前搜索符


class LRState:
    def __init__(self,stateNumb:int,edgesMap:Tuple[int,int],LRItemsSet:set[LRItem]):
        self.stateNumb=stateNumb#状态号
        self.edgesMap=edgesMap#通过边到达另一个状态
        self.LRItemsSet=LRItemsSet#状态里的产生式项目

class LRDFA:
    def __init__(self,LRStateSet:List[LRState]):
        self.startNum = 0
        self.LRStateSet = LRStateSet
        self.yyl = YaccParser("./yacc/c99.y")#读取文法
        self.Dict = Dic("./yacc/result.txt")#读取字典

    def init_state_0(self):#设置拓广文法
        self.LRStateSet.append(LRState)
        self.LRStateSet[0].LRItemsSet.add
        self.LRStateSet[0].stateNumb=0
        Item_0:LRItem
        Item_0.Pposition=0
        Item_0.GrammerInt=0
        Item_0.lookahead=100#100代表$
        self.LRStateSet[0].LRItemsSet.add(Item_0)
