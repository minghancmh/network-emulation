import heapq
import json

class APSP:
    def __init__(self, inputFile, fn):
        self.inputFile = inputFile+"_" + str(fn) + ".json"
        self.outputFile = "routing_tables.json"

    def run(self):
        # Load JSON data from a file
        with open(self.inputFile, "r") as file:
            connections_data = json.load(file)["connections"]

        for connection in connections_data:
            destn = connection["destination_id"]
            src = connection["source_id"]
            destn_num = int(destn[-1])
            src_num = int(src[-1])
            if (destn_num == 1):
                connection["destination_id"] = "test-cluster-worker"
            else:
                connection["destination_id"] = "test-cluster-worker" + str(destn_num)
            if (src_num == 1):
                connection["source_id"] = "test-cluster-worker"
            else:
                connection["source_id"] = "test-cluster-worker" + str(src_num)



        # Initialize an empty graph
        graph = {}

        # Populate the graph with connections
        for connection in connections_data:
            src = connection["source_id"]
            dest = connection["destination_id"]
            # Assuming weight of each edge is 1
            if src not in graph:
                graph[src] = {}
            if dest not in graph:
                graph[dest] = {}
            graph[src][dest] = 1
            graph[dest][src] = 1  # Assuming undirected graph; remove if directed

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
        for node in graph:
            distances, predecessors = dijkstra(graph, node)
            routing_table = {}
            for destination in graph:
                if destination != node:
                    next_hop = get_next_hop(predecessors, node, destination)
                    routing_table[destination] = {"distance": distances[destination], "next_hop": next_hop}
            routing_tables[node] = routing_table
            
        with open(self.outputFile, "w") as f:
            json.dump(routing_tables, f)



