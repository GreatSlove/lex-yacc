# NFA.py
# Author: Furina-Focalors
# Date: 2024.05.23
from collections import defaultdict

from FiniteAutomata import *
from RegexNormalizer import EPSILON, DOT, ascii_dict

class NFA(FiniteAutomata):
    def __init__(self, states:set=None, moves=None, start_state:int=0, accepting_states:set=None, alphabet:set=None):
        super().__init__(states, moves, start_state, accepting_states, alphabet)
        self.acceptActionMap = {} # accepting_state:action

    def get_eps_closure(self, state: int)->set:
        """
        获取状态state的ε闭包
        :param state: 相应的状态
        :return: state的ε闭包
        """
        if state not in self.states:
            raise Exception("Cannot find state {} in this NFA.".format(state))
        eps_closure = set()

        # 用一个stack来记录闭包的元素变化情况。这里不能用另一个set，因为set在作为迭代变量时大小不允许改变
        stack = [state]
        while len(stack)>0:
            # 将上一轮多出来的状态加入闭包
            while len(stack)>0:
                eps_closure.add(stack.pop())
            # 对于闭包中的每个状态，将从它出发的所有空串边相连的状态加入闭包
            for s in eps_closure:
                for (to_state,character) in self.moves[s]:
                    # 这里写not in逻辑不是因为重复添加进集合，而是如果不写这个逻辑，stack会永远非空
                    # 想你了，std::unordered_set
                    if character == EPSILON and to_state not in eps_closure:
                        stack.append(to_state)
        return eps_closure


def gen_atom_nfa(char: str) -> NFA:
    """
    生成原子NFA，形如s1--char-->[s2]
    :param char: 转移边的值
    :return: 生成的NFA
    """
    start_state = gen_new_state()

    accept_states = set()
    accept_state = gen_new_state()
    accept_states.add(accept_state)

    states = set()
    states.add(start_state)
    states.add(accept_state)

    moves = defaultdict(list) # 将所有不存在的键都初始化成[]，方便使用append
    moves[start_state].append((accept_state,char))

    alphabet = set()
    if char != EPSILON: # 空串不加入字符集
        alphabet.add(char)
    return NFA(states, moves, start_state, accept_states, alphabet)

def concat_nfa(left:NFA,right:NFA)->NFA:
    """
    将两个NFA连接（·），即left --ε--> right
    :param left:
    :param right:
    :return:
    """
    # global EPSILON
    start_state = left.startState
    states = left.states.union(right.states)
    alphabet = left.alphabet.union(right.alphabet)
    # alphabet.add(EPSILON)
    # 合并两个转移边集，添加一条left终态到right初态的空串边
    moves = left.moves
    for key,value in right.moves.items():
        for edge in value: # 将每一条边依次加入
            moves[key].append(edge)
    # 在根据正则表达式生成NFA时，单个正则表达式只会有一个终态，因此它只会执行一次
    for state in left.acceptingStates:
        left_accepting = state
        moves[left_accepting].append((right.startState, EPSILON))
    # 连接方法中，用right的终态作为终态集
    accepting_states = right.acceptingStates
    return NFA(states,moves,start_state,accepting_states,alphabet)

def parallel_nfa(up:NFA,down:NFA)->NFA:
    """
    将两个NFA并列（|），即
               ε --> up --> ε
    new_start<                >new_accepting
               ε -> down -> ε
    :param up:
    :param down:
    :return:
    """
    start_state = gen_new_state()

    accepting_state = gen_new_state()
    accepting_states = set()
    accepting_states.add(accepting_state)

    alphabet = up.alphabet.union(down.alphabet)
    # alphabet.add(EPSILON)

    states = up.states.union(down.states)
    states.add(start_state)
    states.add(accepting_state)

    # 合并两个转移边集
    moves = up.moves
    for key, value in down.moves.items():
        for edge in value:  # 将每一条边依次加入
            moves[key].append(edge)
    # 添加四条空串边
    moves[start_state].append((up.startState, EPSILON))
    moves[start_state].append((down.startState, EPSILON))
    for state in up.acceptingStates:
        moves[state].append((accepting_state, EPSILON))
    for state in down.acceptingStates:
        moves[state].append((accepting_state, EPSILON))

    return NFA(states,moves,start_state,accepting_states,alphabet)

