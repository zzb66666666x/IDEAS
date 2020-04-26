# this is the code for B-tree
from math import ceil

class Btree:
    def __init__(self, order=5):
        self.order = order
        self.min = ceil(order/2)
        self.max = order - 1
        self.root = LinkedList()

    def find(self, key):
        return self.__find(self.root, key)

    def __find(self, root, key):
        # for i in root:
        #     print(i.key, end=" ")
        # print()
        if root is None:
            return False
        node = root.find_loc_for_key(key)
        if node is None:
            return self.__find(root.child, key)
        else:
            if node.key == key:
                return node.data
            else:
                return self.__find(node.child, key)

    def insert(self, key, value):
        # print("#############")
        # print("the key inserted is:", key)
        # print("the value inserted is:", value)
        self.__insert(self.root, key, value)
        # print("#############\n")

    def __insert(self, root, key, value):
        if root.child is None:
            # at the leaf node
            self.__insert_to_root(root, key, value)
        else:
            node = root.find_loc_for_key(key)
            if node is None:
                self.__insert(root.child, key, value)
            else:
                self.__insert(node.child, key, value)

    def __insert_to_root(self, root, key, value, child=None):
        if root.numberKeys < self.max:
            # print("Inside the root.numberKeys < self.max")
            # print("the number of keys: ", root.numberKeys)
            root.insert(key, value, child)
            # print("the root has: ")
            # for i in root:
            #     print(i.key, end = " ")
            # print()
        else:
            # print("seems that too many elements in one list")
            root.insert(key, value, child)
            # print("------checking-------")
            # for i in root:
            #     print(i.key, end = " ")
            # print()
            split_res = root.split(self.order)
            root = split_res[0]
            single_node = split_res[1]
            second_list = split_res[2]
            # for i in root:
            #     print(i.key, end = " ")
            # print("   ", end="")
            # print(single_node.key, "    ", end="")
            # for i in second_list:
            #     print(i.key, end = " ")
            # print()
            # print("the single node has value:",single_node.key)
            # print("the single node has child:", single_node.child)
            # print("-------finished------")
            self.__adjust(root, single_node, second_list)

    def __adjust(self, root, single_node, second_list):
        # print("Begin to adjust things... ")
        if root.parent is None:
            # print("No parent -- create one, the new root")
            new_parent = LinkedList(child=root)
            self.__insert_to_root(new_parent, single_node.key, single_node.data, second_list) # this may trigger further split
            root.parent = new_parent
            second_list.parent = new_parent
            self.root = new_parent
            # print("New parent!!!")
            # for i in root.parent:
            #     print(i.key, end = " ")
            # print()
            # print("See whether it's possible for parents to find children")
            # for i in root.parent.child:
            #     print(i.key, end = " ")
            # print()
            # for i in second_list.parent.first.child:
            #     print(i.key, end = " ")
            # print()
        else:
            # print("------checking in adjust-------")
            parent = root.parent
            # for i in parent:
            #     print(i.key, end=" ")
            # print()
            # print("-------finished for adjust------")
            self.__insert_to_root(parent, single_node.key, single_node.data, second_list)

    def show(self):
        # Using BFS here to print out the tree
        queue1 = Queue()
        queue2 = Queue()
        queue1.enqueue(self.root)
        layer = 0
        while queue1.is_empty() is False:
            print("\n### LAYER %d ###" % layer)
            while queue1.is_empty() is False:
                current_list = queue1.dequeue()
                if current_list.child is not None:
                    queue2.enqueue(current_list.child)
                for i in current_list:
                    if i.child is not None:
                        queue2.enqueue(i.child)
                    print(i.key, end=" ")
                print()
            queue1 = queue2
            queue2 = Queue()
            layer += 1
            print("###############\n")


