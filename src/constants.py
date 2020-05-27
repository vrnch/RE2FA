
KLEENE_CLOSURE = '*'
ALTERNATION = '|'
CONCATENATION = '·'
LEFT_PARENTHESES, RIGHT_PARENTHESES = '(', ')'
ALPHABET = [chr(i) for i in range(ord('A'), ord('Z') + 1)] + \
           [chr(i) for i in range(ord('a'), ord('z') + 1)] + \
           [chr(i) for i in range(ord('0'), ord('9') + 1)]
EPSILON = 'ε'