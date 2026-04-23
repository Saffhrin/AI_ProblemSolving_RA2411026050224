import tkinter as tk
from tkinter import messagebox

# -------------------------------
# CSP Logic (Backtracking)
# -------------------------------

def is_valid(region, color, assignment, neighbors):
    for neighbor in neighbors[region]:
        if neighbor in assignment and assignment[neighbor] == color:
            return False
    return True

def backtrack(assignment, regions, colors, neighbors):
    if len(assignment) == len(regions):
        return assignment

    unassigned = [r for r in regions if r not in assignment][0]

    for color in colors:
        if is_valid(unassigned, color, assignment, neighbors):
            assignment[unassigned] = color
            result = backtrack(assignment, regions, colors, neighbors)
            if result:
                return result
            del assignment[unassigned]

    return None

# -------------------------------
# GUI Application
# -------------------------------

class MapColoringApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Map Coloring Problem (CSP)")

        # Sample Input (as given in assignment)
        self.regions = ["A", "B", "C", "D"]
        self.colors = ["Red", "Green", "Blue"]
        self.neighbors = {
            "A": ["B", "C"],
            "B": ["A", "C", "D"],
            "C": ["A", "B", "D"],
            "D": ["B", "C"]
        }

        tk.Label(root, text="Map Coloring using CSP", font=("Arial", 14)).pack(pady=10)

        tk.Button(root, text="Solve", command=self.solve).pack(pady=10)

        self.result_box = tk.Text(root, height=10, width=35)
        self.result_box.pack()

        self.canvas = tk.Canvas(root, width=300, height=200)
        self.canvas.pack(pady=10)

    def solve(self):
        solution = backtrack({}, self.regions, self.colors, self.neighbors)

        self.result_box.delete("1.0", tk.END)

        if solution:
            self.result_box.insert(tk.END, "Color Assignment:\n\n")
            for region in sorted(solution):
                self.result_box.insert(tk.END, f"{region} → {solution[region]}\n")

            self.draw_map(solution)
        else:
            messagebox.showerror("Error", "No valid coloring found!")

    def draw_map(self, solution):
        self.canvas.delete("all")

        color_map = {
            "Red": "red",
            "Green": "green",
            "Blue": "blue"
        }

        positions = {
            "A": (40, 40),
            "B": (160, 40),
            "C": (40, 120),
            "D": (160, 120)
        }

        for region, (x, y) in positions.items():
            self.canvas.create_oval(x, y, x+60, y+60,
                                    fill=color_map[solution[region]])
            self.canvas.create_text(x+30, y+30, text=region, fill="white")

# -------------------------------
# Run Application
# -------------------------------

if __name__ == "__main__":
    root = tk.Tk()
    app = MapColoringApp(root)
    root.mainloop()
