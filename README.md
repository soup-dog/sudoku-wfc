# sudoku-wfc

Sudoku solver written in ~45 minutes from first principles. Takes vague inspiration from wave function collapse and solves the puzzle in a series of solving "passes" in which grid cell state collapse is unbuffered (i.e. collapse results are written to the grid immediately).
Has a command-line interface where the first argument is the sudoku puzzle. Puzzle is specified as a string in row-major order where each char corresponds to a cell on the grid. Blank cells are 0. 

Sample usage (solving [this puzzle](https://en.wikipedia.org/wiki/File:Sudoku_Puzzle_by_L2G-20050714_standardized_layout.svg)):
```commandline
python sudoku.py 530070000600195000098000060800060003400803001700020006060000280000419005000080079
```

# Requirements
Requires numpy.
```commandline
pip install -r requirements.txt
```
