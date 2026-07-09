from collections import deque

# Social Network Graph (Undirected)
graph = {
    "Alice": ["Charlie", "David"],
    "Bob": ["Emma", "Fred"],
    "Charlie": ["Alice", "Emma"],
    "David": ["Alice", "Emma", "Fred"],
    "Emma": ["Bob", "Charlie", "David"],
    "Fred": ["Bob", "David"]
}

# Sort neighbors alphabetically
for node in graph:
    graph[node].sort()


# ---------------- BFS ---------------- #
def bfs(graph, start, goal):
    queue = deque([(start, [start])])
    visited = set([start])

    print("\n========== BREADTH FIRST SEARCH ==========")
    step = 1

    while queue:
        print(f"\nStep {step}")
        print("Queue:", [node for node, path in queue])
        print("Visited:", list(visited))

        current, path = queue.popleft()

        if current == goal:
            print("\nGoal Found!")
            return path

        for neighbor in graph[current]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))

        step += 1

    return None


# ---------------- DFS ---------------- #
def dfs(graph, start, goal):
    stack = [(start, [start])]
    visited = set()

    print("\n========== DEPTH FIRST SEARCH ==========")
    step = 1

    while stack:
        print(f"\nStep {step}")
        print("Stack:", [node for node, path in stack])
        print("Visited:", list(visited))

        current, path = stack.pop()

        if current not in visited:
            visited.add(current)

            if current == goal:
                print("\nGoal Found!")
                return path

            # Reverse alphabetical order so traversal happens alphabetically
            for neighbor in sorted(graph[current], reverse=True):
                if neighbor not in visited:
                    stack.append((neighbor, path + [neighbor]))

        step += 1

    return None


# ---------------- Main ---------------- #
start = "Alice"
goal = "Bob"

bfs_path = bfs(graph, start, goal)
print("\nShortest Path using BFS:")
print(" -> ".join(bfs_path))

dfs_path = dfs(graph, start, goal)
print("\nPath Found using DFS:")
print(" -> ".join(dfs_path))