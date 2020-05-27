# source: https://github.com/YanhuiJessica/Finite-Automata-Machine
# sequence diagram: http://www.plantuml.com/plantuml/umla/nPRDRXiX483lF0MtsAlMXnmjfKfLjxVqKAaFW9U9ZOHX1QpLzEdBO4H9m8LLssGF6o_p_mqCkRUE6JUV925iTDhGxnOCmHTz_u4-CA7ebffPqL4hgoLGDas4u3hAly41Vjn-_V9nIuKIRcNmUusUn9av-2qdXFedVRwmtSz2SlzhjGvgryobrXCTZpuKjI0VDo5Qa0GhwQAGoUd8zk2Iw8-ncHMZTMOU7OQFJpqDckHLh_uTEIH7fJDV3Aqyw25FZCRCgih58eV2Vo79V0SVIGsa1IHtTqUbKD153HMxeRqgDSmiqwuJ8cr6IQF6YUk-pUNrEYar8VqpHY6h5g4seEh-mM52EyZGRL3jPFEw6mWJQ-BftpwWECd_9fKoCCwqOL2FR1W8gJA_teXo97kFNDX9iYUSh9r3EJUBE6ygXYsy5sSxSJ1iEjQxaqoZLW4yhWTCuJxQKezcSpXl9dKe6r0wkwdIglPp2Ur4sd_TxlBDbxIZ16CbhSmWNdYxTE5L3LyO1xkuEpO7S9ydAwHMdwIsiu4LeWbNkNyvM7Trw5bAJCfWQgyGgkMK5n_awPQMe5ONTrdNdr_X73D-Eksrp3IQPJ_eCrmyl_D-5X_uicvdOjdz1puLOh4EAQnRELEhDl_Nn5Ab7Uh3U6bPeRcywVLmJGuBzq4_c7pcjTRYT_fD6bisSYdoZLEJXwbvFKKEnI6hB0NLydp7WTX_OCjH-bOZa_UEpBzdLt8x-I9EuYSqPsEjezxOVmz3Pwn8-cBL3bZsf-pDV-mBebdMccovplyU59zFyXS0
# class diagram: http://www.plantuml.com/plantuml/uml/TL6xijem4Etz5IgL6MWeKq42xi9aGlgCRAt9JlGmqeh4m_3laInXH78l3TQUe_FGRZq9Hq6hfbV2UzRksArXyHVd19vzP1ue3oRTMLKDRWE2adTomdWaj2Qn9GmYA9BO4w--Fpmq7St2aOacomneX5hS5FfY1tHAT3v3-RwGiatiVsRVbmHyS5RFu8gHBHzena3zppVeF-QOLO7CCV3xKq0bsoXs3Be3n-Va9kZ_2OTB4Eeqn-Tm2NWL2Wojs6YBsXdeC7fKrdnMrWS7F3QMfK4XVB5Nu2Mk_mLJ1YJwKOc93qRe28pnBrwvDsLLt-0CVpR7PMCkdTD-oB4SSn3nsEvgiKZdMVsM_B2_H_kl3gr3chWTNx5EUEoZNkY9ByzO4nGQABXOiUuLb9RUnTA3Fi2CTEb5SxobOZnkzaj1MVhaTXfDXAf1QRXF4lKW4tdbaevcABuEdZicy6LpnG4rUiY9eerThv-l_XYKZ4sp1IE3Ldy1
from collections import defaultdict
from graphviz import Digraph, render

from constants import *

