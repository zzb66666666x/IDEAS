# this is the code for B-tree
from math import ceil


class Btree:
    def __init__(self, order=5):
        self.order = order
        self.min = ceil(order / 2)-1
        self.max = order - 1
        self.root = LinkedList()

    def find(self, key):
        return self.__find(self.root, key)

    def __find(self, root, key):
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
        self.__insert(self.root, key, value)

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
        # the name here: insert to root
        # the root is not the absolute root of the tree, but the relative root whose type is a linked list
        if root.numberKeys < self.max:
            root.insert(key, value, child)
        else:
            # print("seems that too many elements in one list")
            root.insert(key, value, child)
            split_res = root.split(self.order)
            root = split_res[0]
            single_node = split_res[1]
            second_list = split_res[2]
            self.__adjust(root, single_node, second_list)
            return second_list

    def __adjust(self, root, single_node, second_list):
        # print("Begin to adjust things... ")
        if root.parent is None:
            # print("No parent -- create one, the new root")
            new_parent = LinkedList(child=root)
            self.__insert_to_root(new_parent, single_node.key, single_node.data,
                                  second_list)  # this may trigger further split
            root.parent = new_parent
            second_list.parent = new_parent
            self.root = new_parent
        else:
            parent = root.parent
            splitted_list = self.__insert_to_root(parent, single_node.key, single_node.data, second_list)
            if splitted_list is not None:
                splitted_list.child.parent = splitted_list
                for i in splitted_list:
                    i.child.parent = splitted_list

    def delete(self, key):
        self.__delete(self.root, key)

    def __delete(self, root, key):
        if root is None:
            raise Exception("No such key should be deleted")
        node = root.find_loc_for_key(key)
        if node is None:
            self.__delete(root.child, key)
        elif node.key == key:
            # find the one to be deleted
            if node.child is None:
                # delete the leaf node in the leaf list
                self.__delete_in_root(root, key)
            else:
                # transfer the condition to delete a leaf
                temp_key = node.child.first.key
                temp_data = node.child.first.data
                node.key = temp_key
                node.data = temp_data
                self.__delete(node.child, temp_key)
        else:
            self.__delete(node.child, key)

    def __delete_in_root(self, root, key):
        # print(key)
        if root is None:
            return
        if root.numberKeys > self.min:
            root.delete(key)
        else:
            # find brothers
            root.delete(key)
            if root.parent is None:
                if root.numberKeys == 0:
                    self.root = root.child
                return
            left_sibling_tuple = root.parent.left_sibling(root)
            right_sibling_tuple = root.parent.right_sibling(root)
            # choose one to use
            if left_sibling_tuple is not None and left_sibling_tuple[0].numberKeys > self.min:
                # choose left
                left_sibling = left_sibling_tuple[0]
                separator = left_sibling_tuple[1]
                temp_data = separator.data
                temp_key = separator.key
                temp_child = left_sibling.last.child
                separator.key = left_sibling.last.key
                separator.data = left_sibling.last.data
                self.__delete(left_sibling, left_sibling.last.key)  # left_sibling might not be leaf
                self.__insert_to_root(root, temp_key, temp_data, temp_child)
            elif right_sibling_tuple is not None and right_sibling_tuple[0].numberKeys > self.min:
                # choose right
                right_sibling = right_sibling_tuple[0]
                # print("checking right_sibling.first.key", right_sibling.first.key)
                separator = right_sibling_tuple[1]
                temp_data = separator.data
                temp_key = separator.key
                temp_child = right_sibling.child
                separator.key = right_sibling.first.key
                separator.data = right_sibling.first.data
                self.__delete(right_sibling, right_sibling.first.key)   # right_sibling might not be leaf
                self.__insert_to_root(root, temp_key, temp_data, temp_child)
            else:
                # merge things here
                if left_sibling_tuple is not None:
                    # merge_direction = -1 # left
                    left_sibling = left_sibling_tuple[0]
                    separator = left_sibling_tuple[1]
                    # print("the sep has key:", separator.key)
                    # print("the left sibling has the first: ", left_sibling.first.key)
                    self.__insert_to_root(left_sibling, separator.key, separator.data, root.child)
                    left_sibling.extend(root.first)
                    self.__delete_in_root(root.parent, separator.key)
                else:
                    # merge_direction = 1 # right
                    right_sibling = right_sibling_tuple[0]
                    separator = right_sibling_tuple[1]
                    self.__insert_to_root(root, separator.key, separator.data, right_sibling.child)
                    root.extend(right_sibling.first)
                    self.__delete_in_root(root.parent, separator.key)

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
        def __init__(self, key=None, data=None, next=None, child=None):
            self.key = key
            self.data = data
            self.next = next
            self.child = child  # things with larger key

    def __init__(self, parent=None, numberKeys=0, first=None, last=None, child=None):
        self.parent = parent
        self.numberKeys = numberKeys
        self.first = first
        self.last = last
        self.child = child  # things with key < current key

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

    def left_sibling(self, llist):
        # the self here is a parent of llist
        cursor = self.first
        # print(self.first.key)
        if self.child == llist:
            return None
        prev = self
        while cursor is not None:
            if cursor.child == llist:
                return prev.child, cursor
            prev = cursor
            cursor = cursor.next
        raise Exception("No such list exists")

    def right_sibling(self, llist):
        cursor = self.first
        prev = self
        while cursor is not None:
            if prev.child == llist:
                return cursor.child, cursor
            prev = cursor
            cursor = cursor.next
        if prev.child == llist:
            return None
        raise Exception("No such list exists")

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
            return node, new_node
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
            return node, new_node

    def extend(self, node):
        self.last.next = node
        self.adjust()

    def split(self, order):
        # take order == 5, then by the moment this function is called, there will be 5 elements in this list
        # then split it into 1 2; 3; 4 5
        # the middle one which should be picked out for parents should be ceil(order + 1) = 3
        # run through the list to locate the 2, so take counter = 1
        # while counter < 2, move the cursor from 1 to 2, then counter = 2, the next loop will terminate
        # the cursor will be the end of first list
        # cursor.next will be the single node, and the cursor.next.next will be the start of the second new list
        index1 = ceil((order + 1) / 2) - 1
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
        return self, single_node, second_list

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

    def delete(self, key):
        cursor = self.first
        prev = None
        while cursor is not None:
            if cursor.key == key:
                cursor.data = None
                cursor.child = None
                if cursor.next is None:
                    self.last = prev
                if prev is None:
                    # delete the first element
                    self.first = cursor.next
                else:
                    prev.next = cursor.next
                self.numberKeys -= 1
                return True
            prev = cursor
            cursor = cursor.next
        raise IndexError("No such key here")


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
    # np.random.shuffle(keys)
    data = list(range(10))
    for i in keys:
        temp = tuple([i * j for j in data])
        tree.insert(i, temp)
    tree.show()
    print(tree.find(5))
    print(tree.find(15))
    # testing delete
    print("------------")
    tree.delete(0)
    #tree.delete(1)
    #tree.delete(2)
    #tree.delete(3)
    #tree.delete(4)
    #tree.delete(5)
    #tree.delete(6)
    tree.show()
    # print(tree.root.numberKeys)
    # print()
    # for i in tree.root.child:
    #     print(i.key)
    # print(tree.root.first.child)
    # for i in tree.root.first.next.child:
    #     print(i.key)
