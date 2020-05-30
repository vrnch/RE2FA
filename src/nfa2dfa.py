import finite_automata as fa

class NFA2DFA:
    """
    Nondeterministic finite automaton to deterministic
    """
    def __init__(self, nfa):
        self.build_DFA(nfa)

    def display_DFA(self):
        self.dfa.display('dfa.gv', 'deterministic_finite_automaton')

    def display_minDFA(self):
        self.minDFA.display('mindfa.gv', 'minimal_deterministic_finite_automaton')

    def build_DFA(self, nfa): 
        """
        The subset construction
        """
        marked_states = dict()  
        epsilon_closure = dict()   # every state's e-closure
        start = nfa.get_epsilon_closure(nfa.initial_state)
        epsilon_closure[nfa.initial_state] = start
        number_of_subset = 1 # the number of subset, dfa state id
        dfa = fa.FA(nfa.symbols)
        dfa.set_initial_state(number_of_subset)
        unmarked_states = [[start, dfa.initial_state]] 
        marked_states[number_of_subset] = start
        number_of_subset += 1
        while len(unmarked_states): # while there is an unmarked state in transitions
            state, from_state = unmarked_states.pop()
            for ch in dfa.symbols: # for each input symbol ch
                transition_states = nfa.get_move(state, ch)
                for s in list(transition_states): 
                    if s not in epsilon_closure:
                        epsilon_closure[s] = nfa.get_epsilon_closure(s)
                    transition_states = transition_states.union(epsilon_closure[s])
                if len(transition_states):
                    if transition_states not in marked_states.values(): # if transition is unmarked
                        unmarked_states.append([transition_states, number_of_subset])
                        marked_states[number_of_subset] = transition_states
                        to_state = number_of_subset
                        number_of_subset += 1
                    else:
                        to_state = [k for k, v in marked_states.items() if v  ==  transition_states][0]
                    dfa.add_transition(from_state, to_state, ch)
            for value, state in marked_states.items():
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
        Hopcroft's algorithm, partitioning the DFA states into groups by their behavior.
        """
        dfa_states = list(self.dfa.states)
        move = dict() # Move(every state, every symbol)

        """
        Preprocess the next state that each state can reach via an input symbol
        """
        for state in dfa_states:
            for symbol in self.dfa.symbols:
                if state in move:
                    if symbol in move[state]:
                        move[state][symbol] = move[state][symbol].union(self.dfa.get_move(state, symbol))
                    else:
                        move[state][symbol] = self.dfa.get_move(state, symbol)
                else:
                    move[state] = {symbol : self.dfa.get_move(state, symbol)}
                if len(move[state][symbol]):
                    move[state][symbol] = move[state][symbol].pop()
                else:
                    move[state][symbol] = 0

        equivalent = dict()  # state sets 
        position = dict()    # record the set which state belongs to (corresponding to the status)

        # initialization 2 sets, nonterminal states and final states
        equivalent = {1: set(), 2: set()}
        for state in dfa_states:
            if state not in self.dfa.accepting_states:
                equivalent[1] = equivalent[1].union(set([state]))
                position[state] = 1
        for accepting_state in self.dfa.accepting_states:
            equivalent[2] = equivalent[2].union(set([accepting_state]))
            position[accepting_state] = 2

        unchecked = list()
        number_of_sets = 3 
        unchecked.extend([[equivalent[1], 1], [equivalent[2], 2]])
        while len(unchecked):
            equal_states, id = unchecked.pop()
            for symbol in self.dfa.symbols:
                distinguished = dict()
                for state in equal_states:
                    if move[state][symbol] == 0:
                        if 0 in distinguished:
                            distinguished[0].add(state)
                        else:
                            distinguished[0] = set([state])
                    else:
                        if position[
                            move[state][symbol]
                        ] in distinguished:
                            distinguished[position[move[state][symbol]]
                            ].add(state)
                        else:
                            distinguished[position[move[state][symbol]]] = set([state])
                if len(distinguished) > 1:
                    for k, v in distinguished.items():
                        if k:
                            for i in v:
                                equivalent[id].remove(i)
                                if number_of_sets in equivalent:
                                    equivalent[number_of_sets] = equivalent[number_of_sets].union(set([i]))
                                else:
                                    equivalent[number_of_sets] = set([i])
                            if len(equivalent[id]) == 0:
                                equivalent.pop(id)
                            for i in v:
                                position[i] = number_of_sets
                            unchecked.append([equivalent[number_of_sets], number_of_sets])
                            number_of_sets += 1
                    break
        if len(equivalent) == len(dfa_states):
            self.minDFA = self.dfa
        else:
            NFA2DFA.renumber(dfa_states, position)
            self.minDFA = self.dfa.rebuild_from_equal_states(equivalent, position)