class FA:

    def __init__(self, symbol = set(list())):
        self.states = set()
        self.symbol = symbol    # Input symbol table
        self.transitions = defaultdict(defaultdict)
        self.initial_state = None
        self.accepting_states = list()

    def set_initial_state(self, state):
        self.initial_state = state
        self.states.add(state)

    def add_accepting_states(self, state):
        if isinstance(state, int):
            state = [state]
        for s in state:
            if s not in self.accepting_states:
                self.accepting_states.append(s)

    def add_transition(self, fromstate, tostate, inputch):   
        """
        Add only one mapping transition
        """
        if isinstance(inputch, str):
            inputch = set([inputch])
        self.states.add(fromstate)
        self.states.add(tostate)
        if fromstate in self.transitions and tostate in self.transitions[fromstate]:
            self.transitions[fromstate][tostate] = self.transitions[fromstate][tostate].union(inputch)
        else:
            self.transitions[fromstate][tostate] = inputch

    def add_transition_dict(self, transitions): 
        """
        Add the contents of one dictionary to another dictionary
        """
        for fromstate, tostates in transitions.items():
            for state in tostates:
                self.add_transition(fromstate, state, tostates[state])

    def rebuild_from_number(self, start_number):
        """
        Reset the representation number of each state as start from the given start_number
        """
        translations = {}
        for state in self.states:
            translations[state] = start_number
            start_number += 1
        rebuild = FA(self.symbol)
        rebuild.set_initial_state(translations[self.initial_state])
        rebuild.add_accepting_states(translations[self.accepting_states[0]])
        """
        Multiple accepting states are not easy to merge, and the provided merge 
        operation ensures that only one accepting state is generated
        """
        for from_state, to_states in self.transitions.items():
            for state in to_states:
                rebuild.add_transition(translations[from_state], translations[state], to_states[state])
        return rebuild, start_number

    def rebuild_from_equal_states(self, equivalent, position):
        # Reset states' number after merging
        """
        Reset the state representation number after minimizing the merged state
        """
        rebuilt = FA(self.symbol)
        for from_state, to_states in self.transitions.items():
            for state in to_states:
                rebuilt.add_transition(position[from_state], position[state], to_states[state])
        rebuilt.set_initial_state(position[self.initial_state])
        for state in self.accepting_states:
            rebuilt.add_accepting_states(position[state])
        return rebuilt

    def get_epsilon_closure(self, find_state):
        all_states = set()
        states = [find_state]
        while len(states):
            from_state = states.pop()
            all_states.add(from_state)
            if from_state in self.transitions:
                for to_state in self.transitions[from_state]:
                    if EPSILON in self.transitions[from_state][to_state] and to_state not in all_states:
                        states.append(to_state)
        return all_states

    def get_move(self, state, skey):
        if isinstance(state, int):
            state = [state]
        transition_states = set()
        for s in state:
            if s in self.transitions:
                for transition in self.transitions[s]:
                    if skey in self.transitions[s][transition]:
                        transition_states.add(transition)
        return transition_states

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

        fa.view(directory="./img")

