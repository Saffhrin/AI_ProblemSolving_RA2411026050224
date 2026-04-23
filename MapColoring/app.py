import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

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

st.set_page_config(page_title="Map Coloring CSP", page_icon="🎨")

st.title("🎨 Map Coloring Problem (CSP)")
st.markdown("Assign colors so that no adjacent regions share the same color.")

st.subheader("Enter Regions")
regions_input = st.text_input("Regions (comma separated)", "A,B,C,D")
regions = [r.strip() for r in regions_input.split(",") if r.strip()]

st.subheader("Enter Neighbor Relationships")

neighbors = {}
for region in regions:
    neighbors_input = st.text_input(f"Neighbors of {region}", "")
    neighbors[region] = [n.strip() for n in neighbors_input.split(",") if n.strip()]

st.subheader("Select Colors")
color_count = st.selectbox("Number of colors", [3, 4])

if color_count == 3:
    colors = ["red", "green", "blue"]
else:
    colors = ["red", "green", "blue", "yellow"]

# -------------------------------
# Solve
# -------------------------------

if st.button("Solve"):

    solution = backtrack({}, regions, colors, neighbors)

    if solution:
        st.success("Solution Found!")

        st.subheader("Color Assignment")
        for r in solution:
            st.write(f"{r} → {solution[r]}")

        # -------------------------------
        # Graph Visualization
        # -------------------------------

        st.subheader("Graph Visualization")

        G = nx.Graph()

        # Add nodes
        for r in regions:
            G.add_node(r)

        # Add edges
        for r in neighbors:
            for n in neighbors[r]:
                G.add_edge(r, n)

        # Assign colors
        node_colors = [solution[node] for node in G.nodes()]

        # Draw graph
        pos = nx.spring_layout(G)

        fig, ax = plt.subplots()
        nx.draw(
            G,
            pos,
            with_labels=True,
            node_color=node_colors,
            node_size=2000,
            font_size=12,
            font_color="white",
            ax=ax
        )

        st.pyplot(fig)

    else:
        st.error("No valid coloring found")
