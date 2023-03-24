import numpy as np


WIDTH = 9
HEIGHT = 9
SUBGRID_WIDTH = 3
SUBGRID_HEIGHT = 3


grid = np.array([
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9],
])


def get_dependents(row, col):
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


def possible_states(grid, row, col):
    state = full_state()

    dependents = get_dependents(row, col)

    for d in dependents:
        cell = grid[d[0], d[1]]
        if len(cell) == 1:
            try:
                state.remove(next(iter(cell)))
            except KeyError:
                pass

    return state


def collapse(grid, needs_collapse, row, col):
    dependents = get_dependents(row, col)

    for d in dependents:
        if needs_collapse[d[0], d[1]] == 1:
            collapse(grid, needs_collapse, d[0], d[1])

    state = full_state()

    for d in dependents:
        cell = grid[d[0], d[1]]
        if len(cell) == 1:
            state.remove(cell[0])

    old_state = grid[row, col]

    if state == old_state:
        for d in dependents:
            needs_collapse[d[0], d[1]] = 1

    needs_collapse[row, col] = 0

    grid[row, col] = state


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
    # needs_collapse = np.ones(grid.shape)

    # wf_grid = np.empty(grid.shape, dtype=set)
    #
    # for r in range(grid.shape[0]):
    #     for c in range(grid.shape[1]):
    #         if grid[r, c] != 0:
    #             wf_grid[r, c] = {grid[r, c]}
    #         else:
    #             wf_grid[r, c] = full_state()

    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if len(wf_grid[r, c]) != 1:
                wf_grid[r, c] = possible_states(wf_grid, r, c)

    # for r in range(needs_collapse.shape[0]):
    #     for c in range(needs_collapse.shape[1]):
    #         if needs_collapse[r, c]:
    #             collapse(grid, needs_collapse, r, c)

    return wf_grid


vectorised_len = np.vectorize(len)


def solved(wf_grid):
    return np.all(vectorised_len(wf_grid) == 1)


# print(grid)
# dependents = get_dependents(3, 3)
# for d in dependents:
#     grid[d[0], d[1]] = 9
#
# print(grid)

print(grid)
wf_grid = make_wf_grid(grid)
print(wf_grid)
while not solved(wf_grid):
    wf_grid = solve_pass(wf_grid)
    print(wf_grid)