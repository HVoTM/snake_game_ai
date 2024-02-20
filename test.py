def myAtoI(s:str) -> int:
    if s == '':
        return 0
    # inititalize a temporary string for storage
    int_return = ''
    ispositive = True
    # iterate over each character of the string
    for ch in s:
        if ch == '-':
            isneg = False
        if ch.isdigit():
            int_return += ch
        if ispositive:
            return int(int_return)
        else:
            return -1 * int(int_return)
