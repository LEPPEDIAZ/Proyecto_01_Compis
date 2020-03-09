def regularexp_valido(expresion_regular):
    return valid_brackets(expresion_regular) and valid_operations(expresion_regular)


def valid_brackets(expresion_regular):
    opened_brackets = 0
    for c in expresion_regular:
        if c == '(':
            opened_brackets += 1
        if c == ')':
            opened_brackets -= 1
        if opened_brackets < 0:
            print('ERROR missing bracket')
            return False
    if opened_brackets == 0:
        return True
    print('ERROR unclosed brackets')
    return False


def valid_operations(expresion_regular):
    for i, c in enumerate(expresion_regular):
        if c == '*':
            if i == 0:
                print('ERROR * with no argument at', i)
                return False
            if expresion_regular[i - 1] in '(|':
                print('ERROR * with no argument at', i)
                return False
        if c == '|':
            if i == 0 or i == len(expresion_regular) - 1:
                print('ERROR | with missing argument at', i)
                return False
            if expresion_regular[i - 1] in '(|':
                print('ERROR | with missing argument at', i)
                return False
            if expresion_regular[i + 1] in ')|':
                print('ERROR | with missing argument at', i)
                return False
    return True
	