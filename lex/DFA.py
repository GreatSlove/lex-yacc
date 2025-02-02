# DFA.py
# Author: Furina-Focalors
# Date: 2024.05.26
from collections import defaultdict

from NFA import NFA
from FiniteAutomata import FiniteAutomata
from NFA import gen_new_state


class DFA(FiniteAutomata):
    def __init__(self, states:set=None, moves=None, start_state:int=0, accepting_states:set=None, alphabet:set=None):
        super().__init__(states, moves, start_state, accepting_states, alphabet)
        self.acceptActionMap = {} # accepting_state:action

    def __eq__(self, other):
        return (
            self.states == other.states
            and self.moves == other.moves
            and self.startState == other.startState
            and self.acceptingStates == other.acceptingStates
            and self.alphabet == other.alphabet
            and self.acceptActionMap == other.acceptActionMap
        )

    def write_to_file(self, filename: str):
        """
        将DFA写入文件
        :param filename:
        :return:
        """
        with open(filename, 'wb') as file:
            # 状态
            for state in self.states:
                content = '{}NEXT'.format(state)
                file.write(content.encode('utf-8'))
            # moves
            file.write(b'SEPARATE')
            for from_state, moves_list in self.moves.items():
                for to_state, character in moves_list:
                    content = '{}FURINA{}FURINA{}NEXT'.format(from_state, to_state, character)
                    file.write(content.encode('utf-8'))
            # 初态
            content = 'SEPARATE{}SEPARATE'.format(self.startState)
            file.write(content.encode('utf-8'))
            # 终态集
            for state in self.acceptingStates:
                content = '{}NEXT'.format(state)
                file.write(content.encode('utf-8'))
            # 字母表
            file.write(b'SEPARATE')
            for character in self.alphabet:
                content = character + 'NEXT'
                file.write(content.encode('utf-8'))
            # 语义动作
            file.write(b'SEPARATE')
            for state, action in self.acceptActionMap.items():
                content = '{}FURINA{}NEXT'.format(state, action)
                file.write(content.encode('utf-8'))

    def read_from_file(self, filename):
        """
        从文件读取DFA
        :param filename:
        :return:
        """
        with open(filename, 'rb') as file:
            content = file.read()
            content = content.decode('utf-8')
            parts = content.split('SEPARATE')
            # assert(len(parts)==6)
            # 按照写入顺序分割内容
            states = parts[0]
            moves = parts[1]
            start_state = parts[2]
            accepting_states = parts[3]
            alphabet = parts[4]
            accept_action_map = parts[5]
            # 分割每个部分的内容
            # 状态集
            states = states.split('NEXT')
            states = states[:len(states) - 1]  # 最后一个是空，写入产生的
            result_states = set()
            for state in states:
                result_states.add(int(state))
            # moves
            moves = moves.split('NEXT')
            moves = moves[:len(moves) - 1]
            result_moves = defaultdict(list)
            for item in moves:
                items = item.split('FURINA')
                result_moves[int(items[0])].append((int(items[1]), items[2]))
            # 初态
            result_start_state = int(start_state)
            # 终态集
            accepting_states = accepting_states.split('NEXT')
            accepting_states = accepting_states[:len(accepting_states) - 1]
            result_accepting_state = set()
            for state in accepting_states:
                result_accepting_state.add(int(state))
            # 字母表
            alphabet = alphabet.split('NEXT')
            alphabet = alphabet[:len(alphabet) - 1]
            result_alphabet = set()
            for character in alphabet:
                result_alphabet.add(character)
            # 语义动作
            accept_action_map = accept_action_map.split('NEXT')
            accept_action_map = accept_action_map[:len(accept_action_map) - 1]
            result_accept_action_map = {}
            for item in accept_action_map:
                items = item.split('FURINA')
                result_accept_action_map[int(items[0])] = items[1]

        self.states = result_states
        self.moves = result_moves
        self.startState = result_start_state
        self.acceptingStates = result_accepting_state
        self.alphabet = result_alphabet
        self.acceptActionMap = result_accept_action_map
    def match(self, string:str):
        """
        匹配给定的字符串
        :param string:
        :return:
        """
        cur_state = self.startState
        for i in range(len(string)):
            has_trans = False
            for next_state, rcv_char in self.moves[cur_state]:
                if rcv_char == string[i]:
                    cur_state = next_state
                    has_trans = True
                    break
            if not has_trans:
                if i!=range(len(string)-1): # 要求完整匹配
                    return None
                else:
                    break
        if cur_state not in self.acceptingStates:
            return None
        else:
            return self.acceptActionMap[cur_state]


    def minimize(self):
        """
        最小化DFA
        :return:
        """
        # 将终态和非终态分到两类中
        terminals = self.acceptingStates
        non_terminals = self.states - terminals
        terminals = list(terminals)
        non_terminals = list(non_terminals)
        partition = []
        # 建立状态到分组的索引
        state_group = {}
        for state in non_terminals:
            state_group[state] = non_terminals
        # 下一轮迭代的数组
        next_turn = []

        # 将没有任何moves的终态直接进行划分。非终态不可能没有moves
        term_has_moves = []
        for state in terminals:
            if len(self.moves[state])==0:
                # 将有相同语义动作的状态分为一组
                append_new = True
                for group in next_turn:
                    if self.acceptActionMap[state] == self.acceptActionMap[group[0]]:
                        group.append(state)
                        append_new = False
                        break
                # 没有相同，新建一组
                if append_new:
                    next_turn.append([state])
            else:
                term_has_moves.append(state)

        next_turn.append(term_has_moves)
        # 为没有moves的终态建立索引
        for group in next_turn:
            for state in group:
                state_group[state] = group
        # 为有moves的终态建立索引
        for state in term_has_moves:
            state_group[state] = term_has_moves
        # 将非终态加入待处理划分
        next_turn.append(non_terminals)

        # 生成一个新的moves字典，它的结构为from_state:[(to_group,character),...]
        modified_moves = defaultdict(list)

        while len(partition) != len(next_turn): # 不断尝试划分，直到不再有新的分组出现
            partition = next_turn
            next_turn = []

            # 按照上一轮划分完成的结果更新moves表
            modified_moves = defaultdict(list)
            for group in partition:
                # 将没有moves的状态直接放到next_turn中
                if len(self.moves[group[0]]) == 0:
                    next_turn.append(group)
                    continue

                for state in group:
                    moves_list = self.moves[state]
                    for to_state,character in moves_list:
                        modified_moves[state].append((state_group[to_state],character))

            # 将转移到不同group的状态分开
            # 由于把moves中所有的to_state换成了对应的group，因此判断两个状态在同一个group，可以检查moves是否相等
            # 但是，如果是终态，除了要检查moves是否相同，还要检查action是否相同，action不同的状态不能当作同一组对待
            for from_state in list(modified_moves.keys()):
                is_in_group = False
                for g in next_turn:
                    # 如果一个是终态一个不是终态，不能合并，跳过
                    if (
                        from_state in self.acceptingStates and g[0] not in self.acceptingStates
                        or from_state not in self.acceptingStates and g[0] in self.acceptingStates
                    ):
                        continue
                    # 判断from_state和已有组g中的所有状态moves是否相同
                    has_same_moves = True
                    for s in g:
                        if modified_moves[from_state] != modified_moves[s]:
                            has_same_moves = False
                            break
                    if has_same_moves:
                        # 如果是终态，额外判断action是否相同
                        if from_state in self.acceptingStates:
                            can_merge = True
                            for s in g:
                                if self.acceptActionMap[s] != self.acceptActionMap[from_state]:
                                    # 如果它和组内任何一个状态的语义动作不同，则不能放进这个组
                                    can_merge = False
                                    break
                            if not can_merge: # 不能合，检查下一组是否满足条件
                                continue
                        if from_state not in g: # list要保证不重复
                            g.append(from_state)
                        is_in_group = True
                        break
                if not is_in_group: # 如果没有和它moves相同的组，说明它属于一个新的组，增加一组
                    next_turn.append([from_state])
            # 按next_turn更新state_group索引关系
            for g in next_turn:
                for s in g:
                    state_group[s] = g

        # 划分完成后，partition即包含每个分组及其中的状态；modified_moves包含了每个状态对应的moves
        # 选择代表状态，构造DFA的五元组和语义动作
        new_start_state = -1
        new_accepting_states = set()
        new_states = set()
        new_accept_action_map = {}
        new_moves = defaultdict(list)
        temp_new_moves = defaultdict(set) # 可能会有重复添加动作，使用set来去掉它们from_state:set((to_state,char))
        for group in partition: # 选择每个group的首个元素作为该group的代表元素
            new_states.add(group[0])
            if self.startState in group: # 设置初态
                new_start_state = group[0]
            # 由于初始划分将终态和非终态分开，因此判断任何一个元素是否属于终态集即可
            if group[0] in self.acceptingStates:
                new_accepting_states.add(group[0])
                # 不需要选择最小，因为划分时已经保证了每一项语义动作都相同
                new_accept_action_map[group[0]] = self.acceptActionMap[group[0]]
            # 构造moves
            for to_group,character in modified_moves[group[0]]:
                temp_new_moves[group[0]].add((to_group[0],character))
        if new_start_state == -1:
            raise Exception('Start state not found.')
        # 将set转换为list
        for key,value in temp_new_moves.items():
            new_moves[key] = list(value)
        self.startState = new_start_state
        self.moves = new_moves
        self.states = new_states
        self.acceptingStates = new_accepting_states
        self.acceptActionMap = new_accept_action_map
        # 不需要更新字母表


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
    tmp_accepting = set() # 需要选择.l文件中靠前的语义动作，即编号最小的状态对应的语义动作
    for state in start_closure:
        if state in nfa.acceptingStates:
            tmp_accepting.add(state)
            new_accepting_states.add(new_start_state)
    if len(tmp_accepting)>0:
        # 规定它的语义动作。如果这个集合中包含了多个终态，取.l文件中靠上的语义
        new_accept_action_map[new_start_state] = nfa.acceptActionMap[min(tmp_accepting)]

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
                # 检查其中是否有终态，并指定语义动作
                tmp_accepting = set()
                for s in result:
                    if s in nfa.acceptingStates:
                        tmp_accepting.add(s)
                        new_accepting_states.add(new_state)
                if len(tmp_accepting)>0:
                    new_accept_action_map[new_state] = nfa.acceptActionMap[min(tmp_accepting)]
            else: # 如果是已有的状态，也要添加相应的move
                new_moves[cur_state].append((result_state,character))

    # 字符集不需要重新计算
    result = DFA(new_states,new_moves,new_start_state,new_accepting_states,nfa.alphabet)
    result.acceptActionMap = new_accept_action_map
    return result