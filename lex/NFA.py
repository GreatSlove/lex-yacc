# NFA.py
# Author: Furina-Focalors
# Date: 2024.05.23

from .FiniteAutomata import *
from .RegexNormalizer import EPSILON, DOT, ascii_dict

class NFA(FiniteAutomata):
    def __init__(self, states:set=None, moves=None, start_state:int=0, accepting_states:set=None, alphabet:set=None):
        super().__init__(states, moves, start_state, accepting_states, alphabet)
        self.acceptActionMap = {} # accepting_state:action


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

    moves = [(start_state,accept_state,char)]

    alphabet = set()
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
    alphabet.add(EPSILON)
    moves:[] = left.moves + right.moves # 合并两个转移边集，添加一条left终态到right初态的空串边
    # 在根据正则表达式生成NFA时，单个正则表达式只会有一个终态，因此它只会执行一次
    for state in left.acceptingStates:
        left_accepting = state
        moves.append((left_accepting, right.startState, EPSILON))
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
    alphabet.add(EPSILON)

    states = up.states.union(down.states)
    states.add(start_state)
    states.add(accepting_state)

    moves: [] = up.moves + down.moves
    # 添加四条空串边
    moves.append((start_state, up.startState, EPSILON))
    moves.append((start_state, down.startState, EPSILON))
    for state in up.acceptingStates:
        moves.append((state, accepting_state, EPSILON))
    for state in down.acceptingStates:
        moves.append((state, accepting_state, EPSILON))

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
    moves.append((start_state, nfa.startState, EPSILON))
    moves.append((start_state, accepting_state, EPSILON))
    for state in nfa.acceptingStates:
        moves.append((state, nfa.startState, EPSILON))
        moves.append((state, accepting_state, EPSILON))

    states = nfa.states
    states.add(start_state)
    states.add(accepting_state)

    alphabet = nfa.alphabet
    alphabet.add(EPSILON)
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