
def get_dividors(s):
    possible_cut = []
    n = len(s)
    dividors = []

    for i in range(2, n):
        if n % i == 0:
            dividors.append(i)

    for d in dividors:
        cake = s
        pieces = []

        while len(cake):
            pieces.append(cake[:d])
            cake = cake[d:]
        
        if len(set(pieces)) == 1:
            possible_cut.append(d)

    return n // min(possible_cut)


if __name__ == '__main__':

    print(get_dividors("abccbaabccba"))
