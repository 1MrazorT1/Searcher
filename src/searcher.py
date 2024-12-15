import tkinter as tk
from collections import deque

GRID_SIZE = 10
CELL_SIZE = 10

grid_state = []
current_algo = ""

app = tk.Tk()
app.title("Searcher")
app.geometry("800x600")
app.resizable(True, True)

def bfs(canvas, start_row, start_col):
    rows, cols = len(grid_state), len(grid_state[0])
    visited = [[False for _ in range(cols)] for _ in range(rows)]
    queue = deque([(start_row, start_col, [])])

    while queue:
        row, col, path = queue.popleft()
        if row < 0 or row >= rows or col < 0 or col >= cols or visited[row][col]:
            continue
        if grid_state[row][col] == "white":
            continue
        visited[row][col] = True
        new_path = path + [(row, col)]
        if grid_state[row][col] == "green":
            return new_path
        queue.append((row - 1, col, new_path))
        queue.append((row + 1, col, new_path))
        queue.append((row, col - 1, new_path))
        queue.append((row, col + 1, new_path))

    return None

def dfs(canvas, start_row, start_col):
    rows, cols = len(grid_state), len(grid_state[0])
    visited = [[False for _ in range(cols)] for _ in range(rows)]
    stack = [(start_row, start_col, [])]

    while stack:
        row, col, path = stack.pop()
        if row < 0 or row >= rows or col < 0 or col >= cols or visited[row][col]:
            continue
        if grid_state[row][col] == "white":
            continue
        visited[row][col] = True
        new_path = path + [(row, col)]
        if grid_state[row][col] == "green":
            return new_path
        stack.append((row - 1, col, new_path))
        stack.append((row + 1, col, new_path))
        stack.append((row, col - 1, new_path))
        stack.append((row, col + 1, new_path))

    return None

import heapq

def ucs(canvas, start_row, start_col):
    rows, cols = len(grid_state), len(grid_state[0])
    visited = [[False for _ in range(cols)] for _ in range(rows)]
    pq = [(0, start_row, start_col, [])]
    while pq:
        cost, row, col, path = heapq.heappop(pq)
        if row < 0 or row >= rows or col < 0 or col >= cols or visited[row][col]:
            continue
        if grid_state[row][col] == "white":
            continue
        visited[row][col] = True
        new_path = path + [(row, col)]
        if grid_state[row][col] == "green":
            return new_path
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            heapq.heappush(pq, (cost + 1, row + dr, col + dc, new_path))

    return None


def heuristic(row, col, target_row, target_col):
    """Manhattan distance heuristic."""
    return abs(row - target_row) + abs(col - target_col)

def gbfs(canvas, start_row, start_col):
    rows, cols = len(grid_state), len(grid_state[0])
    visited = [[False for _ in range(cols)] for _ in range(rows)]
    pq = []
    target = None
    for r in range(rows):
        for c in range(cols):
            if grid_state[r][c] == "green":
                target = (r, c)
                break

    if not target:
        print("Target not found!")
        return None

    target_row, target_col = target
    heapq.heappush(pq, (0, start_row, start_col, []))

    while pq:
        _, row, col, path = heapq.heappop(pq)
        if row < 0 or row >= rows or col < 0 or col >= cols or visited[row][col]:
            continue
        if grid_state[row][col] == "white":
            continue
        visited[row][col] = True
        new_path = path + [(row, col)]
        if grid_state[row][col] == "green":
            return new_path
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            h = heuristic(row + dr, col + dc, target_row, target_col)
            heapq.heappush(pq, (h, row + dr, col + dc, new_path))

    return None


def a_star(canvas, start_row, start_col):
    rows, cols = len(grid_state), len(grid_state[0])
    visited = [[False for _ in range(cols)] for _ in range(rows)]
    pq = []
    target = None
    for r in range(rows):
        for c in range(cols):
            if grid_state[r][c] == "green":
                target = (r, c)
                break
    if not target:
        print("Target not found!")
        return None
    target_row, target_col = target
    heapq.heappush(pq, (0, 0, start_row, start_col, []))

    while pq:
        _, g, row, col, path = heapq.heappop(pq)
        if row < 0 or row >= rows or col < 0 or col >= cols or visited[row][col]:
            continue
        if grid_state[row][col] == "white":
            continue
        visited[row][col] = True
        new_path = path + [(row, col)]
        if grid_state[row][col] == "green":
            return new_path
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            h = heuristic(row + dr, col + dc, target_row, target_col)
            heapq.heappush(pq, (g + 1 + h, g + 1, row + dr, col + dc, new_path))

    return None

