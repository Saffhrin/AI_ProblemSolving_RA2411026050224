import streamlit as st

# CSP Logic
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

# UI
st.title("Map Coloring Problem (CSP)")

regions = ["A", "B", "C", "D"]
colors = ["Red", "Green", "Blue"]
neighbors = {
    "A": ["B", "C"],
    "B": ["A", "C", "D"],
    "C": ["A", "B", "D"],
    "D": ["B", "C"]
}

if st.button("Solve"):
    solution = backtrack({}, regions, colors, neighbors)

    if solution:
        st.success("Solution Found!")
        for r in solution:
            st.write(f"{r} → {solution[r]}")
    else:
        st.error("No solution found")