class LinkedList:
    class Node:
        def __init__(self, key = None, data = None, next = None, child = None):
            self.key = key
            self.data = data
            self.next = next
            self.child = child # things with larger key

    def __init__(self, parent=None, numberKeys=0, first=None, last=None, child=None):
        self.parent = parent
        self.numberKeys = numberKeys
        self.first = first
        self.last = last
        self.child = child # things with key < current key

    def __iter__(self):
        cursor = self.first
        while cursor is not None:
            yield cursor
            cursor = cursor.next

    def find_loc_for_key(self, key):
        # locate the position within: cursor <= pos < cursor.next
        # then return cursor
        # facing the end of the linked list?
        # then still return cursor(the cursor will point to the last node)
        # facing the starting point of the list(ie. less than the first key)?
        # then return None
        cursor = self.first
        if cursor is None or (cursor is not None and key < cursor.key):
            return None
        else:
            # cursor is not None
            while cursor.next is not None:
                temp_key = cursor.next.key
                if cursor.key <= key < temp_key:
                    break
                cursor = cursor.next
            return cursor

    def locate(self, key):
        cursor = self.first
        while cursor is not None:
            if cursor.key == key:
                return cursor
            cursor = cursor.next
        raise IndexError("No such key here")

    def insert(self, key, value, child=None):
        node = self.find_loc_for_key(key)
        if node is None:
            # insert to the first position or insert to an empty list
            next = self.first
            new_node = self.Node(key, value, next, child)
            self.first = new_node
            if self.last is None:
                self.last = new_node
            self.numberKeys += 1
            return node,new_node
        elif node.next is None:
            # at the last position of the list
            new_node = self.Node(key, value, None, child)
            node.next = new_node
            self.last = new_node
            self.numberKeys += 1
            return node, new_node
        else:
            # no need to change node.first and node.last
            next = node.next
            new_node = self.Node(key, value, next, child)
            node.next = new_node
            self.numberKeys += 1
            return node,new_node

    def split(self, order):
        # take order == 5, then by the moment this function is called, there will be 5 elements in this list
        # then split it into 1 2; 3; 4 5
        # the middle one which should be picked out for parents should be ceil(order + 1) = 3
        # run through the list to locate the 2, so take counter = 1
        # while counter < 2, move the cursor from 1 to 2, then counter = 2, the next loop will terminate
        # the cursor will be the end of first list
        # cursor.next will be the single node, and the cursor.next.next will be the start of the second new list
        index1 = ceil((order+1)/2) - 1
        counter = 1
        cursor = self.first
        while counter < index1:
            cursor = cursor.next
            counter += 1
        single_node = cursor.next
        new_list_head = single_node.next
        second_list = LinkedList(parent=self.parent, child=single_node.child)
        self.truncate(cursor)
        second_list.build(new_list_head)
        single_node.next = None
        return self,single_node,second_list

    def truncate(self, node):
        node.next = None
        self.adjust()

    def build(self, node):
        self.first = node
        self.adjust()

    def adjust(self):
        cursor = self.first
        prev = None
        counter = 0
        while cursor is not None:
            if cursor.child is not None:
                cursor.child.parent = self
            prev = cursor
            cursor = cursor.next
            counter += 1
        self.numberKeys = counter
        self.last = prev

class Queue:
    class __Node:
        def __init__(self, val):
            self.val = val
            self.next = None

    def __init__(self, content=[]):
        self.head = None
        self.end = None
        for i in content:
            self.enqueue(i)

    def enqueue(self, val):
        node = self.__Node(val)
        if self.end is None:
            assert (self.head is None)
            self.head = self.end = node
        else:
            self.end.next = node
            self.end = node

    def dequeue(self):
        if self.head is None:
            return None
        node = self.head
        self.head = node.next
        if self.head is None:
            self.end = None
        return node.val

    def is_empty(self):
        if self.head is None:
            assert (self.end is None)
            return True
        return False

    def show(self):
        temp = self.head
        while temp is not None:
            print(temp.val)
            temp = temp.next

if __name__ == "__main__":
    # generating data
    tree = Btree()
    keys = list(range(20))
    #np.random.shuffle(keys)
    data = list(range(10))
    for i in keys:
        temp = tuple([i*j for j in data])
        tree.insert(i, temp)
    tree.show()
    print(tree.find(5))
    print(tree.find(15))







