class WDiGraph:
    def __init__(self, edges=[]):
        # the edges[(1,2,10),(2,3,15),(3,4,10)]
        self.vertexList = VertexList(edges)
        for e in edges:
            self.addEdge(e)
            ## Modification
            # for directed graph, we only need to store one direction - (in, out)

    def addEdge(self, edge):
        # locate the related vertex according to the edge given
        vertex = self.vertexList.locate(edge[0])  # edge[0] is the incoming vertex
        edgelist = vertex.edges  # get the edgelist object for this incoming vertex
        if edgelist != None:
            # add outcoming vertex to the edgelist
            edgelist.add(edge[1], edge[2])
        else:
            # construct a new Edgelist object if this vertex has no edgelist yet
            edgelist = EdgeList(edge[1], edge[2])
        vertex.setEdges(edgelist)

    def __iter__(self):
        vertices = self.vertexList
        for v in vertices:
            x = vertices.locate(v)
            y = x.edges
            if y != None:
                for z in y:
                    yield (v, z[0], z[1])

    def insertVertex(self, item):
        if not (item in self.vertexList):
            self.vertexList.append(item)

    def deleteVertex(self, item):
        return self.vertexList.remove(item)

    def insertEdge(self, edge):
        self.vertexList.addVertex(edge)
        self.addEdge(edge)
        ## Modification, only one direction now
        # self.addEdge((edge[1],edge[0]))

    def deleteEdge(self, edge):
        self.__deleteEdge(edge)
        ## Modification, only one direction now

    def __deleteEdge(self, edge):
        if not (edge[0] in self.vertexList):
            print("There is no edge", edge)
            return False
        vertexlocation = self.vertexList.locate(edge[0])
        edgelist = vertexlocation.getEdges()
        if edgelist == None:
            print("There is no edge", edge)
            return False
        res = edgelist.remove(edge[1])
        if res == False:
            print("There is no edge", edge)
        return res

    def outgoingEdges(self, item):
        vertex = self.vertexList.locate(item)
        if vertex == None:
            print("There is no vertex", item)
            return []
        edgelist = vertex.getEdges()
        if edgelist == None:
            return []
        res = []
        for v in edgelist:
            res.append((item, v[0], v[1]))
        return res
        # yield (item,v) # If we replace the above two lines with this line, then this methods works as an iterator.

    def dfs(self, root):
        numVertices = self.vertexList.getlength()
        self.mark = [None] * numVertices
        self.dfsNum = [1] * numVertices
        self.finishTime = [1] * numVertices
        self.dfsPos = 1
        self.finishingTime = 1
        graph = WDiGraph()
        index = self.vertexList.index(root)
        self.mark[index] = root
        self.dfsPos += 1
        self.__dfs(root, graph)
        return graph

    def __dfs(self, root, graph):
        index = self.vertexList.index(root)
        for edge in self.outgoingEdges(root):
            # print("the edges are: ",edge)
            next_index = self.vertexList.index(edge[1])
            if self.mark[next_index] is None:
                self.mark[next_index] = root
                self.dfsNum[next_index] = self.dfsPos
                self.dfsPos += 1
                graph.insertEdge(edge)
                self.__dfs(edge[1], graph)
        self.finishTime[index] = self.finishingTime
        self.finishingTime += 1

    def path(self, root, target):
        numVertices = self.vertexList.getlength()
        self.mark = [None]*numVertices
        stk = Stack()
        self.__search_path(root, target, stk)
        if stk.isEmpty():
            return None
        path = WDiGraph()
        while stk.isEmpty() is False:
            edge = stk.pop()
            path.insertEdge(edge)
        return path

    def __search_path(self, root, target, stk):
        if root == target:
            return True
        for edge in self.outgoingEdges(root):
            next_index = self.vertexList.index(edge[1])
            if self.mark[next_index] is None:
                self.mark[next_index] = root
                if self.__search_path(edge[1], target, stk):
                    stk.push(edge)
                    return True
        return False

