# DFA.py
# Author: Furina-Focalors
# Date: 2024.05.26
from collections import defaultdict

from lex import NFA
from lex.FiniteAutomata import FiniteAutomata
from lex.NFA import gen_new_state


class DFA(FiniteAutomata):
    def __init__(self, states:set=None, moves=None, start_state:int=0, accepting_states:set=None, alphabet:set=None):
        super().__init__(states, moves, start_state, accepting_states, alphabet)
        self.acceptActionMap = {} # accepting_state:action

def nfa_to_dfa(nfa: NFA)->DFA:
    """
    将NFA转化成DFA
    :param nfa:
    :return:
    """
    states_map = {} # 新状态和它对应的闭包，用来判断某个状态是否已经存在
    to_process = [] # 待处理的状态
    # 将原来初态的闭包作为第一个待处理的状态
    start_closure = nfa.get_eps_closure(nfa.startState)
    new_start_state = gen_new_state() # 新的初始状态
    states_map[new_start_state] = start_closure
    to_process.append(new_start_state)

    new_moves = defaultdict(list)
    new_states = set()
    new_states.add(new_start_state)
    new_accepting_states = set()
    new_accept_action_map = {}

    # 检查新的初始状态是否同时也是终态
    for state in start_closure:
        if state in nfa.acceptingStates:
            new_accepting_states.add(new_start_state)
            # 规定它的语义动作。如果这个集合中包含了多个终态，取.l文件中靠上的语义，因此执行完之后需要break
            new_accept_action_map[new_start_state] = nfa.acceptActionMap[state]
            break

    for cur_state in to_process: # 对于每个待处理的状态集（通过求闭包得到）对应的新状态
        closure = states_map[cur_state] # 对应的状态集

        # print(closure)

        for character in nfa.alphabet: # 读入一个字符
            result = set()
            for state_ in closure: # 将闭包内每个状态经过读入character转移得到的状态加入新集合
                for to_state, c in nfa.moves[state_]:
                    if c == character:
                        result.add(to_state)

            # print('before eps-closure, char={}, result={}'.format(character,result))
            # 求result的ε闭包
            temp = set()
            for item in result:
                temp = temp.union(nfa.get_eps_closure(item))
            result = temp

            # print('char={},result={}'.format(character,result))

            if not result: # 如果这个状态不能读入字符character，不做任何操作
                continue
            # 查找result在states_map中对应的状态。在这里执行可以减少重复执行O(n)检索。
            result_state = None
            for target, corresponding_closure in states_map.items():
                if corresponding_closure == result:
                    result_state = target
                    break
            # 如果result不存在于states_map中，表示生成了一个新状态，需要将它加入新的状态集，加入states_map，同时添加一条新的move
            if result_state is None:
                new_state = gen_new_state()
                # 将result加入待处理的队列
                to_process.append(new_state)
                states_map[new_state] = result
                new_states.add(new_state)
                # 当前闭包对应的新状态，读入character，到现在生成的这个新状态
                new_moves[cur_state].append((new_state, character))
                # 检查其中是否有终态，原理同新初态检查
                for s in result:
                    if s in nfa.acceptingStates:
                        new_accepting_states.add(new_state)
                        new_accept_action_map[new_state] = nfa.acceptActionMap[s]
                        break
            else: # 如果是已有的状态，也要添加相应的move
                new_moves[cur_state].append((result_state,character))

    # 字符集不需要重新计算
    return DFA(new_states,new_moves,new_start_state,new_accepting_states,nfa.alphabet)