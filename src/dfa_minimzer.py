import finite_automata as fa

class DFAMinimizer:

    def __init__(self, dfa):
        self._dfa = dfa

        self.dfa_states = list()
        self.transition_table = dict()
        
        self.dfa_states = list(self._dfa.states)
        self._init_transition_table(self.dfa_states)

        self.partitions = dict()
        self.belongs_to_partition = dict()
        
        self._init_partitions(self.dfa_states)

        self.distinguished = dict()

        self._minimise_DFA()


    def display_minDFA(self):
        self._min_dfa.display('mindfa.gv', 'minimal_deterministic_finite_automaton')

    def _minimise_DFA(self):
        """
        Hopcroft's algorithm, partitioning the DFA states into groups by their behavior.
        """

        number_of_sets = 3 
        unchecked_partitions = dict(self.partitions)
        unchecked_partitions_ids = list(unchecked_partitions.keys())

        while unchecked_partitions_ids:
            id = unchecked_partitions_ids.pop()
            partition_states = unchecked_partitions[id]

            for symbol in self._dfa.symbols:

                self.distinguished = dict()

                for from_state in partition_states:
                    self._add_state_to_distinguished(symbol, from_state)


                if len(self.distinguished) > 1:
                    for k, v in self.distinguished.items():
                        if k:
                            for i in v:
                                self.partitions[id].remove(i)
                                if number_of_sets in self.partitions:
                                    self.partitions[number_of_sets] = self.partitions[number_of_sets].union(set([i]))
                                else:
                                    self.partitions[number_of_sets] = set([i])
                            if len(self.partitions[id]) == 0:
                                self.partitions.pop(id)
                            for i in v:
                                self.belongs_to_partition[i] = number_of_sets

                            unchecked_partitions[number_of_sets] = self.partitions[number_of_sets]
                            unchecked_partitions_ids.append(number_of_sets)

                            number_of_sets += 1
                    break

        if len(self.partitions) == len(self.dfa_states):
            self._min_dfa = self._dfa
        else:
            DFAMinimizer.renumber(self.dfa_states, self.belongs_to_partition)
            self._min_dfa = self._dfa.rebuild_from_equal_states(self.partitions, self.belongs_to_partition)


    def _add_state_to_distinguished(self, symbol, from_state):
        to_state = self.transition_table[from_state][symbol]

        partition_of_state = self.belongs_to_partition[to_state] if to_state != None else None
        
        if partition_of_state in self.distinguished:
            self.distinguished[partition_of_state].add(from_state)
        else:
            self.distinguished[partition_of_state] = set([from_state])
        

    def _init_transition_table(self, dfa_states):
        """
        Preprocess the next state that each state can reach via an input symbol
        transition_table(every_state, every_symbol)
        """
        self.transition_table = dict() 

        for dfa_state in self.dfa_states:
            for symbol in self._dfa.symbols:
                if dfa_state in self.transition_table:
                    if symbol in self.transition_table[dfa_state]:
                        self.transition_table[dfa_state][symbol] = self.transition_table[dfa_state][symbol].union(self._dfa.get_move(dfa_state, symbol))
                    else:
                        self.transition_table[dfa_state][symbol] = self._dfa.get_move(dfa_state, symbol)
                else:
                    self.transition_table[dfa_state] = {symbol : self._dfa.get_move(dfa_state, symbol)}
                if len(self.transition_table[dfa_state][symbol]):
                    self.transition_table[dfa_state][symbol] = self.transition_table[dfa_state][symbol].pop() # convert symbol from set to int
                else:
                    self.transition_table[dfa_state][symbol] = None # 0


    def _init_partitions(self, dfa_states):
        """
        initialization 2 sets, nonterminal states and final states
        self.partitions - state sets 
        self.belongs_to_partition - record the set which state belongs to (corresponding to the status)
        """

        self.partitions = {1: set(), 2: set()}
        self.belongs_to_partition = dict()

        for state in self.dfa_states:
            if state not in self._dfa.accepting_states:
                self.partitions[1] = self.partitions[1].union(set([state]))
                self.belongs_to_partition[state] = 1
        for accepting_state in self._dfa.accepting_states:
            self.partitions[2] = self.partitions[2].union(set([accepting_state]))
            self.belongs_to_partition[accepting_state] = 2

    
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