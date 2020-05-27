from collections import defaultdict
from graphviz import Digraph, render

KLEENE_CLOSURE = '*'
ALTERNATION = '|'
CONCATENATION = '·'
LEFT_PARENTHESES, RIGHT_PARENTHESES = '(', ')'
ALPHABET = [chr(i) for i in range(ord('A'), ord('Z') + 1)] + \
    [chr(i) for i in range(ord('a'), ord('z') + 1)] + \
    [chr(i) for i in range(ord('0'), ord('9') + 1)]
EPSILON = 'ε'

class FA:

    def __init__(self, symbol = set([])):
        self.states = set()
        self.symbol = symbol    # Input symbol table
        self.transitions = defaultdict(defaultdict)
        self.initial_state = None
        self.accepting_states = []

    def set_initial_state(self, state):
        self.initial_state = state
        self.states.add(state)

    def add_accepting_states(self, state):
        if isinstance(state, int):
            state = [state]
        for s in state:
            if s not in self.accepting_states:
                self.accepting_states.append(s)

    def addTransition(self, fromstate, tostate, inputch):   # add only one 仅添加一条映射关系
        if isinstance(inputch, str):
            inputch = set([inputch])
        self.states.add(fromstate)
        self.states.add(tostate)
        if fromstate in self.transitions and tostate in self.transitions[fromstate]:
            self.transitions[fromstate][tostate] = \
            self.transitions[fromstate][tostate].union(inputch)
        else:
            self.transitions[fromstate][tostate] = inputch

    def addTransition_dict(self, transitions):  # add dict to dict 将一个字典的内容添加到另一个字典
        for fromstate, tostates in transitions.items():
            for state in tostates:
                self.addTransition(fromstate, state, tostates[state])

    def newBuildFromNumber(self, startnum):
    # change the states' representing number to start with the given startnum
    # 改变各状态的表示数字，使之从 startnum 开始
        translations = {}
        for i in self.states:
            translations[i] = startnum
            startnum += 1
        rebuild = FA(self.symbol)
        rebuild.set_initial_state(translations[self.initial_state])
        rebuild.add_accepting_states(translations[self.accepting_states[0]])
        # 多个终结状态不方便合并操作, 同时提供的合并操作可以保证只产生一个终结状态
        for fromstate, tostates in self.transitions.items():
            for state in tostates:
                rebuild.addTransition(translations[fromstate], translations[state], tostates[state])
        return [rebuild, startnum]

    def newBuildFromEqualStates(self, equivalent, pos):
        # change states' number after merging
        # 在最小化合并状态后修改状态的表示数字
        rebuild = FA(self.symbol)
        for fromstate, tostates in self.transitions.items():
            for state in tostates:
                rebuild.addTransition(pos[fromstate], pos[state], tostates[state])
        rebuild.set_initial_state(pos[self.initial_state])
        for s in self.accepting_states:
            rebuild.add_accepting_states(pos[s])
        return rebuild

    def getEpsilonClosure(self, findstate):
        allstates = set()
        states = [findstate]
        while len(states):
            state = states.pop()
            allstates.add(state)
            if state in self.transitions:
                for tos in self.transitions[state]:
                    if EPSILON in self.transitions[state][tos] and \
                        tos not in allstates:
                        states.append(tos)
        return allstates

    def getMove(self, state, skey):
        if isinstance(state, int):
            state = [state]
        trstates = set()
        for st in state:
            if st in self.transitions:
                for tns in self.transitions[st]:
                    if skey in self.transitions[st][tns]:
                        trstates.add(tns)
        return trstates

    def display(self, fname, pname):
        fa = Digraph(pname, filename = fname, format = 'png')
        fa.attr(rankdir='LR')

        fa.attr('node', shape = 'doublecircle')
        for fst in self.accepting_states:
            fa.node('s' + str(fst))

        fa.attr('node', shape = 'circle')
        for fromstate, tostates in self.transitions.items():
            for state in tostates:
                tmp = ''
                for s in tostates[state]:
                    tmp += s + ','
                fa.edge('s' + str(fromstate), 's' + str(state), label = tmp[:-1])

        fa.attr('node', shape = 'point')
        fa.edge('', 's' + str(self.initial_state))

        fa.view(directory="./example/img")
