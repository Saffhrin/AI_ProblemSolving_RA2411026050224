"""
Map Coloring Problem — Constraint Satisfaction Problem (CSP)
============================================================
Algorithm : Backtracking Search with MRV (Minimum Remaining Values) heuristic
            and Forward Checking.

Usage
-----
    python map_coloring_csp.py          # launches the Tkinter GUI
    python map_coloring_csp.py --cli    # runs the built-in sample in the terminal

Sample Input (matches the assignment brief)
-------------------------------------------
    Regions    : A, B, C, D
    Adjacency  : A-B, A-C, B-C, B-D, C-D
    Colors     : Red, Green, Blue

Expected Output
---------------
    A → Red
    B → Green
    C → Blue
    D → Red
"""

import sys
import tkinter as tk
from tkinter import ttk, messagebox
import math


# ─── CSP Core ────────────────────────────────────────────────────────────────

class MapColoringCSP:
    """
    Represents a map-coloring problem as a CSP.

    Attributes
    ----------
    regions   : list[str]       all region names
    neighbors : dict[str, set]  adjacency list
    colors    : list[str]       available colors
    """

    def __init__(self, regions: list[str], adjacency: list[tuple[str, str]],
                 colors: list[str]):
        self.regions = list(regions)
        self.colors = list(colors)
        self.neighbors: dict[str, set] = {r: set() for r in regions}
        for a, b in adjacency:
            if a in self.neighbors and b in self.neighbors:
                self.neighbors[a].add(b)
                self.neighbors[b].add(a)
        self.trace: list[str] = []      # algorithm steps for display

    # ── helpers ──────────────────────────────────────────────────────────────

    def _is_consistent(self, region: str, color: str,
                       assignment: dict[str, str]) -> bool:
        """Return True if `color` does not conflict with already-assigned neighbors."""
        return all(assignment.get(n) != color for n in self.neighbors[region])

    def _mrv_variable(self, assignment: dict[str, str]) -> str | None:
        """
        Select the unassigned variable with the fewest legal colors
        (Minimum Remaining Values heuristic).
        """
        unassigned = [r for r in self.regions if r not in assignment]
        if not unassigned:
            return None
        return min(unassigned,
                   key=lambda r: sum(
                       self._is_consistent(r, c, assignment)
                       for c in self.colors
                   ))

    def _forward_check(self, region: str, color: str,
                       assignment: dict[str, str]) -> bool:
        """
        After assigning `color` to `region`, ensure every unassigned neighbor
        still has at least one legal color remaining.
        """
        for n in self.neighbors[region]:
            if n not in assignment:
                if not any(self._is_consistent(n, c, assignment)
                           for c in self.colors):
                    return False
        return True

    # ── solver ───────────────────────────────────────────────────────────────

    def solve(self) -> dict[str, str] | None:
        """
        Run backtracking search with MRV + forward checking.

        Returns
        -------
        assignment dict if a solution is found, else None.
        """
        self.trace = []
        result = self._backtrack({})
        return result

    def _backtrack(self, assignment: dict[str, str]) -> dict[str, str] | None:
        if len(assignment) == len(self.regions):
            return dict(assignment)                          # complete assignment

        region = self._mrv_variable(assignment)
        if region is None:
            return None

        for color in self.colors:
            if self._is_consistent(region, color, assignment):
                assignment[region] = color
                self.trace.append(f"assign  {region:>6}  →  {color}")

                if self._forward_check(region, color, assignment):
                    result = self._backtrack(assignment)
                    if result is not None:
                        return result

                self.trace.append(f"backtrack {region} (conflict with {color})")
                del assignment[region]

        return None


# ─── CLI mode ────────────────────────────────────────────────────────────────

def run_cli():
    print("=" * 50)
    print("  Map Coloring CSP — Sample Run")
    print("=" * 50)

    regions    = ["A", "B", "C", "D"]
    adjacency  = [("A","B"),("A","C"),("B","C"),("B","D"),("C","D")]
    colors     = ["Red", "Green", "Blue"]

    print(f"\nRegions   : {', '.join(regions)}")
    print(f"Adjacency : {', '.join(f'{a}-{b}' for a,b in adjacency)}")
    print(f"Colors    : {', '.join(colors)}\n")

    csp = MapColoringCSP(regions, adjacency, colors)
    solution = csp.solve()

    if solution:
        print("Solution found:\n")
        for r in regions:
            print(f"  {r}  →  {solution[r]}")
        print("\nAlgorithm trace (first 20 steps):")
        for step in csp.trace[:20]:
            print(f"  {step}")
    else:
        print("No solution exists with the given colors.")


