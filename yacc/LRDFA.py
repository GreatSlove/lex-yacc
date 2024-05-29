from typing import List, Tuple,Set
from yaccParser import *
from init_Dic import *
from init_first import *
import queue

class Item:
    def __init__(self,productionInt:int,lookahead:Set[int]):
        self.Pposition=0#点的位置
        self.productionInt=productionInt#产生式
        self.lookahead=lookahead#向前搜索符


class ItemSet:
    def __init__(self,stateNumb:int,itemSet:List[Item]):
        self.stateNumb=stateNumb#状态号
        self.edgesMap={}#map[int,int]#通过边到达另一个状态
        self.itemSet=itemSet#状态里的产生式项目


    def calculate_first(self, symbols: str,dic: Dic, first: first_set) -> Set[int]:
        first_result = set()
        for i in first.firstSet:
            if i[0]==symbols:
                first_result+=dic.string_to_num(i[1])
            else:
                 continue
        return first_result

class DFA:
    def __init__(self):
        self.startNum = 0
        self.Collection=[]#:List[LRState]
        self.yyl = YaccParser("./yacc/c99.y")#读取文法
        self.Dict = Dic("./yacc/result.txt")#读取字典
        self.first=first_set("./yacc/firstSet.txt")#读取first集


    def print_LRItems(self):
        for state in self.Collection:
            print(f"State Number: {state.stateNumb}")
            print("LR Items:")
            for item in state.LRItemsSet:
                print(f"Pposition: {item.Pposition}")
                print(f"Production: {item.production}")
                print(f"Lookahead: {item.lookahead}")
                print()
    
    def CFGToLRDFA(self):
        q=queue.Queue()
        newItem:Item
        newItemSet:ItemSet
        newItem.productionInt=0#S'->S
        newItem.lookahead.add(-88)#文法结束符号
        newItemSet.stateNumb=0
        newItemSet.itemSet.append(newItem)#仅保留内核项
        self.Collection.append(newItemSet)
        q.put(0)

        while not len(q)==0:
            x=q.queue[0]
            q.get()
            wholeSet:ItemSet
            epsilon_clousure(self.Collection[x],wholeSet)



    #def epsilon_clousure(self,LRStateSet:ItemSet,wholeLRStateSet:ItemSet):
        

myLRDFA=DFA()
myLRDFA.print_LRItems()