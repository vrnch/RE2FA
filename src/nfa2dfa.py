import finite_automata as fa
# import dfa_minimzer as dfam

class NFA2DFA:
    """
    Nondeterministic finite automaton to deterministic
    """
    def __init__(self, nfa):
        self._nfa = nfa
        self._dfa = {}

        self._build_DFA()


    def display_DFA(self):
        self._dfa.display('dfa.gv', 'deterministic_finite_automaton')

    def get_DFA(self):
        return self._dfa

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


