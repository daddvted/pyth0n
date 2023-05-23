def recursion(l: list):
    global tmp
    if len(l) == 0:
        return tmp
    else:
        item = l.pop()
        if item.endswith('[]'):
            inner_object = {
                item[:-2]: [tmp]
            }
            # tmp = copy.deepcopy(inner_object)
            tmp = inner_object
        else:
            inner_object = {
                item: tmp
            }
            tmp = inner_object

        return recursion(l)


def for_loop(l: list):
    l.reverse()
    global tmp
    for item in l:
        if item.endswith('[]'):
            inner_object = {
                item[:-2]: [tmp]
            }
            # tmp = copy.deepcopy(inner_object)
            tmp = inner_object
        else:
            inner_object = {
                item: tmp
            }
            tmp = inner_object

    return tmp


if __name__ == "__main__":
    path = "houses[].houseOrgBorrowInfos.personName.abc[].efg"

    tmp = None

    # print(recursion(path.split('.')))
    print(for_loop(path.split('.')))
