
def create_board(rows, cols):
    '''
    Create game board with specified rows and columns
    '''
    board = []
    for r in range(rows):
        board.append([])
        for c in range(cols):
            board[r].append(0)
    return board

def valid_location(board, row, col, player):
    '''
    Check if a location on board is available
    '''
    try:
        if board[row][col] == 0:
            return True
        else:
            print("Mark already in position!\n")
            
    except Exception as e:
        print(f"Illegal move: {e}\n") 

    return False

def place_mark(board, pos, player):
    '''
    Place player mark on the board
    '''
    row, col = pos
    if valid_location:
        board[row][col] = player
    return board

def remove_mark(board, pos):
    '''
    Remove player mark from the board
    '''
    row, col = pos
    board[row][col] = 0
    return board

def check_win(board, row, col, player, rows = 10, cols = 10, win_length = 5):
    '''
    Check if a player has won the game
    '''
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

    for dr, dc in directions:
        count = 1 

        # walk forward
        r, c = row + dr, col + dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == player:
            count += 1
            r += dr
            c += dc

        # walk backward
        r, c = row - dr, col - dc
        while 0 <= r < rows and 0 <= c < cols and board[r][c] == player:
            count += 1
            r -= dr
            c -= dc

        if count >= win_length:
            return True

    return False

OUTER_SQUARE = 100
RADIUS =  30

BOARD_COLOR = (0,0,0)
SQUARE_COLOR = (255,255,255)
TITLE_COLOR = (0,0,0)
P1_COLOR = (0,0,255)
P2_COLOR = (255,0,0)

def draw_board(pg, board, screen, ROW_COUNT, COL_COUNT):
    for r in range(ROW_COUNT):
        for c in range(COL_COUNT):
            # Board background
            pg.draw.rect(screen, BOARD_COLOR, (c*OUTER_SQUARE, r*OUTER_SQUARE+ OUTER_SQUARE, OUTER_SQUARE, OUTER_SQUARE))
            # Board squares
            pg.draw.rect(screen, SQUARE_COLOR, (c*OUTER_SQUARE + 5, r*OUTER_SQUARE + OUTER_SQUARE + 5, OUTER_SQUARE- 10, OUTER_SQUARE - 10))
            # Player 1
            if board[r][c] == 1:
                pg.draw.circle(screen, P1_COLOR, (c*OUTER_SQUARE + 0.5*OUTER_SQUARE, (r*OUTER_SQUARE + 0.5*OUTER_SQUARE) + OUTER_SQUARE) , RADIUS)
            # Player 2
            elif board[r][c] == 2:
                pg.draw.circle(screen, P2_COLOR, (c*OUTER_SQUARE + 0.5*OUTER_SQUARE, (r*OUTER_SQUARE + 0.5*OUTER_SQUARE) + OUTER_SQUARE), RADIUS)       

def draw_scoreboard(pg, board, screen, player, game_over, ROW_COUNT, COL_COUNT):
    pg.draw.rect(screen, BOARD_COLOR, (0,0,COL_COUNT*OUTER_SQUARE, OUTER_SQUARE))
    pg.draw.rect(screen, SQUARE_COLOR, ((COL_COUNT * OUTER_SQUARE)- 200, 25, 175, 50))

    reset_font = pg.font.SysFont("Arial", 30, True)
    status_font = pg.font.SysFont("Arial", 30, True)
    reset_text = reset_font.render("RESET", True, BOARD_COLOR)
    screen.blit(reset_text, (((COL_COUNT * OUTER_SQUARE)- 160), 32))

    if player == 1:
        if game_over:
            status_font = pg.font.SysFont("Arial", 70, True)
            player_text = status_font.render("BLUE WON!", True, P1_COLOR)
        else:
            player_text = status_font.render("BLUE TURN", True, P1_COLOR)
        screen.blit(player_text, (0,0))
    else:
        if game_over:
            status_font = pg.font.SysFont("Arial", 70, True)
            player_text = status_font.render("RED WON!", True, P2_COLOR)
        else:
            player_text = status_font.render("RED TURN", True, P2_COLOR)
        screen.blit(player_text, (0,0))