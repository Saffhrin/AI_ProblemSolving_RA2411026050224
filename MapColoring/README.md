# Map Coloring Problem (CSP)

## Problem Description
The Map Coloring Problem involves assigning colors to different regions on a map such that no two adjacent regions share the same color.

## Algorithm Used
Constraint Satisfaction Problem (CSP) using Backtracking Algorithm.

## Constraints
- Adjacent regions must not have the same color  
- Limited colors are used (Red, Green, Blue)

## Execution Steps
1. Run the program:  
   python main.py  
2. Click the "Solve" button  
3. View the color assignment and visualization  

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
