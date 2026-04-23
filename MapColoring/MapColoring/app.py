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

        st.subheader("Final Color Assignment")
        for r in sorted(solution):
            st.write(f"{r} → {solution[r]}")

        st.info("All constraints satisfied: No adjacent regions share the same color")

        # -------------------------------
        # VISUALIZATION (COLORED BOXES)
        # -------------------------------
        st.subheader("Map Visualization")

        color_map = {
            "Red": "#FF4B4B",
            "Green": "#2ECC71",
            "Blue": "#3498DB"
        }

        # Layout in 2x2 grid
        col1, col2 = st.columns(2)

        positions = ["A", "B", "C", "D"]

        for i, region in enumerate(positions):
            color = color_map[solution[region]]

            box = f"""
            <div style="
                width:100px;
                height:100px;
                background-color:{color};
                display:flex;
                align-items:center;
                justify-content:center;
                color:white;
                font-size:24px;
                font-weight:bold;
                border-radius:10px;
                margin:10px;">
                {region}
            </div>
            """

            if i % 2 == 0:
                col1.markdown(box, unsafe_allow_html=True)
            else:
                col2.markdown(box, unsafe_allow_html=True)

    else:
        st.error("No solution found")
