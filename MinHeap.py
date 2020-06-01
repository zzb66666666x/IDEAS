import numpy as np

class MinHeap:
    # Root: A[1]
    # Node A[n]
    # Node.left A[2n]
    # Node.right A[2n+1]
    # Node.parent A[n//2]
    # heap: [None, 1,2,3,4,5,6,7,8,10,...]
    def __init__(self, content=[]):
        self.heap = [None]+content
        self.build_heap()

    def build_heap(self):
        for i in range(int(len(self.heap) / 2), 0, -1):
            self.sift_down(i)

    def insert(self, val):
        self.heap.append(val)
        self.sift_up(len(self.heap)-1)

    def retrieve_min(self):
        return self.heap[1]

    def delete_min(self):
        if len(self.heap) <= 1:
            return None
        minimal_val = self.heap[1]
        self.heap[1] = self.heap[-1]
        self.heap.pop(-1)
        self.sift_down(1)
        return minimal_val

    def sift_down(self, index):
        length = len(self.heap)
        max_index = length - 1
        left = index * 2
        right = index * 2 + 1
        minimal = index
        if left <= max_index and self.heap[left] < self.heap[minimal]:
            minimal = left
        if right <= max_index and self.heap[right] < self.heap[minimal]:
            minimal = right
        if minimal != index:
            self.heap[minimal], self.heap[index] = self.heap[index], self.heap[minimal]
            self.sift_down(minimal)

    def sift_up(self, index):
        parent = index // 2
        if parent >= 1 and self.heap[parent] > self.heap[index]:
            self.heap[parent],self.heap[index] = self.heap[index],self.heap[parent]

    def isEmpty(self):
        if len(self.heap) == 1:
            return True
        return False


if __name__ == "__main__":
    minheap = MinHeap()
    minheap.insert(1)
    minheap.insert(2)
    minheap.insert(34)
    minheap.insert(4)
    minheap.insert(56)
    minheap.insert(6)
    minheap.insert(32)
    print(minheap.heap)
    while minheap.isEmpty() is False:
        print(minheap.delete_min())
    del minheap
    print("\nanother test!!!\n")
    content = list(range(100))
    np.random.shuffle(content)
    minheap = MinHeap(content)
    while minheap.isEmpty() is False:
        print(minheap.delete_min())