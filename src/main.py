from regex2nfa import Regex2NFA
from nfa2dfa import NFA2DFA

if __name__ == '__main__':

    #regex = input('Enter the regex: ')
    regex = "(a|b)*abb"
    #regex = "(a*|b*)*"
    #regex = "(00|11)*((01|10)(11|00)*(01|10)(11|00)*)"
    a = Regex2NFA(regex)
    a.display_NFA()

    b = NFA2DFA(a.nfa)
    b.display_DFA()
    b.display_minDFA()