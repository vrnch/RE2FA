# source: https://github.com/YanhuiJessica/Finite-Automata-Machine
# sequence diagram: http://www.plantuml.com/plantuml/umla/nPRDRXiX483lF0MtsAlMXnmjfKfLjxVqKAaFW9U9ZOHX1QpLzEdBO4H9m8LLssGF6o_p_mqCkRUE6JUV925iTDhGxnOCmHTz_u4-CA7ebffPqL4hgoLGDas4u3hAly41Vjn-_V9nIuKIRcNmUusUn9av-2qdXFedVRwmtSz2SlzhjGvgryobrXCTZpuKjI0VDo5Qa0GhwQAGoUd8zk2Iw8-ncHMZTMOU7OQFJpqDckHLh_uTEIH7fJDV3Aqyw25FZCRCgih58eV2Vo79V0SVIGsa1IHtTqUbKD153HMxeRqgDSmiqwuJ8cr6IQF6YUk-pUNrEYar8VqpHY6h5g4seEh-mM52EyZGRL3jPFEw6mWJQ-BftpwWECd_9fKoCCwqOL2FR1W8gJA_teXo97kFNDX9iYUSh9r3EJUBE6ygXYsy5sSxSJ1iEjQxaqoZLW4yhWTCuJxQKezcSpXl9dKe6r0wkwdIglPp2Ur4sd_TxlBDbxIZ16CbhSmWNdYxTE5L3LyO1xkuEpO7S9ydAwHMdwIsiu4LeWbNkNyvM7Trw5bAJCfWQgyGgkMK5n_awPQMe5ONTrdNdr_X73D-Eksrp3IQPJ_eCrmyl_D-5X_uicvdOjdz1puLOh4EAQnRELEhDl_Nn5Ab7Uh3U6bPeRcywVLmJGuBzq4_c7pcjTRYT_fD6bisSYdoZLEJXwbvFKKEnI6hB0NLydp7WTX_OCjH-bOZa_UEpBzdLt8x-I9EuYSqPsEjezxOVmz3Pwn8-cBL3bZsf-pDV-mBebdMccovplyU59zFyXS0
# class diagram: http://www.plantuml.com/plantuml/uml/TL6xijem4Etz5IgL6MWeKq42xi9aGlgCRAt9JlGmqeh4m_3laInXH78l3TQUe_FGRZq9Hq6hfbV2UzRksArXyHVd19vzP1ue3oRTMLKDRWE2adTomdWaj2Qn9GmYA9BO4w--Fpmq7St2aOacomneX5hS5FfY1tHAT3v3-RwGiatiVsRVbmHyS5RFu8gHBHzena3zppVeF-QOLO7CCV3xKq0bsoXs3Be3n-Va9kZ_2OTB4Eeqn-Tm2NWL2Wojs6YBsXdeC7fKrdnMrWS7F3QMfK4XVB5Nu2Mk_mLJ1YJwKOc93qRe28pnBrwvDsLLt-0CVpR7PMCkdTD-oB4SSn3nsEvgiKZdMVsM_B2_H_kl3gr3chWTNx5EUEoZNkY9ByzO4nGQABXOiUuLb9RUnTA3Fi2CTEb5SxobOZnkzaj1MVhaTXfDXAf1QRXF4lKW4tdbaevcABuEdZicy6LpnG4rUiY9eerThv-l_XYKZ4sp1IE3Ldy1
from collections import defaultdict
from graphviz import Digraph, render

from constants import EPSILON

class FA:
    """
    Finite Automaton
    """
    def __init__(self, symbols = set(list())):
        self.states = set()
        self.symbols = symbols    # Input symbol table
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

    def add_transition(self, from_state, to_state, symbol):   
        """
        Add only one mapping transition
        """
        if isinstance(symbol, str):
            symbol = set([symbol])
        self.states.add(from_state)
        self.states.add(to_state)
        if from_state in self.transitions and to_state in self.transitions[from_state]:
            self.transitions[from_state][to_state] = self.transitions[from_state][to_state].union(symbol)
        else:
            self.transitions[from_state][to_state] = symbol

    def add_transition_dict(self, transitions): 
        """
        Add the contents of one dictionary to another dictionary
        """
        for from_state, to_states in transitions.items():
            for state in to_states:
                self.add_transition(from_state, state, to_states[state])

    def rebuild_from_number(self, start_number):
        """
        Reset the representation number of each state as start from the given start_number
        """
        translations = {}
        for state in self.states:
            translations[state] = start_number
            start_number += 1
        rebuild = FA(self.symbols)
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
        """
        Reset the state representation number after minimizing the merged state
        """
        rebuilt = FA(self.symbols)
        for from_state, to_states in self.transitions.items():
            for state in to_states:
                rebuilt.add_transition(position[from_state], position[state], to_states[state])
        rebuilt.set_initial_state(position[self.initial_state])
        for state in self.accepting_states:
            rebuilt.add_accepting_states(position[state])
        return rebuilt

    def get_epsilon_closure(self, find_state):
        """
        Set of NFA states reachable from some NFA state on e-transitions
        """
        stack = [find_state]
        epsilon_closure = set()
        while len(stack): # while stack is not empty
            from_state = stack.pop()
            epsilon_closure.add(from_state) # add to e-closure
            if from_state in self.transitions:
                for to_state in self.transitions[from_state]:
                    if EPSILON in self.transitions[from_state][to_state] and to_state not in epsilon_closure:
                        stack.append(to_state) # push onto stack
        return epsilon_closure

    def get_move(self, state, symbol) -> set():
        """
        Set of NFA states to which there is a transition on input symbol from some state
        """
        if isinstance(state, int):
            state = [state]
        transition_states = set()
        for s in state:
            if s in self.transitions:
                for transition in self.transitions[s]:
                    if symbol in self.transitions[s][transition]:
                        transition_states.add(transition)
        return transition_states

    def display(self, fname, pname):
        fa = Digraph(pname, filename = fname, format = 'png')
        fa.attr(rankdir='LR')

        fa.attr('node', shape = 'doublecircle')
        for state in self.accepting_states:
            fa.node('s' + str(state))

        fa.attr('node', shape = 'circle')
        for from_state, to_states in self.transitions.items():
            for state in to_states:
                tmp = ''
                for s in to_states[state]:
                    tmp += s + ','
                fa.edge('s' + str(from_state), 's' + str(state), label = tmp[:-1])

        fa.attr('node', shape = 'point')
        fa.edge('', 's' + str(self.initial_state))

        fa.view(directory="img")