# ─── Tkinter GUI ─────────────────────────────────────────────────────────────

COLOR_HEX = {
    "Red":    "#E24B4A",
    "Green":  "#4CAF50",
    "Blue":   "#378ADD",
    "Yellow": "#F5C542",
    "Purple": "#7F77DD",
    "Teal":   "#1D9E75",
}


class MapColoringApp(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Map Coloring — CSP Solver")
        self.resizable(True, True)
        self.configure(bg="#f5f5f0")
        self._build_ui()
        self._load_sample()

    # ── UI construction ───────────────────────────────────────────────────────

    def _build_ui(self):
        pad = dict(padx=10, pady=6)

        # ── left panel ──────────────────────────────────────────────────────
        left = tk.Frame(self, bg="#f5f5f0")
        left.grid(row=0, column=0, sticky="nsew", **pad)

        tk.Label(left, text="Regions (one per line)",
                 bg="#f5f5f0", font=("Helvetica", 11, "bold")).pack(anchor="w")
        self.regions_txt = tk.Text(left, width=18, height=8,
                                   font=("Courier", 11))
        self.regions_txt.pack(fill="x")

        tk.Label(left, text="Adjacency (e.g. A-B)",
                 bg="#f5f5f0", font=("Helvetica", 11, "bold")).pack(anchor="w",
                                                                      pady=(8,0))
        self.adj_txt = tk.Text(left, width=18, height=10,
                                font=("Courier", 11))
        self.adj_txt.pack(fill="x")

        tk.Label(left, text="Colors (one per line)",
                 bg="#f5f5f0", font=("Helvetica", 11, "bold")).pack(anchor="w",
                                                                      pady=(8,0))
        self.colors_txt = tk.Text(left, width=18, height=5,
                                   font=("Courier", 11))
        self.colors_txt.pack(fill="x")

        btn_frame = tk.Frame(left, bg="#f5f5f0")
        btn_frame.pack(fill="x", pady=10)
        tk.Button(btn_frame, text="  Solve  ", command=self._solve,
                  bg="#1a1a1a", fg="white", font=("Helvetica", 11, "bold"),
                  relief="flat", padx=8, pady=4).pack(side="left")
        tk.Button(btn_frame, text="Sample", command=self._load_sample,
                  font=("Helvetica", 10), relief="flat",
                  padx=6, pady=4).pack(side="left", padx=6)
        tk.Button(btn_frame, text="Clear", command=self._clear,
                  font=("Helvetica", 10), relief="flat",
                  padx=6, pady=4).pack(side="left")

        # ── right panel ──────────────────────────────────────────────────────
        right = tk.Frame(self, bg="#f5f5f0")
        right.grid(row=0, column=1, sticky="nsew", **pad)

        tk.Label(right, text="Map Visualization",
                 bg="#f5f5f0", font=("Helvetica", 11, "bold")).pack(anchor="w")

        self.canvas = tk.Canvas(right, width=460, height=340,
                                 bg="#eeeee8", highlightthickness=1,
                                 highlightbackground="#ccc")
        self.canvas.pack()

        tk.Label(right, text="Result",
                 bg="#f5f5f0", font=("Helvetica", 11, "bold")).pack(anchor="w",
                                                                      pady=(8,0))
        self.result_lbl = tk.Label(right, text="", bg="#f5f5f0",
                                    font=("Courier", 10), justify="left",
                                    anchor="w")
        self.result_lbl.pack(fill="x")

        tk.Label(right, text="Algorithm Trace",
                 bg="#f5f5f0", font=("Helvetica", 11, "bold")).pack(anchor="w",
                                                                      pady=(8,0))
        trace_frame = tk.Frame(right, bg="#f5f5f0")
        trace_frame.pack(fill="both", expand=True)
        self.trace_txt = tk.Text(trace_frame, height=8,
                                  font=("Courier", 9), state="disabled",
                                  bg="#f0f0eb")
        scroll = tk.Scrollbar(trace_frame, command=self.trace_txt.yview)
        self.trace_txt.configure(yscrollcommand=scroll.set)
        self.trace_txt.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

    # ── actions ───────────────────────────────────────────────────────────────

    def _load_sample(self):
        self.regions_txt.delete("1.0", "end")
        self.regions_txt.insert("end", "A\nB\nC\nD")

        self.adj_txt.delete("1.0", "end")
        self.adj_txt.insert("end", "A-B\nA-C\nB-C\nB-D\nC-D")

        self.colors_txt.delete("1.0", "end")
        self.colors_txt.insert("end", "Red\nGreen\nBlue")

        self.result_lbl.config(text="")
        self._clear_trace()
        self.canvas.delete("all")

    def _clear(self):
        for w in (self.regions_txt, self.adj_txt, self.colors_txt):
            w.delete("1.0", "end")
        self.result_lbl.config(text="")
        self._clear_trace()
        self.canvas.delete("all")

    def _solve(self):
        regions = [r.strip() for r in
                   self.regions_txt.get("1.0","end").splitlines() if r.strip()]
        colors  = [c.strip() for c in
                   self.colors_txt.get("1.0","end").splitlines() if c.strip()]

        adjacency = []
        for line in self.adj_txt.get("1.0","end").splitlines():
            line = line.strip()
            if not line:
                continue
            parts = [p.strip() for p in line.replace(","," ").split("-") if p.strip()]
            if len(parts) == 2:
                adjacency.append((parts[0], parts[1]))

        if not regions:
            messagebox.showwarning("Input", "Please enter at least one region.")
            return
        if not colors:
            messagebox.showwarning("Input", "Please enter at least one color.")
            return

        csp = MapColoringCSP(regions, adjacency, colors)
        solution = csp.solve()

        # update trace
        self._clear_trace()
        self.trace_txt.configure(state="normal")
        for step in csp.trace:
            self.trace_txt.insert("end", step + "\n")
        self.trace_txt.configure(state="disabled")

        if solution:
            result_lines = "\n".join(f"  {r}  →  {solution[r]}" for r in regions)
            self.result_lbl.config(text=result_lines, fg="#2a7a2a")
            self._draw_map(regions, adjacency, solution)
        else:
            self.result_lbl.config(
                text="No solution found.\nTry adding more colors.", fg="#c0392b")
            self._draw_map(regions, adjacency, {})

    # ── visualization ─────────────────────────────────────────────────────────

    def _draw_map(self, regions, adjacency, solution):
        self.canvas.delete("all")
        n = len(regions)
        if n == 0:
            return

        cw = int(self.canvas["width"])
        ch = int(self.canvas["height"])
        cx, cy = cw / 2, ch / 2
        radius = min(cw, ch) * 0.34

        # Compute node positions (circular layout)
        positions = {}
        for i, r in enumerate(regions):
            angle = (2 * math.pi * i / n) - math.pi / 2
            positions[r] = (
                cx + radius * math.cos(angle),
                cy + radius * math.sin(angle),
            )

        # Draw edges
        drawn = set()
        for a, b in adjacency:
            if a not in positions or b not in positions:
                continue
            key = tuple(sorted([a, b]))
            if key in drawn:
                continue
            drawn.add(key)
            x1, y1 = positions[a]
            x2, y2 = positions[b]
            self.canvas.create_line(x1, y1, x2, y2,
                                     fill="#aaaaaa", width=1.5, dash=(4, 4))

        # Draw nodes
        r_node = 26
        for region in regions:
            x, y = positions[region]
            color = solution.get(region, "")
            fill  = COLOR_HEX.get(color, "#dddddd")
            self.canvas.create_oval(x - r_node, y - r_node,
                                     x + r_node, y + r_node,
                                     fill=fill, outline="#555", width=2)
            self.canvas.create_text(x, y, text=region,
                                     font=("Helvetica", 13, "bold"),
                                     fill="white" if color else "#333")
            if color:
                self.canvas.create_text(x, y + r_node + 12, text=color,
                                         font=("Helvetica", 8), fill="#555")

    def _clear_trace(self):
        self.trace_txt.configure(state="normal")
        self.trace_txt.delete("1.0", "end")
        self.trace_txt.configure(state="disabled")


# ─── Entry point ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    if "--cli" in sys.argv:
        run_cli()
    else:
        app = MapColoringApp()
        app.mainloop()
