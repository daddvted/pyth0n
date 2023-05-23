# You have L, a list containing some digits (0 to 9).
# Write a function solution(L) which finds the largest number that can be made from some or all of these digits and is divisible by 3.
# If it is not possible to make such a number, return 0 as the solution.
# L will contain anywhere from 1 to 9 digits. 
# The same digit may appear multiple times in the list, but each element in the list may only be used once.
from itertools import combinations

def is_divided_by_3(num):
    return True if num % 3 == 0 else False

def format_num(l):
    l.sort(reverse=True)
    str_num = "".join(list(map(str, l)))
    return int(str_num)

def solution(l):
    for n in range(1, len(l)+1)[::-1]:
        candidates = []
        for com in combinations(l, n):
            if is_divided_by_3(sum(com)):
                candidates.append(format_num(list(com)))
        if candidates:
            candidates.sort()
            return candidates[-1]
    return 0



if __name__ == '__main__':
    # l = [3,1,4,1]
    # l = [3,1,4,2]
    # l = [9,9,9,1]
    l = [3, 1, 4, 1, 5, 9]
    print(solution(l))