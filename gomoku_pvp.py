import pygame as pg
import math

ROW_COUNT = 10
COL_COUNT = 10

OUTER_SQUARE = 100
RADIUS =  30

BOARD_COLOR = (0,0,0)
SQUARE_COLOR = (255,255,255)
TITLE_COLOR = (0,0,0)
P1_COLOR = (0,0,255)
P2_COLOR = (255,0,0)

def valid_location(board, row, col, player):
    try:
        if board[row][col] == 0:
            return True
        else:
            print("Mark already in position!\n")
            
    except Exception as e:
        print(f"Illegal move: {e}\n") 

    return False
    
def check_win(board, row, col, player, size=10, win_length = 5):

    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

    for dr, dc in directions:
        count = 1 

        # walk forward
        r, c = row + dr, col + dc
        while 0 <= r < size and 0 <= c < size and board[r][c] == player:
            count += 1
            r += dr
            c += dc

        # walk backward
        r, c = row - dr, col - dc
        while 0 <= r < size and 0 <= c < size and board[r][c] == player:
            count += 1
            r -= dr
            c -= dc

        if count >= win_length:
            return True

    return False

def create_board(rows, cols):
    board = []
    for r in range(rows):
        board.append([])
        for c in range(cols):
            board[r].append(0)
    return board

def draw_board(board, screen):
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

def draw_scoreboard(board, screen, player, game_over):
    pg.draw.rect(screen, BOARD_COLOR, (0,0,COL_COUNT*OUTER_SQUARE, OUTER_SQUARE))
    pg.draw.rect(screen, SQUARE_COLOR, ((COL_COUNT * OUTER_SQUARE)- 200, 25, 175, 50))

    title_font = pg.font.SysFont("Arial", 30, True)
    reset_text = title_font.render("RESET", True, BOARD_COLOR)
    screen.blit(reset_text, (((COL_COUNT * OUTER_SQUARE)- 160), 32))

    if player == 1:
        if game_over:
            player_text = title_font.render("BLUE WON!", True, P1_COLOR)
        else:
            player_text = title_font.render("BLUE", True, P1_COLOR)
        screen.blit(player_text, (0,0))
    else:
        if game_over:
            player_text = title_font.render("RED WON!", True, P2_COLOR)
        else:
            player_text = title_font.render("RED", True, P2_COLOR)
        screen.blit(player_text, (0,0))

def play():

    pg.init()
    # Screen size
    width = COL_COUNT * OUTER_SQUARE
    height = (ROW_COUNT + 1) * OUTER_SQUARE
    size = (width, height)
    screen = pg.display.set_mode(size)

    clock = pg.time.Clock()
    running = True

    board = create_board(ROW_COUNT, COL_COUNT)

    game_over = False
    player = 1

    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

            
            if event.type == pg.MOUSEBUTTONDOWN:
                # Click x/y
                pos_x = event.pos[0]
                pos_y = event.pos[1]
                # Click inside board
                if pos_y > OUTER_SQUARE and not game_over: 
                    col = int(math.floor(pos_x/OUTER_SQUARE))
                    row = int(math.floor((pos_y/OUTER_SQUARE)-1))

                    if valid_location(board, row, col, player):
                        board[row][col] = player

                    if check_win(board, row, col, player):
                        print(f"Player {player} wins!")
                        game_over = True

                    elif player == 1:
                        player = 2
                    else: player = 1
                        
                    print(f"Board: {board}")

                # Click inside reset button
                elif (COL_COUNT * OUTER_SQUARE)- 200 < pos_x < (COL_COUNT * OUTER_SQUARE) - 25 and 25 < pos_y < 75:
                    board = create_board(ROW_COUNT, COL_COUNT)
                    game_over = False
                    player = 1
            # fill the screen with a color to wipe away anything from last frame
            #screen.fill("purple")
            
        # RENDER YOUR GAME HERE
        draw_board(board, screen)
        draw_scoreboard(board, screen, player, game_over)
        # flip() the display to put your work on screen
        pg.display.flip()

        clock.tick(60)  # limits FPS to 60

    pg.quit()
        

play()