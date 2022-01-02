# sudoku-solver

A (naive) Sudoku game solver written in Python and Numpy.

## Test the solver

```python3 sudoku.py sample/grid_in.csv```

or:

```./sudoku.py sample/grid_in.csv```

## Run the solver on your CSV file

```./sudoku.py your_file.csv```

CSV file format:
 - delimiter : `,`
 - missing values can be empty or `0`
 - lines in the file shall not contain trailing delimiters
