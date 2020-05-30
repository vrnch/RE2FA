trainsitions = {
    1 : {
        2 : {
            'b'
        },
        3 : {
            'a'
        }
    },
    2 : {
        2 : {'b'},
        3 : {'a'}
    },
    3 : {
        4 : {'b'},
        3 : {'a'}
    },
    4 : {
        5 : {'b'},
        3 : {'a'}
    },
    5 : {
        2 : {'b'},
        3 : {'a'}
    }
}

for from_state, to_state in trainsitions.items() : 
    for state, symbol in to_state.items() :     
        print(f"{from_state} - {symbol} -> {state}")