def load_grid(file_dir, algorithm):
    global grid_state
    grid_state = []
    with open(file_dir, "r") as file:
        first_line = file.readline().strip()
        numbers = first_line.split()
        col = int(numbers[0])
        ln = int(numbers[1])
        canvas = tk.Canvas(app, width=col * CELL_SIZE, height=ln * CELL_SIZE, bg="black")
        canvas.pack()
        for i in range(ln):
            line = file.readline().strip()
            row = []
            for j, char in enumerate(line):
                x0 = j * CELL_SIZE
                y0 = i * CELL_SIZE
                x1 = x0 + CELL_SIZE
                y1 = y0 + CELL_SIZE
                if char == "#":
                    color = "black"
                elif char == "~":
                    color = "red"
                elif char == "=":
                    color = "green"
                else:
                    color = "white"

                canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="grey")
                row.append(color)
            grid_state.append(row)
        canvas.bind("<Button-1>", lambda event: on_canvas_click(event, canvas))
    return canvas

def on_canvas_click(event, canvas):
    reset_graph(canvas)
    global current_algo
    col = event.x // CELL_SIZE
    row = event.y // CELL_SIZE
    if 0 <= row < len(grid_state) and 0 <= col < len(grid_state[0]):
        if grid_state[row][col] == "white":
            print("Cannot start from a wall!")
            return
        path = None
        if current_algo == "BFS":
            path = bfs(canvas, row, col)
        elif current_algo == "DFS":
            path = dfs(canvas, row, col)
        elif current_algo == "UCS":
            path = ucs(canvas, row, col)
        elif current_algo == "GBFS":
            path = gbfs(canvas, row, col)
        elif current_algo == "ASTAR":
            path = a_star(canvas, row, col)
        if path:
            for r, c in path:
                x0 = c * CELL_SIZE
                y0 = r * CELL_SIZE
                x1 = x0 + CELL_SIZE
                y1 = y0 + CELL_SIZE
                if grid_state[r][c] == "black":
                    canvas.create_rectangle(x0, y0, x1, y1, fill="blue", outline="grey")
                    grid_state[r][c] = "blue"
                elif grid_state[r][c] == "red":
                    canvas.create_rectangle(x0, y0, x1, y1, fill="cyan", outline="grey")
                    grid_state[r][c] = "cyan"
            print("Path found and colored!")
        else:
            print("No path to the target!")

def set_algorithm(algorithm, algorithms_window):
    global current_algo
    current_algo = algorithm
    display_current_algorithm(f"Current algorithm selected: {algorithm}")
    algorithms_window.destroy()

def display_current_algorithm(algorithm):
    label = tk.Label(app, text=algorithm)
    label.pack()

def reset_graph(canvas):
    reset_mapping = {
        "blue": "black",
        "cyan": "red"
    }

    for i in range(len(grid_state)):
        for j in range(len(grid_state[i])):
            if grid_state[i][j] in reset_mapping:
                x0 = j * CELL_SIZE
                y0 = i * CELL_SIZE
                x1 = x0 + CELL_SIZE
                y1 = y0 + CELL_SIZE
                original_color = reset_mapping[grid_state[i][j]]
                canvas.create_rectangle(x0, y0, x1, y1, fill=original_color, outline="grey")
                grid_state[i][j] = original_color

def list_algorithms_buttons():
    """Creates buttons to select algorithms."""
    algorithms_window = tk.Toplevel(app)
    algorithms_window.title("Algorithms")
    algorithms_window.geometry("400x400")
    tk.Button(algorithms_window, text="BFS", command=lambda: set_algorithm("BFS", algorithms_window)).pack()
    tk.Button(algorithms_window, text="DFS", command=lambda: set_algorithm("DFS", algorithms_window)).pack()
    tk.Button(algorithms_window, text="UCS", command=lambda: set_algorithm("UCS", algorithms_window)).pack()
    tk.Button(algorithms_window, text="GBFS", command=lambda: set_algorithm("GBFS", algorithms_window)).pack()
    tk.Button(algorithms_window, text="ASTAR", command=lambda: set_algorithm("ASTAR", algorithms_window)).pack()



tk.Button(app, text="Choose search-algorithm", command=lambda: list_algorithms_buttons()).pack()

canvas = load_grid("../assets/starter_virage_sable.txt", current_algo)
tk.Button(app, text="RESET GRAPH", command=lambda: reset_graph(canvas)).pack()

app.mainloop()
