from kruskal import Graph
from collections import defaultdict

def find_path(edges):
    # Create a graph
    graph = defaultdict(list)
    for edge in edges:
        point1, point2 = edge
        graph[point1].append(point2)
        graph[point2].append(point1)

    # Use a depth-first search to find the path
    def dfs(node, visited: set, path: list):
        visited.add(node)
        path.append(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                dfs(neighbor, visited, path)
                path.append(node)

    visited = set()
    path = []

    start_point = edges[0][0]
    dfs(start_point, visited, path)

    return path

def trace(coordinates):

    graph = Graph(len(coordinates))
        
    for i in range(len(coordinates)):
        for j in range(i, len(coordinates)):
            graph.addEdge(i, j, ((coordinates[i][0] - coordinates[j][0])**2 + (coordinates[i][1] - coordinates[j][1])**2)**0.5)
            
    tree = graph.KruskalMST()

    return find_path(tree)