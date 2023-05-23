class Node:
    def __init__(self, data):
        self.left = None
        self.right = None
        self.data = data
    
    def insert(self, data):
        if self.data:
            if data < self.data:
                if self.left is None:
                    self.left = Node(data)
                else:
                    self.left.insert(data)
            elif data > self.data:
                if self.right is None:
                    self.right = Node(data)
                else:
                    self.right.insert(data)
        else:
            self.data = data

    def output(self):
        if self.left:
            self.left.output()
        print(self.data)
        if self.right:
            self.right.output()
    

    def exists(self, val):
        if val == self.data:
            return True

        if val < self.data:
            if self.left == None:
                return False
            return self.left.exists(val)

        if self.right == None:
            return False
        return self.right.exists(val)
    


def find_parent(height, node):
    """
    e.g.
    height = 3
    perfect binary tree(post-order)
         7
       /   \
      3     6
     / \   / \
    1   2 4   5

    with post-order traversal, got
    [1,2,3,4,5,6,7]
    """
 
    start = 1
    end = 2**height - 1
 
    # When node is root node, return -1 for root node has no parent
    if (end == node):
        return -1
 
    # Loop till we found the given node
    while True:
 
        # Exclude last node
        end = end - 1
 
        # Find the middle node,
        # mid and end will point to children nodes of LAST end.
        # Check perfect binary tree at 50th line for reference
        mid = start + (end - start)//2
        print(f'mid: {mid}, end:{end}')
 
        if(mid == node or end == node):
            return (end + 1)
         
        # Search left subtree
        elif (node < mid):
            end = mid
        # Search right subtree
        else:
            start = mid
    
def solution(h, q=None):
    tree = list(range(1, 2**h))
    max_idx = len(tree) - 1
    print(max_idx)
    print(tree)

    labels = []
    for idx in q:
        if idx > max_idx:
            labels.append(-1)
        else:
            labels.append(find_parent(h, idx))
    
    return labels

if __name__ == '__main__':
    # print(solution(3, [7, 3, 5, 1]))
    # print(solution(5, [19, 14, 28]))
    p = find_parent(4, 13)
    print(p)
    p = find_parent(4, 10)
    print(p)