class Regex2NFA:

    def __init__(self, regex):
        self.regex = regex
        self.build_NFA()

    def display_NFA(self):
        self.nfa.display('nfa.gv', 'nondeterministic_finite_automaton')

    @staticmethod
    def get_precedence(operator):
        if operator == ALTERNATION:
            return 1
        elif operator == CONCATENATION:
            return 2
        elif operator == KLEENE_CLOSURE:
            return 3
        else:       # left bracket 左括号
            return 0

    @staticmethod
    def get_symbol_template(symbol):  
        """
        symbol -> NFA
        """
        from_state = 1
        to_state = 2
        symbol_template = FA(set([symbol]))
        symbol_template.set_initial_state(from_state)
        symbol_template.add_accepting_states(to_state)
        symbol_template.add_transition(from_state, to_state, symbol)
        return symbol_template

    @staticmethod
    def get_alternation_template(a, b):  
        """
        a | b -> NFA
        """
        a, m1 = a.rebuild_from_number(2)
        b, m2 = b.rebuild_from_number(m1)
        from_state = 1
        to_state = m2
        alternation_template = FA(a.symbol.union(b.symbol))
        alternation_template.set_initial_state(from_state)
        alternation_template.add_accepting_states(to_state)
        alternation_template.add_transition(alternation_template.initial_state, a.initial_state, EPSILON)
        alternation_template.add_transition(alternation_template.initial_state, b.initial_state, EPSILON)
        alternation_template.add_transition(a.accepting_states[0], alternation_template.accepting_states[0], EPSILON)
        alternation_template.add_transition(b.accepting_states[0], alternation_template.accepting_states[0], EPSILON)
        alternation_template.add_transition_dict(a.transitions)
        alternation_template.add_transition_dict(b.transitions)
        return alternation_template

    @staticmethod
    def get_concatenation_template(a, b):  
        """
        a · b -> NFA
        """
        a, m1 = a.rebuild_from_number(1)
        b, m2 = b.rebuild_from_number(m1)
        from_state = 1
        to_state = m2 - 1
        concatenation_template = FA(a.symbol.union(b.symbol))
        concatenation_template.set_initial_state(from_state)
        concatenation_template.add_accepting_states(to_state)
        concatenation_template.add_transition(a.accepting_states[0], b.initial_state, EPSILON)
        concatenation_template.add_transition_dict(a.transitions)
        concatenation_template.add_transition_dict(b.transitions)
        return concatenation_template

    @staticmethod
    def get_kleene_closure_template(a): 
        """
        a* -> NFA
        """
        a, m1 = a.rebuild_from_number(2)
        from_state = 1
        to_state = m1
        kleene_closure_template = FA(a.symbol)
        kleene_closure_template.set_initial_state(from_state)
        kleene_closure_template.add_accepting_states(to_state)
        kleene_closure_template.add_transition(kleene_closure_template.initial_state, a.initial_state, EPSILON)
        kleene_closure_template.add_transition(kleene_closure_template.initial_state, kleene_closure_template.accepting_states[0], EPSILON)
        kleene_closure_template.add_transition(a.accepting_states[0], kleene_closure_template.accepting_states[0], EPSILON)
        kleene_closure_template.add_transition(a.accepting_states[0], a.initial_state, EPSILON)
        kleene_closure_template.add_transition_dict(a.transitions)
        return kleene_closure_template

    #@staticmethod
    def to_postfix(self) :
        pass

    def build_NFA(self):
        tword = ''
        previous = ''
        symbol = set()

        """
        Explicitly add concatenation to the expression 
        """
        for ch in self.regex:
            if ch in ALPHABET:
                symbol.add(ch)
            if ch in ALPHABET or ch == LEFT_PARENTHESES:
                if previous != CONCATENATION and (previous in ALPHABET or previous in [KLEENE_CLOSURE, RIGHT_PARENTHESES]):
                    tword += CONCATENATION
            tword += ch
            previous = ch
        self.regex = tword

        """
        Convert infix expression to postfix expression
        """ 
        tword = ''
        stack = list()
        for ch in self.regex:
            if ch in ALPHABET:
                tword += ch
            elif ch == LEFT_PARENTHESES:
                stack.append(ch)
            elif ch == RIGHT_PARENTHESES:
                while(stack[-1] != LEFT_PARENTHESES):
                    tword += stack[-1]
                    stack.pop()
                stack.pop()    # pop left bracket
            else:
                while(len(stack) and Regex2NFA.get_precedence(stack[-1]) >= Regex2NFA.get_precedence(ch)):
                    tword += stack[-1]
                    stack.pop()
                stack.append(ch)
        while(len(stack) > 0):
            tword += stack.pop()
        self.regex = tword

        """ 
        Build ε-NFA from postfix expression
        """ 
        self.automata = list()
        for ch in self.regex:
            if ch in ALPHABET:
                self.automata.append(Regex2NFA.get_symbol_template(ch))
            elif ch == ALTERNATION:
                b = self.automata.pop()
                a = self.automata.pop()
                self.automata.append(Regex2NFA.get_alternation_template(a, b))
            elif ch == CONCATENATION:
                b = self.automata.pop()
                a = self.automata.pop()
                self.automata.append(Regex2NFA.get_concatenation_template(a, b))
            elif ch == KLEENE_CLOSURE:
                a = self.automata.pop()
                self.automata.append(Regex2NFA.get_kleene_closure_template(a))
        self.nfa = self.automata.pop()
        self.nfa.symbol = symbol

