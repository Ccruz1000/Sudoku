WIDTH = 600
HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Boards
test_board = [[0 for x in range(9)] for x in range(9)]

# Positions and sizes
top_buff = 100  # Buffer for the top to give room for buttons
out_buff = 75  # Buffer for sides and bottom
grid_pos = (out_buff, top_buff)
cell_size = (WIDTH - 2 * out_buff)/9


