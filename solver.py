def find_empty(bo):
    for row in range(len(bo)):
        for column in range(len(bo[0])):
            if bo[row][column] == 0:
                return row, column
    return None


def print_board(bo):
    # Separate Rows into squares
    for row in range(len(bo)):
        if row % 3 == 0 and row != 0:
            print("- - - - - - - - - - - - - ")
    # Separate Columns into squares
        for column in range(len(bo[0])):
            if column % 3 == 0 and column != 0:
                print(' | ', end='')

            if column == 8:
                print(bo[row][column])
            else:
                print(str(bo[row][column]) + ' ', end='')


def valid(bo, num, pos):
    # Check rows
    for i in range(len(bo[0])):
        if bo[pos[0]][i] == num and pos[1] != i:
            return False
    # Check columns
    for i in range(len(bo)):
        if bo[i][pos[1]] == num and pos[0] != i:
            return False
    # Check squares
    box_x = pos[1] // 3
    box_y = pos[0] // 3
    for i in range(box_y*3, box_y*3 + 3):
        for j in range(box_x*3, box_x*3 + 3):
            if bo[i][j] == num and (i, j) != pos:
                return False
    return True


def solve(bo):
    # Check if solution is finished
    find = find_empty(bo)
    if not find:
        return True
    else:
        row, col = find
    # Run back-tracking algorithm
    for i in range(1, 10):
        if valid(bo, i, (row, col)):
            bo[row][col] = i
            if solve(bo):
                return True
            bo[row][col] = 0
    return False

