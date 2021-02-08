# CSP Solver: Colored Sudoku

This project is a Python implementation of a Constraint Satisfaction Problem (CSP) solver designed to solve a variant of Sudoku called "Colored Sudoku." The solver utilizes backtracking search with forward checking and employs heuristics like Minimum Remaining Values (MRV) and Degree Heuristic to efficiently find solutions.

## Game Rules

In this advanced version of Sudoku, we introduce coloring to the grid. The rules for this version of the game are as follows:

1. **Numbers and Colors**: Each cell in the grid must contain both a number and a color.

2. **Standard Sudoku Constraints**: Similar to the regular Sudoku game, in each row and column of an \( n \times n \) grid, all numbers from 1 to \( n \) must be used, and each number must be unique within its row and column. The number constraints only apply to rows and columns and require uniqueness in those dimensions.

3. **Adjacent Cell Colors**: Adjacent cells (up, down, left, right) must not share the same color. For example, if a cell is yellow, none of its adjacent cells can be yellow.

4. **Color Priority and Number Relation**: Colors have a defined priority order. If a cell has a color with a higher priority compared to its adjacent cells, then the number in that cell must also be greater than the numbers in those adjacent cells.

## Usage

The main script `main.py` is designed to solve Colored Sudoku puzzles. To use the solver, simply run the script and input the puzzle when prompted.

### Steps to Run the Solver

1. **Prepare Your Puzzle Input**

   - The input should specify the grid size, the number of colors, the color mappings (which also define the color priority), and the initial cell assignments.
   - The format is as follows:

     ```
     m n
     color1 color2 ... color_m
     cell11 cell12 ... cell1n
     cell21 cell22 ... cell2n
     ...
     celln1 celln2 ... cellnn
     ```

     - **n**: Grid size (number of rows and columns).
     - **m**: Number of colors.
     - **color1 color2 ... color_m**: List of color codes or names, in order of priority from highest to lowest.
     - **cellij**: Each cell's content, combining a number (or `*` for empty) and a color code (or `#` for no color). For example:
       - `5r` means the cell has the number `5` and color `r`.
       - `*g` means the cell is empty and has color `g`.
       - `*#` means the cell is empty with no color.

2. **Run the Script**

   Execute `main.py` using Python 3:

   ```
   python main.py
   ```

3. **Input the Puzzle**

    When prompted, input the puzzle data line by line.

## Examples

### Example 1: Solving a Colored Sudoku Puzzle

**Input:**

```
4 4
r g b y
*y 2g *r 3b
3g 1# *# *#
*y 4r *b *#
*g *# 1y 2b
```

**Expected Output:**

```
Result:
1y 2g 4r 3b
3g 1y 2b 4r
2b 4r 3g 1y
4r 3b 1y 2g
```

---

### Example 2: Unsolvable Colored Sudoku Puzzle

**Input:**

```
5 4
r g b y p
*y 2g *r 3b
3g 1b *# *#
*y 4r *b *#
*g *# 1y 2b
```

**Expected Output:**

```
Result:
Unsolvable problem.
```
