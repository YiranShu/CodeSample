class Node:
    def __init__(self, order=3):
        self.order = order
        self.keys = []
        self.children = []
        self.is_leaf = False
        self.parent = self.prev = self.next = None

    def add(self, key):
        if not self.keys or key >= self.keys[-1]:
            self.keys.append(key)
        else:
            for index, item in enumerate(self.keys):
                if key < item:
                    self.keys.insert(index, key)
                    break
        if len(self.keys) == self.order:
            self.split()

    def insert_child_to_parent(self, new_Node):
        if self.parent:
            new_Node.parent = self.parent
            for index, child in enumerate(self.parent.children):
                if child is self:
                    self.parent.children.insert(index, new_Node)
                    break
        else:
            parent = Node(order=self.order)
            parent.children.extend([new_Node, self])
            self.parent = new_Node.parent = parent

    def split(self):
        new_Node = Node(order=self.order)
        mid = self.order // 2
        new_Node.is_leaf = self.is_leaf

        if self.is_leaf:
            new_Node.keys, self.keys = self.keys[:mid], self.keys[mid:]
            new_Node.prev, new_Node.next = self.prev, self
            if self.prev:
                self.prev.next = new_Node
            self.prev = new_Node
            self.insert_child_to_parent(new_Node)
            self.parent.add(self.keys[0])
        else:
            new_key = self.keys[mid]
            new_Node.keys, self.keys = self.keys[:mid], self.keys[mid + 1:]
            new_Node.children, self.children = self.children[:mid + 1], self.children[mid + 1:]
            self.insert_child_to_parent(new_Node)
            self.parent.add(new_key)

class BPlusTree:
    def __init__(self, order=3):
        self.root = Node(order)
        self.root.is_leaf = True

    def insert(self, key):
        leaf = self.find(key)
        leaf.add(key)
        while self.root.parent:
            self.root = self.root.parent

    def find(self, key):
        node = self.root
        while not node.is_leaf:
            if key >= node.keys[-1]:
                node = node.children[-1]
                continue
            for index, item in enumerate(node.keys):
                if key < item:
                    node = node.children[index]
                    break
        return node

    def print(self):
        queue = [(self.root, True)]
        s = ''
        while queue:
            node, is_last = queue.pop(0)
            s += 'keys: ' + str(node.keys) + '   '
            if is_last:
                print(s)
                s = ''
            for index, child in enumerate(node.children):
                if is_last and index == len(node.children) - 1:
                    queue.append((child, True))
                else:
                    queue.append((child, False))

if __name__ == '__main__':
    bplus_tree = BPlusTree(4)
    keys = [6, 9, 15, 34, 54, 65, 98, 108, 112, 115]
    for key in keys:
        bplus_tree.insert(key)
        bplus_tree.print()
        print()