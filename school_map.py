school_map = {
    "Main Gate": [("Block A", 5), ("Playground", 3)],
    "Block A": [("Main Gate", 5), ("Library", 4), ("Admin", 2)],
    "Library": [("Block A", 4), ("Lab", 6)],
    "Playground": [("Main Gate", 3)],
    "Admin": [("Block A", 2)],
    "Lab": [("Library", 6)]
}


def find_shortest_path(graph, start, end):
    # Check if locations exist
    if start not in graph or end not in graph:
        return {"path": [], "distance": 0, "status": "error"}

    queue = [(0, start, [])]  # (distance, node, path)
    visited = set()

    while queue:
        queue.sort()  # Prioritize by distance
        dist, node, path = queue.pop(0)

        if node in visited:
            continue

        if node == end:
            return {"path": path + [node], "distance": dist, "status": "success"}

        visited.add(node)

        # Explore neighbors
        for neighbor, weight in graph[node]:
            if neighbor not in visited:
                queue.append((dist + weight, neighbor, path + [node]))

    return {"path": [], "distance": 0, "status": "error"}


# Helper functions
def get_locations():
    return list(school_map.keys())


def is_valid_location(location):
    return location in school_map