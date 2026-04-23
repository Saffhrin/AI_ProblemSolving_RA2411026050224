# Map Coloring Problem (CSP)

## Problem Description
The Map Coloring Problem involves assigning colors to different regions on a map such that no two adjacent regions share the same color. This is a classic problem in Artificial Intelligence and is modeled as a Constraint Satisfaction Problem (CSP).

## Algorithm Used
Constraint Satisfaction Problem (CSP) using Backtracking Algorithm.

- Variables: Regions (A, B, C, D, etc.)
- Domain: Colors (Red, Green, Blue, Yellow)
- Constraint: Adjacent regions must not have the same color

## Constraints
- No two adjacent regions can have the same color  
- Limited number of colors (3 or 4)

## Input
- Regions (user-defined)
- Neighbor relationships between regions
- Number of colors (3 or 4)

## Execution Steps

### Run Locally (Tkinter GUI)
1. Navigate to MapColoring folder  
2. Run:
   python main.py  
3. Click "Solve"  
4. View results and visualization  

### Run Online (Web App)
Open the Streamlit application:  
https://aiproblemsolvingra2411026050224-olxw7xkbbyfc7uiu5gduef.streamlit.app/

## Sample Input
Regions: A, B, C, D  

Neighbors:  
A → B, C  
B → A, C, D  
C → A, B, D  
D → B, C  

## Sample Output
A → Red  
B → Green  
C → Blue  
D → Red  

## Output Visualization
- Tkinter: Colored circles  
- Streamlit: Colored blocks  

## Conclusion
This project demonstrates how CSP techniques can be used to solve constraint-based problems efficiently while satisfying all given conditions.

## Contributed by
X.P.Saffhrin,RA2411026050224
