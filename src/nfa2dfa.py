import finite_automata as fa

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
        dfa = fa.FA(nfa.symbols)
        dfa.set_initial_state(number_of_subset)
        states = [[state1, dfa.initial_state]] # unvisited
        all_states[number_of_subset] = state1
        number_of_subset += 1
        while len(states):
            state, from_index = states.pop()
            for ch in dfa.symbols:
                transition_states = nfa.get_move(state, ch)
                for s in list(transition_states):    # Converted to list, equivalent to using a temporary variable
                    if s not in epsilon_closure:
                        epsilon_closure[s] = nfa.get_epsilon_closure(s)
                    transition_states = transition_states.union(epsilon_closure[s])
                if len(transition_states):
                    if transition_states not in all_states.values():
                        states.append([transition_states, number_of_subset])
                        all_states[number_of_subset] = transition_states
                        to_index = number_of_subset
                        number_of_subset += 1
                    else:
                        to_index = [k for k, v in all_states.items() if v  ==  transition_states][0]
                    dfa.add_transition(from_index, to_index, ch)
            for value, state in all_states.items():
                if nfa.accepting_states[0] in state:
                    dfa.add_accepting_states(value)
        self.dfa = dfa

    @staticmethod
    def renumber(states, position): 
        """
        Renumber the sets' number begin from 1
        """
        count = 1
        change = dict()
        for state in states:
            if position[state] not in change:
                change[position[state]] = count
                count += 1
            position[state] = change[position[state]]

    def minimise(self):
        """
        Segmentation method to generate a new set of states
        """
        states = list(self.dfa.states)
        to_state = dict(set()) # Move(every state, every symbol)

        """
        Preprocess the next state that each state can reach via an input symbol
        """
        for state in states:
            for symbol in self.dfa.symbols:
                if state in to_state:
                    if symbol in to_state[state]:
                        to_state[state][symbol] = to_state[state][symbol].union(self.dfa.get_move(state, symbol))
                    else:
                        to_state[state][symbol] = self.dfa.get_move(state, symbol)
                else:
                    to_state[state] = {symbol : self.dfa.get_move(state, symbol)}
                if len(to_state[state][symbol]):
                    to_state[state][symbol] = to_state[state][symbol].pop()
                else:
                    to_state[state][symbol] = 0

        equal = dict()  # state sets 
        position = dict()    # record the set which state belongs to (corresponding to the status)

        # initialization 2 sets, nonterminal states and final states
        equal = {1: set(), 2: set()}
        for state in states:
            if state not in self.dfa.accepting_states:
                equal[1] = equal[1].union(set([state]))
                position[state] = 1
        for accepting_state in self.dfa.accepting_states:
            equal[2] = equal[2].union(set([accepting_state]))
            position[accepting_state] = 2

        unchecked = list()
        number_of_sets = 3 
        unchecked.extend([[equal[1], 1], [equal[2], 2]])
        while len(unchecked):
            equal_states, id = unchecked.pop()
            for symbol in self.dfa.symbols:
                different_states = dict()
                for state in equal_states:
                    if to_state[state][symbol] == 0:
                        if 0 in different_states:
                            different_states[0].add(state)
                        else:
                            different_states[0] = set([state])
                    else:
                        if position[to_state[state][symbol]] in different_states:
                            different_states[position[to_state[state][symbol]]].add(state)
                        else:
                            different_states[position[to_state[state][symbol]]] = set([state])
                if len(different_states) > 1:
                    for k, v in different_states.items():
                        if k:
                            for i in v:
                                equal[id].remove(i)
                                if number_of_sets in equal:
                                    equal[number_of_sets] = equal[number_of_sets].union(set([i]))
                                else:
                                    equal[number_of_sets] = set([i])
                            if len(equal[id]) == 0:
                                equal.pop(id)
                            for i in v:
                                position[i] = number_of_sets
                            unchecked.append([equal[number_of_sets], number_of_sets])
                            number_of_sets += 1
                    break
        if len(equal) == len(states):
            self.minDFA = self.dfa
        else:
            NFA2DFA.renumber(states, position)
            self.minDFA = self.dfa.rebuild_from_equal_states(equal, position)