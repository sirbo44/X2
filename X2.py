class Graph:
    def __init__(self) -> None:
        self.vertices = {}
        self.shortest_path = ""
        self.paths = []

    def add_vertex(self, id):
        if id in self.vertices:
            print("Vertex already exists")
        else: 
            vertex = Vertex(id)
            self.vertices[id] = vertex

    def add_edges(self, ida, idb, likes=1, comments=1):
        if ida in self.vertices and idb in self.vertices:
            data = []
            data.append(likes)
            data.append(comments)
            edge = Edge(idb, data)
            self.vertices[ida].add_edge(idb, edge)     
            for v in self.vertices:
                total_likes = 0
                total_comments = 0
                followers = 0
                for v2 in self.vertices:
                    if v2 == v:
                        continue
                    else:
                        for e in self.vertices[v2].edges:
                            if e == v:
                                followers += 1
                for e in self.vertices[v].edges:
                    total_likes += self.vertices[v].edges[e].data[0]
                    total_comments += self.vertices[v].edges[e].data[1]
                self.vertices[v].engagement = engagementCalculator(total_likes, total_comments, followers)
                for e in self.vertices[v].edges:
                    self.vertices[v].influence = influenceCalculator(self.vertices[v].edges[e].data[0], self.vertices[v].edges[e].data[1], self.vertices[v].engagement)

    def display(self):
        for v in self.vertices:
            print(v, end=". ")
            print("Edges: ", end="")
            for e in self.vertices[v].edges:
                print("| {} ({}) |".format(e,  self.vertices[v].influence), end="")
            print(" \t Eng:", self.vertices[v].engagement)                  

    def bfs(self, start):
        if start not in self.vertices:
            print("No starting point found")
            return
        for v in self.vertices:
            self.vertices[v].init_bfs()
        queue = []
        queue.append(self.vertices[start])
        self.vertices[start].color = "gray"
        self.vertices[start].distance = 0
        while len(queue) > 0:
            vertex = queue.pop(0)
            for e in vertex.edges:
                did = vertex.edges[e].destination
                destination = self.vertices[did]
                if destination.color == "white":
                    destination.color = "gray"
                    destination.parent = vertex
                    destination.distance = vertex.distance + 1
                    queue.append(destination)
            vertex.color = "black"

    def print_shortest_path(self, start, dest):
        start_vertex = self.vertices[start]
        dest_vertex = self.vertices[dest]
        if dest_vertex.parent is not None:
            self.print_shortest_path(start, dest_vertex.parent.id)
        elif dest != start:
            self.shortest_path = "No path from start to dest"
            return
        self.shortest_path += str(dest) + ' ' 

    def relax(self, va, vb, w):
        if vb.distance > va.distance + w:
            vb.distance = va.distance + w
            vb.parent = va

    def dijkstra(self, start):
        for v in self.vertices:
            self.vertices[v].init_bfs()
        self.vertices[start].distance = 0
        Q = []
        for vertex in self.vertices:
            Q.append(self.vertices[vertex])
        Q.sort(key=lambda x : x.distance)
        while(len(Q) > 0):
            u = Q.pop(0)
            for edge in u.edges:
                v = self.vertices[edge]
                w = u.edges[edge].influence
                self.relax(u, v, w)
            Q.sort(key=lambda x : x.distance)
    
    def dfs(self, start, end, visited=None, path=None):
        if visited is None:
            visited = set()
        if path is None:
            path = []

        visited.add(start)
        path.append(start)

        if start == end:
            self.paths.append(list(path))
        else:
            for neighbor in self.vertices[start].edges:
                if neighbor not in visited:
                    self.dfs(neighbor, end, visited, path)

        path.pop()
        visited.remove(start)

    def get_all_paths(self, start, end):
        self.paths = []
        self.dfs(start, end)
        return self.paths

    def max_engagement(self, paths):
        max = -1
        for path in paths:
            s = 0
            for v in path:
                s += self.vertices[v].engagement
            if s > max:
                max = s
                max_path = path
        
        max_path = ' '.join(list(map(str, max_path)))
        print("Path with the highest engagement rate:", max_path, "Engagement rate:", max)


class Vertex:
    def __init__(self, id) -> None:
        self.id = id
        self.engagement = 0
        self.edges = {}
        # additional values
        self.distance = 0
        self.color = "white"
        self.parent = None

    def add_edge(self, idb, edge):
        self.edges[idb] = edge

    def init_bfs(self):
        self.distance = float("inf")
        self.color = "white"
        self.parent = None


class Edge:
    def __init__(self, d,  data=[]) -> None:
        self.destination = d
        self.influence = 0
        self.data = data

def engagementCalculator(likes: int, comments: int, followers: int) -> float:
    if followers != 0:
        return (likes+comments)/followers * 100
    else:
        return 0

def influenceCalculator(likes_a_to_b: int, comments_a_to_b: int, engagement_of_a: float) -> float: 
    if engagement_of_a != 0:
        return (likes_a_to_b + comments_a_to_b)/ engagement_of_a
    else:
        return 0


if __name__=="__main__":
    # create a graph
    graph = Graph()
    # create 7 vertices
    for i in range(1,8):
        graph.add_vertex(i)
    # add edges to connect vertices 
    graph.add_edges(1,3,100,100)
    graph.add_edges(1,2,400,50)
    graph.add_edges(3,2,800,250)
    graph.add_edges(3,4,200,300)
    graph.add_edges(4,2,300,700)
    graph.add_edges(3,5,190,800)
    graph.add_edges(4,6,900,400)
    graph.add_edges(5,6,1000,300)
    graph.add_edges(6,7,10,2100)
    # display the graph
    graph.display()
    # use Dijkstra algorithm to the graph 
    graph.dijkstra(1)
    print("#################")
    # use BFS algorithm to the graph
    graph.bfs(1)
    # use print_shortest_path() function to create a string of the path 
    graph.print_shortest_path(1,7)
    # display the path if exists or an error message
    print(graph.shortest_path)
    # find all paths from 1 to 7 using get_all_paths() function
    all_paths = graph.get_all_paths(1, 7)
    # use the max_engagement function to find the path with the highest engagement value and print it accordingly
    graph.max_engagement(all_paths)

    
    

