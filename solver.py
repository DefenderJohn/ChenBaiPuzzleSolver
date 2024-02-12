def solve_puzzle(grid, shapes, shape_counts):
    solution = [row[:] for row in grid]
    best_solution = None
    least_universal_shape_count = float('inf')

    def can_place_shape(grid, shape, x, y):
        if x is None or y is None:
            return False
        rows, cols = len(grid), len(grid[0])
        for i in range(len(shape)):
            for j in range(len(shape[0])):
                if shape[i][j] == 0:
                    continue
                new_x, new_y = x + i, y + j
                if new_x >= rows or new_y >= cols or grid[new_x][new_y] != 0:
                    return False 
        return True

    def place_shape(grid, shape, x, y, shape_num):
        for i in range(len(shape)):
            for j in range(len(shape[0])):
                if shape[i][j] != 0:
                    grid[x + i][y + j] = shape_num

    def remove_shape(grid, shape, x, y):
        for i in range(len(shape)):
            for j in range(len(shape[0])):
                if shape[i][j] != 0:
                    grid[x + i][y + j] = 0

    def is_grid_full(grid):
        return all(all(cell != 0 for cell in row) for row in grid)

    def rotate_shape(shape, angle):
        if angle == 90:
            return [list(reversed(col)) for col in zip(*shape)]
        elif angle == 180:
            return [row[::-1] for row in shape[::-1]]
        elif angle == 270:
            return [list(col) for col in zip(*shape[::-1])]
        return shape

    def find_next_empty_position(grid, start_x, start_y):
        for x in range(start_x, len(grid)):
            for y in range(start_y if x == start_x else 0, len(grid[0])):
                if grid[x][y] == 0:
                    return x, y
        return None, None

    def backtrack(x, y, universal_shape_count, used_shape_counts):
        nonlocal solution, best_solution, least_universal_shape_count
        if universal_shape_count < least_universal_shape_count and is_grid_full(solution):
            best_solution = [row[:] for row in solution]
            least_universal_shape_count = universal_shape_count
            return
        
        if universal_shape_count >= least_universal_shape_count:
            return

        for shape_index in range(1, 10):
            shape_num = shape_index - 1
            for angle in [0, 90, 180, 270]:
                rotated_shape = rotate_shape(shapes[shape_index], angle)
                if used_shape_counts[shape_index] < shape_counts[shape_num] and can_place_shape(solution, rotated_shape, x, y):
                    place_shape(solution, rotated_shape, x, y, shape_index)
                    used_shape_counts[shape_index] += 1
                    newX, newY = find_next_empty_position(solution, x, y)
                    if shape_index == 9:
                        backtrack(newX, newY, universal_shape_count + 1, used_shape_counts)
                    else:
                        backtrack(newX, newY, universal_shape_count, used_shape_counts)
                    remove_shape(solution, rotated_shape, x, y)
                    used_shape_counts[shape_index] -= 1
        return

    used_shape_counts = {i: 0 for i in range(1, 10)}
    backtrack(0, 0, 0, used_shape_counts)
    if best_solution is not None:
        return best_solution, least_universal_shape_count
    else:
        return "No solution found", 0


# 这里是解决方案的调用方式
grid = [
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0]
]
shape_counts = [2,3,1,3,1,1,0,1,0]
shapes = {    1: [[1, 1],
                  [1, 1]], 
              2: [[1],
                  [1],
                  [1],
                  [1]],
              3: [[1, 1, 0],
                  [0, 1, 1]],
              4: [[0, 1, 1],
                  [1, 1, 0]],
              5: [[0, 1],
                  [0, 1],
                  [1, 1]],
              6: [[1, 0],
                  [1, 0],
                  [1, 1]],
              7: [[1, 1, 1],
                  [0, 1, 0]],
              8: [[0, 1, 0],
                  [1, 1, 1],
                  [0, 1, 0]],
              9: [[1]]}
solution, least_universal_shape_used = solve_puzzle(grid, shapes, shape_counts)
if "No solution" in solution:
    print("方块不够")
else:
    for row in solution:
        print(row)
print(least_universal_shape_used)