class NFA2DFA:

    def __init__(self, nfa):
        self.build_DFA(nfa)

    def display_DFA(self):
        self.dfa.display('dfa.gv', 'deterministic_finite_automaton')

    def display_minDFA(self):
        self.minDFA.display('mindfa.gv', 'minimal_deterministic_finite_automaton')

    def build_DFA(self, nfa): 
        """
        Subset construction
        """
        all_states = dict()  # visited subset
        epsilon_closure = dict()   # every state's ε-closure
        state1 = nfa.get_epsilon_closure(nfa.initial_state)
        epsilon_closure[nfa.initial_state] = state1
        number_of_subset = 1 # the number of subset, dfa state id
        dfa = FA(nfa.symbol)
        dfa.set_initial_state(number_of_subset)
        states = [[state1, dfa.initial_state]] # unvisit
        all_states[number_of_subset] = state1
        number_of_subset += 1
        while len(states):
            state, fromindex = states.pop()
            for ch in dfa.symbol:
                trstates = nfa.get_move(state, ch)
                for s in list(trstates):    # 转化为list, 相当于使用了一个临时变量
                    if s not in epsilon_closure:
                        epsilon_closure[s] = nfa.get_epsilon_closure(s)
                    trstates = trstates.union(epsilon_closure[s])
                if len(trstates):
                    if trstates not in all_states.values():
                        states.append([trstates, number_of_subset])
                        all_states[number_of_subset] = trstates
                        toindex = number_of_subset
                        number_of_subset += 1
                    else:
                        toindex = [k for k, v in all_states.items() if v  ==  trstates][0]
                    dfa.add_transition(fromindex, toindex, ch)
            for value, state in all_states.items():
                if nfa.accepting_states[0] in state:
                    dfa.add_accepting_states(value)
        self.dfa = dfa

    @staticmethod
    def reNumber(states, pos):  # renumber the sets' number begin from 1
        cnt = 1
        change = dict()
        for st in states:
            if pos[st] not in change:
                change[pos[st]] = cnt
                cnt += 1
            pos[st] = change[pos[st]]

    def minimise(self): # segmentation 分割法, 生成新的状态集合
        states = list(self.dfa.states)
        tostate = dict(set()) # Move(every state, every symbol)

        # initialization 预处理出每个状态经一个输入符号可以到达的下一个状态
        for st in states:
            for sy in self.dfa.symbol:
                if st in tostate:
                    if sy in tostate[st]:
                        tostate[st][sy] = tostate[st][sy].union(self.dfa.get_move(st, sy))
                    else:
                        tostate[st][sy] = self.dfa.get_move(st, sy)
                else:
                    tostate[st] = {sy : self.dfa.get_move(st, sy)}
                if len(tostate[st][sy]):
                    tostate[st][sy] = tostate[st][sy].pop()
                else:
                    tostate[st][sy] = 0

        equal = dict()  # state sets 不同分组的状态集合
        pos = dict()    # record the set which state belongs to 记录状态对应的分组

        # initialization 2 sets, nonterminal states and final states
        equal = {1: set(), 2: set()}
        for st in states:
            if st not in self.dfa.accepting_states:
                equal[1] = equal[1].union(set([st]))
                pos[st] = 1
        for fst in self.dfa.accepting_states:
            equal[2] = equal[2].union(set([fst]))
            pos[fst] = 2

        unchecked = list()
        cnt = 3 # the number of sets
        unchecked.extend([[equal[1], 1], [equal[2], 2]])
        while len(unchecked):
            [equalst, id] = unchecked.pop()
            for sy in self.dfa.symbol:
                diff = dict()
                for st in equalst:
                    if tostate[st][sy] == 0:
                        if 0 in diff:
                            diff[0].add(st)
                        else:
                            diff[0] = set([st])
                    else:
                        if pos[tostate[st][sy]] in diff:
                            diff[pos[tostate[st][sy]]].add(st)
                        else:
                            diff[pos[tostate[st][sy]]] = set([st])
                if len(diff) > 1:
                    for k, v in diff.items():
                        if k:
                            for i in v:
                                equal[id].remove(i)
                                if cnt in equal:
                                    equal[cnt] = equal[cnt].union(set([i]))
                                else:
                                    equal[cnt] = set([i])
                            if len(equal[id]) == 0:
                                equal.pop(id)
                            for i in v:
                                pos[i] = cnt
                            unchecked.append([equal[cnt], cnt])
                            cnt += 1
                    break
        if len(equal) == len(states):
            self.minDFA = self.dfa
        else:
            NFA2DFA.reNumber(states, pos)
            self.minDFA = self.dfa.rebuild_from_equal_states(equal, pos)

"""    def Analysis(self, string):
        string = string.replace('@', epsilon)
        curst = self.dfa.initial_state
        for ch in string:
            if ch == epsilon:
                continue
            st = list(self.dfa.get_move(curst, ch))
            if len(st) == 0:
                return False
            curst = st[0]
        if curst in self.dfa.accepting_states:
            return True
        return False"""

if __name__ == '__main__':

    # using example
    #regex = input('Please input the regex: ')
    regex = "(a*|b*)*"
    a = Regex2NFA(regex)
    a.display_NFA()

    b = NFA2DFA(a.nfa)
    b.display_DFA()
    b.minimise()
    b.display_minDFA()

    """while True:
        try:
            s = input('Please input a word to analysis (take @ as ε): ')
            if b.Analysis(s):
                print('Accepted')
            else:
                print('Unaccepted')
        except EOFError:
            break"""