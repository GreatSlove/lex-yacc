# FiniteAutomata.py
# Author: Furina-Focalors
# Date: 2024.05.23

NEXT_STATE_IDENTIFIER = 1

def gen_new_state():
    global NEXT_STATE_IDENTIFIER
    NEXT_STATE_IDENTIFIER += 1
    return NEXT_STATE_IDENTIFIER-1

class FiniteAutomata:
    """
    有限自动机
    由标准五元组定义
    """
    def __init__(self, states:set=None, moves=None, start_state:int=0, accepting_states:set=None, alphabet:set=None):
        self.states: set = states # 状态集
        self.moves: [] = moves # 状态转移边(fromState, toState, char)
        self.startState: int = start_state # 初态
        self.acceptingStates: set = accepting_states # 终态集
        self.alphabet: set = alphabet # 字母表

    def print(self):
        print('states: ', self.states)
        print('moves: ', self.moves)
        print('startState: ', self.startState)
        print('acceptingStates: ', self.acceptingStates)
        print('alphabet: ', self.alphabet)