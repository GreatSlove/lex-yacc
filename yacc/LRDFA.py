from typing import List, Tuple,Set
from yaccParser import *
from init_Dic import *
from init_first import *
import queue

class LRItem:
    def __init__(self,production:Tuple[str,List[str]],lookahead:Set[int]):
        self.Pposition=0#点的位置
        self.production=production#产生式
        self.lookahead=lookahead#向前搜索符


class LRState:
    def __init__(self,stateNumb:int,LRItemsSet:Set[LRItem]):
        self.stateNumb=stateNumb#状态号
        self.edgesMap={}#Tuple[int,int]#通过边到达另一个状态
        self.LRItemsSet=LRItemsSet#状态里的产生式项目

    def state_internal_extension(self, yyl: YaccParser, dic: Dic, first: first_set):
        q = queue.Queue()
        for item in self.LRItemsSet:
            q.put(item)
        while not q.empty():
            LRItem_tem=q.get()
            if(LRItem_tem.Pposition>len(LRItem_tem.production[1])):
                continue
            sym=LRItem_tem.production[1][LRItem_tem.Pposition]
            if(dic.string_to_num(sym)<0):
                continue
            B=LRItem_tem.production[0]
            if len(LRItem_tem.production[1])>LRItem_tem.Pposition+1:
                print(LRItem_tem.Pposition)
                print(len(LRItem_tem.production[1]))
                predict_set=self.calculate_first(LRItem_tem.production[1][LRItem_tem.Pposition+1],dic,first)
            else:
                predict_set=LRItem_tem.lookahead
            frontB=[]
            for Tup in yyl.producer_list:
                if B==Tup[0]:
                    frontB.append((B,Tup[1]))
                    for lin in frontB:
                        print(lin[0]+lin[1])
            for p in frontB:
                    new_LRItem = LRItem(production=p, lookahead=predict_set)
                    if new_LRItem not in self.LRItemsSet:
                        self.LRItemsSet.add(new_LRItem)
                        q.put(new_LRItem)

                
        

    def calculate_lookaheads(self, item: LRItem, beta: List[str], first: first_set) -> Set[int]:
        lookaheads = set()
        if item.Pposition + 1 < len(item.production[1]):
            beta = item.production[1][item.Pposition + 1:] + beta
            first_beta = self.calculate_first(beta, first)
            if '' in first_beta:  # ε in FIRST(beta)
                first_beta.remove('')
                first_beta.add(item.lookahead)
            lookaheads.update(first_beta)
        else:
            lookaheads.add(item.lookahead)
        return lookaheads

    def calculate_first(self, symbols: str,dic: Dic, first: first_set) -> Set[int]:
        first_result = set()
        for i in first.firstSet:
            if i[0]==symbols:
                first_result+=dic.string_to_num(i[1])
            else:
                 continue
        return first_result

class LRDFA:
    def __init__(self):
        self.startNum = 0
        self.LRStateSet=[]#:List[LRState]
        self.yyl = YaccParser("./yacc/c99.y")#读取文法
        self.Dict = Dic("./yacc/result.txt")#读取字典
        self.first=first_set("./yacc/firstSet.txt")#读取first集

    def init_state_0(self):#设置拓广文法
        state_0 = LRState(stateNumb=0, LRItemsSet=set())  # 创建状态0
        item_0 = LRItem(production=("start",["translation_unit"]), lookahead=-88)  # 创建LR项
        state_0.LRItemsSet.add(item_0)  # 将LR项添加到状态0的LR项集合中
        self.LRStateSet.append(state_0)  # 将状态0添加到LRDFA的LRStateSet列表中
        state_0.state_internal_extension(self.yyl,self.Dict,self.first)


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