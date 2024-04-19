import heapq
import json

class APSP:
    def __init__(self, graph):
        self.graph = graph
        self.outputFile = "routing_tables.json"

    def run(self):

        def dijkstra(graph, start):
            distances = {vertex: float('infinity') for vertex in graph}
            distances[start] = 0
            predecessor = {vertex: None for vertex in graph}
            priority_queue = [(0, start)]

            while priority_queue:
                current_distance, current_vertex = heapq.heappop(priority_queue)

                if current_distance > distances[current_vertex]:
                    continue

                for neighbor, weight in graph[current_vertex].items():
                    distance = current_distance + weight

                    if distance < distances[neighbor]:
                        distances[neighbor] = distance
                        predecessor[neighbor] = current_vertex
                        heapq.heappush(priority_queue, (distance, neighbor))
            
            return distances, predecessor

        def get_next_hop(predecessor, start, destination):
            # Traverse the predecessor chain to find the next hop from start to destination
            current = destination
            while predecessor[current] and predecessor[current] != start:
                current = predecessor[current]
            return current if current != start else None

        # Generate routing tables for each node
        routing_tables = {}
        for node in self.graph:
            distances, predecessors = dijkstra(self.graph, node)
            routing_table = {}
            for destination in self.graph:
                if destination != node:
                    next_hop = get_next_hop(predecessors, node, destination)
                    routing_table[destination] = {"distance": distances[destination], "next_hop": next_hop}
            routing_tables[node] = routing_table
            
        with open(self.outputFile, "w") as f:
            json.dump(routing_tables, f)





