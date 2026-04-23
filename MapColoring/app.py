import streamlit as st

# -------------------------------
# CSP Logic
# -------------------------------

def is_valid(region, color, assignment, neighbors):
    for neighbor in neighbors.get(region, []):
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
# UI
# -------------------------------

st.title("Map Coloring Problem (CSP)")

st.subheader("Step 1: Enter Regions")
regions_input = st.text_input("Enter regions (comma separated)", "A,B,C,D")
regions = [r.strip() for r in regions_input.split(",") if r.strip()]

st.subheader("Step 2: Enter Neighbors")

neighbors = {}
for region in regions:
    neighbors_input = st.text_input(f"Neighbors of {region}", "")
    neighbors[region] = [n.strip() for n in neighbors_input.split(",") if n.strip()]

st.subheader("Step 3: Select Colors")
color_count = st.selectbox("Number of colors", [3, 4])

if color_count == 3:
    colors = ["Red", "Green", "Blue"]
else:
    colors = ["Red", "Green", "Blue", "Yellow"]

# -------------------------------
# Solve Button
# -------------------------------

if st.button("Solve"):
    if not regions:
        st.error("Please enter regions")
    else:
        solution = backtrack({}, regions, colors, neighbors)

        if solution:
            st.success("Solution Found!")

            # Output
            st.subheader("Final Color Assignment")
            for r in sorted(solution):
                st.write(f"{r} → {solution[r]}")

            st.info("All constraints satisfied: No adjacent regions share the same color")

            # -------------------------------
            # Visualization
            # -------------------------------
            st.subheader("Map Visualization")

            color_map = {
                "Red": "#FF4B4B",
                "Green": "#2ECC71",
                "Blue": "#3498DB",
                "Yellow": "#F1C40F"
            }

            cols = st.columns(4)

            for i, region in enumerate(solution):
                color = color_map[solution[region]]

                box = f"""
                <div style="
                    width:80px;
                    height:80px;
                    background-color:{color};
                    display:flex;
                    align-items:center;
                    justify-content:center;
                    color:white;
                    font-size:20px;
                    font-weight:bold;
                    border-radius:8px;
                    margin:5px;">
                    {region}
                </div>
                """

                cols[i % 4].markdown(box, unsafe_allow_html=True)

        else:
            st.error("No valid coloring possible with given constraints")
