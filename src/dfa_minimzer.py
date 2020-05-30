# import finite_automata as fa

# class DFAMinimizer:

#     def __init__(self, dfa):
#         self.dfa = dfa

#      def minimise(self):
#         """
#         Hopcroft's algorithm, partitioning the DFA states into groups by their behavior.
#         """
#         dfa_states = list(self.dfa.states)
#         transition_table = _create_transition_table()

#         equivalent = dict()  # state sets 
#         position = dict()    # record the set which state belongs to (corresponding to the status)

#         # initialization 2 sets, nonterminal states and final states
#         equivalent = _prepare_equivalent()

#         unchecked = list()
#         number_of_sets = 3 
#         unchecked.extend([[equivalent[1], 1], [equivalent[2], 2]])
#         while len(unchecked):
#             equal_states, id = unchecked.pop()
#             for symbol in self.dfa.symbols:
#                 distinguished = dict()
#                 for state in equal_states:
                    
#                     transition = transition_table[state][symbol]

#                     if transition == 0:
#                         if 0 in distinguished:
#                             distinguished[0].add(state)
#                         else:
#                             distinguished[0] = set([state])
#                     else:
#                         if position[transition] in distinguished:
#                             distinguished[position[transition]].add(state)
#                         else:
#                             distinguished[position[transition]] = set([state])
#                 if len(distinguished) > 1:
#                     for k, v in distinguished.items():
#                         if k:
#                             for i in v:
#                                 equivalent[id].remove(i)
#                                 if number_of_sets in equivalent:
#                                     equivalent[number_of_sets] = equivalent[number_of_sets].union(set([i]))
#                                 else:
#                                     equivalent[number_of_sets] = set([i])
#                             if len(equivalent[id]) == 0:
#                                 equivalent.pop(id)
#                             for i in v:
#                                 position[i] = number_of_sets
#                             unchecked.append([equivalent[number_of_sets], number_of_sets])
#                             number_of_sets += 1
#                     break
#         if len(equivalent) == len(dfa_states):
#             self.minDFA = self.dfa
#         else:
#             NFA2DFA.renumber(dfa_states, position)
#             self.minDFA = self.dfa.rebuild_from_equal_states(equivalent, position)


#         def _create_transition_table(self):
#             """
#             Move(every state, every symbol)
#             """
#             move = dict() # Move(every state, every symbol)

#             """
#             Preprocess the next state that each state can reach via an input symbol
#             """
#             for state in dfa_states:
#                 for symbol in self.dfa.symbols:
#                     if state in move:
#                         if symbol in move[state]:
#                             move[state][symbol] = move[state][symbol].union(self.dfa.get_move(state, symbol))
#                         else:
#                             move[state][symbol] = self.dfa.get_move(state, symbol)
#                     else:
#                         move[state] = {symbol : self.dfa.get_move(state, symbol)}
#                     if len(move[state][symbol]):
#                         move[state][symbol] = move[state][symbol].pop()
#                     else:
#                         move[state][symbol] = 0
            
#             return move


#         def _prepare_equivalent(self):
#             equivalent = {1: set(), 2: set()}

#             for state in dfa_states:
#                 if state not in self.dfa.accepting_states:
#                     equivalent[1] = equivalent[1].union(set([state]))
#                     position[state] = 1
#             for accepting_state in self.dfa.accepting_states:
#                 equivalent[2] = equivalent[2].union(set([accepting_state]))
#                 position[accepting_state] = 2

#             return equivalent