def kleene(nfa: NFA)->NFA:
    """
    构造Kleene闭包（*操作）
                     ______ε_______
                    ↓             |
    new_s1 --ε--> nfa.start --->nfa.end --ε--> new_s2
      |____________________ε_____________________↑
    :param nfa: 输入的NFA
    :return: 构造它的kleene闭包
    """
    start_state = gen_new_state()

    accepting_state = gen_new_state()
    accepting_states = set()
    accepting_states.add(accepting_state)

    # 添加空串边
    moves = nfa.moves
    moves[start_state].append((nfa.startState, EPSILON))
    moves[start_state].append((accepting_state, EPSILON))
    for state in nfa.acceptingStates:
        moves[state].append((nfa.startState, EPSILON))
        moves[state].append((accepting_state, EPSILON))

    states = nfa.states
    states.add(start_state)
    states.add(accepting_state)

    alphabet = nfa.alphabet
    # alphabet.add(EPSILON)
    return NFA(states,moves,start_state,accepting_states,alphabet)

def reg_to_nfa(regex: str, semantic_rule: str) -> NFA:
    """
    将正则表达式转化成NFA
    :param semantic_rule: 对应的语义规则
    :param regex: 正则表达式
    :return: 生成的NFA
    """
    nfa_stack = []
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
        if cur_char == '|': # 取栈顶两项并列
            up = nfa_stack.pop()
            down = nfa_stack.pop()
            result = parallel_nfa(up, down)
            nfa_stack.append(result)
        elif cur_char == DOT:
            right = nfa_stack.pop() # 注意出栈顺序和后缀表达式的顺序是反的
            left = nfa_stack.pop()
            result = concat_nfa(left, right)
            nfa_stack.append(result)
        elif cur_char == '*':
            nfa = nfa_stack.pop()
            result = kleene(nfa)
            nfa_stack.append(result)
        elif cur_char in [EPSILON, "'"]:
            nfa = gen_atom_nfa(cur_char)
            nfa_stack.append(nfa)
        else: # 普通或转义字符
            nfa = gen_atom_nfa(ascii_dict[cur_char])
            nfa_stack.append(nfa)
        i += 1
    result = nfa_stack.pop() # 栈顶是最终结果
    # 设置语义动作
    for accepting_state in result.acceptingStates: # 一定只有一个终态
        result.acceptActionMap[accepting_state] = semantic_rule
    return result


def merge_nfa(nfas:[])->NFA:
    """
    合并每个regex转换得到的NFA为一个NFA
    :param nfas:
    :return:
    """
    start_state = gen_new_state()
    accepting = gen_new_state()
    moves = defaultdict(list)

    accepting_states = set()
    accepting_states.add(accepting)

    states = set()
    states.add(start_state)
    states.add(accepting)

    alphabet = set()
    accept_actions = {}

    for nfa in nfas:
        # 合并状态集、字母表和终态集，合并接收态语义动作集
        states = states.union(nfa.states)
        alphabet = alphabet.union(nfa.alphabet)
        accepting_states = accepting_states.union(nfa.acceptingStates)
        accept_actions.update(nfa.acceptActionMap)
        # 合并动作集，这里只能用append方法，update会直接替换
        for from_state,to_states in nfa.moves.items():
            for to_state in to_states:
                moves[from_state].append(to_state)
        # 添加一条新初始状态到该NFA初始状态的空串边
        moves[start_state].append((nfa.startState, EPSILON))
        # 终态不用管，它们需要和语义动作一一对应

    result = NFA(states,moves,start_state,accepting_states,alphabet)
    result.acceptActionMap = accept_actions
    return result