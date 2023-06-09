import numpy as np
from argparse import ArgumentParser


WIDTH = 9
HEIGHT = 9
SUBGRID_WIDTH = 3
SUBGRID_HEIGHT = 3


SGR_RESET = u"\u001b[0m"


def sgr(n: int):
    return u"\u001b[" + str(n) + "m"


def print_wf_grid(wf_grid, uncertain=u"\u001b[31m", certain=u"\u001b[32m"):
    print(SGR_RESET, end="")
    for r in range(wf_grid.shape[0]):
        for c in range(wf_grid.shape[1]):
            state = wf_grid[r, c]
            state_count = len(state)
            if state_count == 1:
                print(certain + str(next(iter(state))), end=" ")
            else:
                print(uncertain + str(state_count), end=" ")
        print()
    print(SGR_RESET, end="")


def get_dependents(row: int, col: int):
    dependents = []
    for r in range(HEIGHT):
        if r != row:
            dependents.append((r, col))
    for c in range(WIDTH):
        if c != col:
            dependents.append((row, c))
    subgrid = row // SUBGRID_HEIGHT * 3, col // SUBGRID_WIDTH * 3
    for r in range(subgrid[0], subgrid[0] + 3):
        for c in range(subgrid[1], subgrid[1] + 3):
            if r != row and c != col:
                dependents.append((r, c))

    return dependents


def full_state():
    return set(i for i in range(1, 10))


def possible_states(grid, row: int, col: int):
    state = full_state()

    dependents = get_dependents(row, col)

    for d in dependents:
        cell = grid[d[0], d[1]]
        if len(cell) == 1:
            v = next(iter(cell))
            if v in state:
                state.remove(v)

    return state


# old rubbish
# def collapse(grid, needs_collapse, row, col):
#     dependents = get_dependents(row, col)
#
#     for d in dependents:
#         if needs_collapse[d[0], d[1]] == 1:
#             collapse(grid, needs_collapse, d[0], d[1])
#
#     state = full_state()
#
#     for d in dependents:
#         cell = grid[d[0], d[1]]
#         if len(cell) == 1:
#             state.remove(cell[0])
#
#     old_state = grid[row, col]
#
#     if state == old_state:
#         for d in dependents:
#             needs_collapse[d[0], d[1]] = 1
#
#     needs_collapse[row, col] = 0
#
#     grid[row, col] = state


def make_wf_grid(grid):
    wf_grid = np.empty(grid.shape, dtype=set)

    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] != 0:
                wf_grid[r, c] = {grid[r, c]}
            else:
                wf_grid[r, c] = full_state()

    return wf_grid


def solve_pass(wf_grid):
    for r in range(wf_grid.shape[0]):
        for c in range(wf_grid.shape[1]):
            if len(wf_grid[r, c]) != 1:
                wf_grid[r, c] = possible_states(wf_grid, r, c)

    return wf_grid


vectorised_len = np.vectorize(len)


def solved(wf_grid):
    return np.all(vectorised_len(wf_grid) == 1)


def parse_flat_sudoku(flat_sudoku: str):
    grid = np.empty([WIDTH, HEIGHT], dtype=np.int32)

    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            grid[r, c] = int(flat_sudoku[r * grid.shape[1] + c])

    return grid


if __name__ == '__main__':
    parser = ArgumentParser(
        prog="wfc-sudoku",
        description="Simple sudoku solver.",
    )

    parser.add_argument("sudoku", type=str, help="the sudoku to solve as a row-major string where a blank space is 0")

    args = parser.parse_args()

    flat_sudoku = args.sudoku

    if len(flat_sudoku) != WIDTH * HEIGHT:
        print(f"Sudoku is of incorrect size ({len(flat_sudoku)} != {WIDTH * HEIGHT}).")
        exit()

    # flat_puzzle = "530070000600195000098000060800060003400803001700020006060000280000419005000080079"

    # grid = np.array([
    #     [5, 3, 0, 0, 7, 0, 0, 0, 0],
    #     [6, 0, 0, 1, 9, 5, 0, 0, 0],
    #     [0, 9, 8, 0, 0, 0, 0, 6, 0],
    #     [8, 0, 0, 0, 6, 0, 0, 0, 3],
    #     [4, 0, 0, 8, 0, 3, 0, 0, 1],
    #     [7, 0, 0, 0, 2, 0, 0, 0, 6],
    #     [0, 6, 0, 0, 0, 0, 2, 8, 0],
    #     [0, 0, 0, 4, 1, 9, 0, 0, 5],
    #     [0, 0, 0, 0, 8, 0, 0, 7, 9],
    # ])

    wf_grid = make_wf_grid(parse_flat_sudoku(flat_sudoku))
    print("INPUT")
    print_wf_grid(wf_grid)
    i = 0
    while not solved(wf_grid):
        print(f"SOLVE PASS: {i}")
        wf_grid = solve_pass(wf_grid)
        print_wf_grid(wf_grid)
        i += 1

    print(f"Solved in {i} passes.")

