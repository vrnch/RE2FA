from constants import *
import finite_automata as fa

class Regex2NFA:
    """
    Regular expression to nondeterministic finite automaton
    """
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
        else:       # left bracket 
            return 0

    @staticmethod
    def get_symbol_template(symbol):  
        """
        symbol -> NFA
        """
        from_state = 1
        to_state = 2
        symbol_template = fa.FA(set([symbol]))
        symbol_template.set_initial_state(from_state)
        symbol_template.add_accepting_states(to_state)
        symbol_template.add_transition(from_state, to_state, symbol)
        return symbol_template

    @staticmethod
    def get_alternation_template(a, b):  
        """
        a | b -> NFA
        """
        a, num1 = a.rebuild_from_number(2)
        b, num2 = b.rebuild_from_number(num1)
        from_state = 1
        to_state = num2
        alternation_template = fa.FA(a.symbols.union(b.symbols))
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
        a, num1 = a.rebuild_from_number(1)
        b, num2 = b.rebuild_from_number(num1)
        from_state = 1
        to_state = num2 - 1
        concatenation_template = fa.FA(a.symbols.union(b.symbols))
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
        a, num1 = a.rebuild_from_number(2)
        from_state = 1
        to_state = num1
        kleene_closure_template = fa.FA(a.symbols)
        kleene_closure_template.set_initial_state(from_state)
        kleene_closure_template.add_accepting_states(to_state)
        kleene_closure_template.add_transition(kleene_closure_template.initial_state, a.initial_state, EPSILON)
        kleene_closure_template.add_transition(kleene_closure_template.initial_state, kleene_closure_template.accepting_states[0], EPSILON)
        kleene_closure_template.add_transition(a.accepting_states[0], kleene_closure_template.accepting_states[0], EPSILON)
        kleene_closure_template.add_transition(a.accepting_states[0], a.initial_state, EPSILON)
        kleene_closure_template.add_transition_dict(a.transitions)
        return kleene_closure_template

    @staticmethod
    def to_postfix(regex) :
        """
        Convert infix expression to postfix expression
        """ 
        postfix = ''
        previous = ''
        symbol = set()

        """
        Explicitly add concatenation operator to the expression 
        """
        for ch in regex:
            if ch in ALPHABET:
                symbol.add(ch)
            if ch in ALPHABET or ch == LEFT_PARENTHESES:
                if previous != CONCATENATION and (previous in ALPHABET or previous in [KLEENE_CLOSURE, RIGHT_PARENTHESES]):
                    postfix += CONCATENATION
            postfix += ch
            previous = ch
        regex = postfix

        postfix = ''
        stack = list()
        for ch in regex:
            if ch in ALPHABET:
                postfix += ch
            elif ch == LEFT_PARENTHESES:
                stack.append(ch)
            elif ch == RIGHT_PARENTHESES:
                while(stack[-1] != LEFT_PARENTHESES):
                    postfix += stack[-1]
                    stack.pop()
                stack.pop()    # pop left bracket
            else:
                while(len(stack) and Regex2NFA.get_precedence(stack[-1]) >= Regex2NFA.get_precedence(ch)):
                    postfix += stack[-1]
                    stack.pop()
                stack.append(ch)
        while(len(stack) > 0):
            postfix += stack.pop()
        return postfix

    @staticmethod
    def get_symbol(regex) :
        """
        Get symbols from the regex
        """
        symbol = set()
        for ch in regex:
            if ch in ALPHABET:
                symbol.add(ch)
        return symbol
        
    def build_NFA(self):
        """ 
        Thompson's construction (from postfix regex)
        """ 
        self.automata = list()
        for ch in Regex2NFA.to_postfix(self.regex):
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
        self.nfa.symbols = Regex2NFA.get_symbol(self.regex)