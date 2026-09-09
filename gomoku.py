import pygame as pg
import math
from time import perf_counter

from minimax import *
from utils.board_utils import *

OUTER_SQUARE = 100
RADIUS =  30

BOARD_COLOR = (0,0,0)
SQUARE_COLOR = (255,255,255)
TITLE_COLOR = (0,0,0)
P1_COLOR = (0,0,255)
P2_COLOR = (255,0,0)

DEPTH = 3

def draw_board(board, screen, ROW_COUNT, COL_COUNT):
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

def draw_scoreboard(board, screen, player, game_over, ROW_COUNT, COL_COUNT):
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

def play(alphabeta = False, depth = 3, performance_metrics = False, ROW_COUNT = 10, COL_COUNT = 10):

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
    all_moves = []
    total_marks = 0

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
                    print(f"Player turn!")
                    col = int(math.floor(pos_x/OUTER_SQUARE))
                    row = int(math.floor((pos_y/OUTER_SQUARE)-1))

                    if valid_location(board, row, col, 1):
                        place_mark(board, (row, col), 1)
                        all_moves.append((row, col))
                        total_marks +=1
                        print(f"Placed mark on {row, col}\n")

                    if check_win(board, row, col, 1, ROW_COUNT, COL_COUNT):
                        print(f"Player wins!")
                        game_over = True
                        player = 1
                        continue


                    print("AI turn!")
                    if performance_metrics: start = perf_counter()

                    if alphabeta: best, best_move = alpha_beta(board, all_moves, depth, ROW_COUNT, COL_COUNT)
                    else: best, best_move = minimax(board, all_moves, depth, ROW_COUNT, COL_COUNT)

                    if performance_metrics: 
                        total = perf_counter() - start
                        print(f"Total algorithm time: {total}")

                    place_mark(board, best_move, 2)
                    all_moves.append(best_move)
                    total_marks +=1
                    print(f"AI placed mark on {best_move}\n")

                    if check_win(board, best_move[0], best_move[1], 2, ROW_COUNT, COL_COUNT):
                        print(f"AI wins!")
                        print(f"Total marks played: {total_marks}")
                        game_over = True
                        player = 2
                        continue
                    else:
                        player = 1

                # Click inside reset button
                if (COL_COUNT * OUTER_SQUARE)- 200 < pos_x < (COL_COUNT * OUTER_SQUARE) - 25 and 25 < pos_y < 75:
                    board = create_board(ROW_COUNT, COL_COUNT)
                    game_over = False

            # fill the screen with a color to wipe away anything from last frame
            #screen.fill("purple")


        draw_board(board, screen, ROW_COUNT, COL_COUNT)
        draw_scoreboard(board, screen, player, game_over, ROW_COUNT, COL_COUNT)
        # flip() the display to put your work on screen
        pg.display.flip()

        clock.tick(60)  # limits FPS to 60

    pg.quit()
