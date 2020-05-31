import finite_automata as fa
# import dfa_minimzer as dfam

class NFA2DFA:
    """
    Nondeterministic finite automaton to deterministic
    """
    def __init__(self, nfa):
        self._nfa = nfa
        self._dfa = {}
        self._min_dfa = {}

        self._build_DFA()
        self.display_DFA()

        self._minimise_DFA()
        

    def display_DFA(self):
        self._dfa.display('dfa.gv', 'deterministic_finite_automaton')

    def display_minDFA(self):
        self._min_dfa.display('mindfa.gv', 'minimal_deterministic_finite_automaton')

    def _build_DFA(self): 
        """
        The subset construction
        """
        marked_states = dict()  
        epsilon_closure = dict()   # every state's e-closure
        start = self._nfa.get_epsilon_closure(self._nfa.initial_state)
        epsilon_closure[self._nfa.initial_state] = start
        number_of_subset = 1 # the number of subset, dfa state id
        dfa = fa.FA(self._nfa.symbols)
        dfa.set_initial_state(number_of_subset)
        unmarked_states = [[start, dfa.initial_state]] 
        marked_states[number_of_subset] = start
        number_of_subset += 1
        while len(unmarked_states): # while there is an unmarked state in transitions
            state, from_state = unmarked_states.pop()
            for ch in dfa.symbols: # for each input symbol ch
                transition_states = self._nfa.get_move(state, ch)
                for s in list(transition_states): 
                    if s not in epsilon_closure:
                        epsilon_closure[s] = self._nfa.get_epsilon_closure(s)
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
                if self._nfa.accepting_states[0] in state:
                    dfa.add_accepting_states(value)
        self._dfa = dfa

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

    def _minimise_DFA(self):
        """
        Hopcroft's algorithm, partitioning the DFA states into groups by their behavior.
        """
        dfa_states = list(self._dfa.states)
        transition_table = self._create_transition_table(dfa_states)

        # initialization 2 sets, nonterminal states and final states
        # partitions - state sets 
        # belongs_to_partition - record the set which state belongs to (corresponding to the status)
        partitions, belongs_to_partition = self._prepare_partitions(dfa_states)

        number_of_sets = 3 
        unchecked_partitions = dict(partitions)
        unchecked_partitions_ids = list(unchecked_partitions.keys())

        while unchecked_partitions_ids:
            id = unchecked_partitions_ids.pop()
            partition_states = unchecked_partitions[id]

            for symbol in self._dfa.symbols:

                distinguished = dict()

                def add_to_distinguished(state):
                    if belongs_to_partition[state] in distinguished:
                        distinguished[belongs_to_partition[state]].add(from_state)
                    else:
                        distinguished[belongs_to_partition[state]] = set([from_state])

                for from_state in partition_states:
                    to_state = transition_table[from_state][symbol]

                    if to_state == None: #0
                        if None in distinguished: #0
                            distinguished[None].add(from_state)
                        else:
                            distinguished[None] = set([from_state])
                    else:
                        add_to_distinguished(to_state)


                if len(distinguished) > 1:
                    for k, v in distinguished.items():
                        if k:
                            for i in v:
                                partitions[id].remove(i)
                                if number_of_sets in partitions:
                                    partitions[number_of_sets] = partitions[number_of_sets].union(set([i]))
                                else:
                                    partitions[number_of_sets] = set([i])
                            if len(partitions[id]) == 0:
                                partitions.pop(id)
                            for i in v:
                                belongs_to_partition[i] = number_of_sets

                            unchecked_partitions[number_of_sets] = partitions[number_of_sets]
                            unchecked_partitions_ids.append(number_of_sets)

                            number_of_sets += 1
                    break

        if len(partitions) == len(dfa_states):
            self._min_dfa = self._dfa
        else:
            NFA2DFA.renumber(dfa_states, belongs_to_partition)
            self._min_dfa = self._dfa.rebuild_from_equal_states(partitions, belongs_to_partition)

    def _create_transition_table(self, dfa_states):
        """
        Move(every_state, every_symbol)
        """
        move = dict() 

        """
        Preprocess the next state that each state can reach via an input symbol
        """
        for dfa_state in dfa_states:
            for symbol in self._dfa.symbols:
                if dfa_state in move:
                    if symbol in move[dfa_state]:
                        move[dfa_state][symbol] = move[dfa_state][symbol].union(self._dfa.get_move(dfa_state, symbol))
                    else:
                        move[dfa_state][symbol] = self._dfa.get_move(dfa_state, symbol)
                else:
                    move[dfa_state] = {symbol : self._dfa.get_move(dfa_state, symbol)}
                if len(move[dfa_state][symbol]):
                    move[dfa_state][symbol] = move[dfa_state][symbol].pop() # convert symbol from set to int
                else:
                    move[dfa_state][symbol] = None # 0
        
        return move


    def _prepare_partitions(self, dfa_states):
        equivalent = {1: set(), 2: set()}
        position = dict()

        for state in dfa_states:
            if state not in self._dfa.accepting_states:
                equivalent[1] = equivalent[1].union(set([state]))
                position[state] = 1
        for accepting_state in self._dfa.accepting_states:
            equivalent[2] = equivalent[2].union(set([accepting_state]))
            position[accepting_state] = 2

        return equivalent, position