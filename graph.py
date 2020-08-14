from queue import Queue
class Graph:
    def __init__(self):
        self.vertices = {}
        
    def add_vertex(self, vertex_id):
        """
        Add a vertex to the graph.
        """
        self.vertices[vertex_id] = set()

    def add_edge(self, v1, v2):
        """
        Add a directed edge to the graph.
        """
        if v1 in self.vertices and v2 in self.vertices:
            self.vertices[v1].add(v2)
        else: 
            raise IndexError("nonexistant vertex")

    def get_neighbors(self, vertex_id):
        """
        Get all neighbors (edges) of a vertex.
        """
        return self.vertices[vertex_id]

    def bfs(self, starting_vertex, destination_vertex):
        """
        Return a list containing the shortest path from
        starting_vertex to destination_vertex in
        breath-first order.
        """
        # create empty queue
        q =  Queue()
        # add starting vertex id
        q.enqueue([starting_vertex])
        # create set for visited 
        visited = set()
        # while queue not
        while q.size() > 0:
            v =  q.dequeue()
            if v[-1] not in visited:
                # print(v)
                visited.add(v[-1])
                for n in self.get_neighbors(v[-1]):
                    new_path = v + [n]
                    if new_path[-1] == destination_vertex:
                        return new_path
                    q.enqueue(new_path)