# Definition of VertexList Class, a linked list
class VertexList:
    class __Vertex:
        def __init__(self, item, next=None, previous=None):
            self.item = item  # the vertex content
            self.next = next
            self.previous = previous
            self.edges = None  # vertices related to this vertex

        def getItem(self):
            return self.item

        def getNext(self):
            return self.next

        def getPrevious(self):
            return self.previous

        def getEdges(self):
            return self.edges

        def setItem(self, item):
            self.item = item

        def setNext(self, next):
            self.next = next

        def setPrevious(self, previous):
            self.previous = previous

        def setEdges(self, edge):
            self.edges = edge

    def __init__(self, edges=[]):
        self.dummy = VertexList.__Vertex(None, None, None)
        self.numVertices = 0
        self.dummy.setNext(self.dummy)
        self.dummy.setPrevious(self.dummy)
        for e in edges:
            self.addVertex(e)

    def __iter__(self):
        cursor = self.dummy
        for i in range(self.numVertices):
            cursor = cursor.getNext()
            yield cursor.getItem()

    def append(self, item):
        lastVertex = self.dummy.getPrevious()
        newVertex = VertexList.__Vertex(item, self.dummy, lastVertex)
        lastVertex.setNext(newVertex)
        self.dummy.setPrevious(newVertex)
        self.numVertices += 1

    def __contains__(self, item):
        cursor = self.dummy
        for i in range(self.numVertices):
            cursor = cursor.getNext()
            vertex = cursor.getItem()
            if vertex == item:
                return True
        return False

    def __getitem__(self, index):
        if index >= self.numVertices:
            return None
        temp_index = 0
        for i in self:
            if temp_index == index:
                return i
            temp_index += 1

    # locate the vertex location using its vertex value
    def locate(self, vertex):
        cursor = self.dummy
        for i in range(self.numVertices):
            cursor = cursor.getNext()
            item = cursor.getItem()
            if vertex == item:
                return cursor

    # add new vertex if possible for the new edge
    def addVertex(self, edge):
        node1 = edge[0]
        node2 = edge[1]
        if not (node1 in self):
            self.append(node1)
        if not (node2 in self):
            self.append(node2)

    # remove a vertex
    def remove(self, vertex):
        cursor = self.dummy
        location = None
        for i in range(self.numVertices):
            cursor = cursor.getNext()
            cursor_info = cursor.getItem()
            edgelist = cursor.edges
            if edgelist != None:
                if vertex in edgelist:
                    print(vertex, "cannot be deleted, as it appears in an edge.")
                    return False
            if vertex == cursor_info:
                location = cursor
        if location == None:
            print(vertex, "is not a vertex.")
            return False
        nextVertex = location.getNext()
        prevVertex = location.getPrevious()
        prevVertex.setNext(nextVertex)
        nextVertex.setPrevious(prevVertex)
        self.numVertices -= 1
        return True

    def index(self, item):
        cursor = self.dummy
        for i in range(self.numVertices):
            cursor = cursor.getNext()
            if cursor.getItem() == item:
                return i
        return -1

    def getlength(self):
        return self.numVertices


# Definition of EdgeList Class, also a linked list
class EdgeList:
    class __Edge:
        def __init__(self, item, length, next=None, previous=None):
            self.item = item
            self.length = length
            self.next = next
            self.previous = previous

        def getItem(self):
            return self.item, self.length

        def getNext(self):
            return self.next

        def getPrevious(self):
            return self.previous

        def setItem(self, vertex, length):
            self.item = vertex
            self.length = length

        def setNext(self, next):
            self.next = next

        def setPrevious(self, previous):
            self.previous = previous

    def __init__(self, nextvertex, length):
        self.first = EdgeList.__Edge(nextvertex, length, None, None)
        self.first.setNext(self.first)
        self.first.setPrevious(self.first)
        self.numEdges = 1

    def add(self, nextvertex, length):
        lastEdge = self.first.getPrevious()
        newEdge = EdgeList.__Edge(nextvertex, length, self.first, lastEdge)
        lastEdge.setNext(newEdge)
        self.first.setPrevious(newEdge)
        self.numEdges += 1

    def __iter__(self):
        cursor = self.first
        for i in range(self.numEdges):
            yield cursor.getItem()
            cursor = cursor.getNext()

    def __contains__(self, vertex):
        cursor = self.first
        for i in range(self.numEdges):
            item = cursor.getItem()
            if vertex == item[0]:
                return True
            cursor = cursor.getNext()
        return False

    def remove(self, vertex):
        cursor = self.first
        for i in range(self.numEdges):
            item = cursor.getItem()
            if vertex == item[0]:
                nextVertex = cursor.getNext()
                prevVertex = cursor.getPrevious()
                prevVertex.setNext(nextVertex)
                nextVertex.setPrevious(prevVertex)
                self.numEdges -= 1
                if (cursor == self.first):
                    self.first = nextVertex
                return True
            cursor = cursor.getNext()
        return False

class Stack(object):
    class Node(object):
        def __init__(self, val):
            self.val = val
            self.next = None

    def __init__(self):
        self.head = None

    def top(self):
        if self.head is not None:
            return self.head.val
        else:
            return None

    def push(self, n):
        n = self.Node(n)
        n.next = self.head
        self.head = n
        return n.val

    def pop(self):
        if self.head is None:
            return None
        else:
            tmp = self.head.val
            self.head = self.head.next
            return tmp

    def isEmpty(self):
        if self.head is None:
            return True
        else:
            return False

    def show(self):
        if self.head is None:
            return
        temp = self.head
        while temp is not None:
            temp = temp.next

    def __iter__(self):
        if self.head is None:
            return
        temp = self.head
        while temp is not None:
            yield temp.val
            temp = temp.next