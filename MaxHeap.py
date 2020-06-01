import numpy as np

class MaxHeap:
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

    def retrieve_max(self):
        return self.heap[1]

    def delete_max(self):
        if len(self.heap) <= 1:
            return None
        maximal_val = self.heap[1]
        self.heap[1] = self.heap[-1]
        self.heap.pop(-1)
        self.sift_down(1)
        return maximal_val

    def sift_down(self, index):
        length = len(self.heap)
        max_index = length - 1
        left = index * 2
        right = index * 2 + 1
        maximal = index
        if left <= max_index and self.heap[left] > self.heap[maximal]:
            maximal = left
        if right <= max_index and self.heap[right] > self.heap[maximal]:
            maximal = right
        if maximal != index:
            self.heap[maximal], self.heap[index] = self.heap[index], self.heap[maximal]
            self.sift_down(maximal)

    def sift_up(self, index):
        parent = index // 2
        if parent >= 1 and self.heap[parent] < self.heap[index]:
            self.heap[parent],self.heap[index] = self.heap[index],self.heap[parent]
            self.sift_up(parent)

    def isEmpty(self):
        if len(self.heap) == 1:
            return True
        return False


if __name__ == "__main__":
    maxheap = MaxHeap()
    maxheap.insert(1)
    maxheap.insert(2)
    maxheap.insert(34)
    maxheap.insert(4)
    maxheap.insert(56)
    maxheap.insert(6)
    maxheap.insert(32)
    print(maxheap.heap)
    while maxheap.isEmpty() is False:
        print(maxheap.delete_max())
    del maxheap
    print("\nanother test!!!\n")
    content = list(range(100))
    np.random.shuffle(content)
    maxheap = MaxHeap(content)
    while maxheap.isEmpty() is False:
        print(maxheap.delete_max())