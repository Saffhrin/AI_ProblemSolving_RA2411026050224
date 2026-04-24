# Map Coloring (CSP)

> Assign colors to map regions so no two adjacent regions share the same color, using a **Constraint Satisfaction Problem (CSP)** backtracking solver with MRV heuristic and Forward Checking.

---

## Repository Structure

```
AI_ProblemSolving_RA2411026050224/
├── README.md
└── map_coloring/
    ├── map_coloring_csp.py     ← Python solver + Tkinter GUI
    └── index.html              ← Interactive web UI
```

---

## Problem Description

Given a map with regions and their neighboring relationships, assign a color to each region such that **no two adjacent regions share the same color**, using the minimum number of colors (typically 3 or 4).

### Sample Input / Output

**Input:**
- Regions: A, B, C, D
- Adjacency: A–B, A–C, B–C, B–D, C–D
- Colors available: Red, Green, Blue

**Output:**
```
A → Red
B → Green
C → Blue
D → Red
```

---

## Algorithm

### CSP Backtracking with MRV + Forward Checking

| Component | Detail |
|-----------|--------|
| **Variables** | Each region on the map |
| **Domain** | Set of available colors |
| **Constraints** | Adjacent regions must have different colors |
| **Search** | Backtracking (depth-first) |
| **Heuristic** | MRV — assign the most constrained region first |
| **Pruning** | Forward Checking — prune neighbor domains after each assignment |

**How it works:**
1. Pick the unassigned region with the fewest remaining legal colors (MRV)
2. Try each color — skip if a neighbor already uses it
3. After assigning, check that every unassigned neighbor still has at least one legal color
4. If a conflict is found, backtrack and try the next color
5. Repeat until all regions are assigned or no solution exists

---

## Files

### `map_coloring_csp.py` — Python solver
- Full CSP engine with backtracking + MRV + Forward Checking
- Tkinter GUI with canvas map visualization and algorithm trace
- CLI mode for running directly in the terminal

### `index.html` — Web UI
- Runs entirely in the browser, no installation needed
- Add/remove regions and adjacency interactively
- Toggle available colors (2–6 colors)
- Map view (Voronoi) and Graph view (node-link diagram)
- Live CSP trace showing every assign and backtrack step

---

## Execution Steps

### Web UI
Open `map_coloring/index.html` in any browser — or visit the live GitHub Pages link below.

### Python GUI
```bash
python map_coloring/map_coloring_csp.py
```
Requires Python 3.10+ with Tkinter (`sudo apt install python3-tk` on Ubuntu).

### Python CLI
```bash
python map_coloring/map_coloring_csp.py --cli
```

---

## Sample Output (CLI)

```
==================================================
  Map Coloring CSP — Sample Run
==================================================

Regions   : A, B, C, D
Adjacency : A-B, A-C, B-C, B-D, C-D
Colors    : Red, Green, Blue

Solution found:

  A  →  Red
  B  →  Green
  C  →  Blue
  D  →  Red

Algorithm trace:
  assign  A  →  Red
  assign  B  →  Green
  assign  C  →  Blue
  assign  D  →  Red
```

---

## Live Website
[View interactive demo on GitHub Pages](https://yourusername.github.io/AI_ProblemSolving_YourName/)

## Contributed by
X.P.Saffhrin , RA2411026050224
