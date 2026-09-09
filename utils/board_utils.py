
def create_board(rows, cols):
    board = []
    for r in range(rows):
        board.append([])
        for c in range(cols):
            board[r].append(0)
    return board

def valid_location(board, row, col, player):
    try:
        if board[row][col] == 0:
            return True
        else:
            print("Mark already in position!\n")
            
    except Exception as e:
        print(f"Illegal move: {e}\n") 

    return False

def place_mark(board, pos, player):
    row, col = pos
    if valid_location:
        board[row][col] = player
    return board

def remove_mark(board, pos):
    row, col = pos
    board[row][col] = 0
    return board