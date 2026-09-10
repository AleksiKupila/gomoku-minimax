from math import inf
from time import perf_counter
from utils.board_utils import *

def get_candidates(board, all_moves, ROW_COUNT, COL_COUNT, player, opponent, move_ordering):
    '''
    Get all free neighboring tiles of a tile
    '''
    # Adjacent tiles within 1 tile
    nearby_tiles = [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, 1), (1, -1)]
    candidates = []

    for (r,c) in all_moves:

        if board[r][c] == 0:
            continue

        for tile in nearby_tiles:
            candidate = (r + tile[0], c + tile[1])

            # Make sure not in list already
            if candidate in candidates:
                continue

            # Make sure within range
            if candidate[0] >= ROW_COUNT or candidate[0] < 0 or candidate[1] >= COL_COUNT or candidate[1] < 0:
                continue 

            # Make sure is empty
            if board[candidate[0]][candidate[1]] != 0:
                continue

            candidates.append(candidate)

    if move_ordering:
        candidates = order_candidates(board, candidates, player, opponent, ROW_COUNT, COL_COUNT)

    return candidates

class Tile():
    '''
    Represents a single tile on board
    '''
    def __init__(self, position=None, owner=None):
        self.position = position
        self.owner = owner
        self.streaks = {}

    def __lt__(self, other):
        return  self.position < other.position
    
class Streak():
    '''
    Represents a continuous, uninterrupted streak (2, 3, 4, 5...) of tiles
    '''
    def __init__(self, parent=None, members = None, open_end = True, open_start = True, style = None, double_threat = False):
        self.parent = parent
        self.members = members
        self.open_end = open_end
        self.open_start = open_start
        self.double_threat = double_threat
        self.style = style

        self.streak = len(members) + 1

def order_candidates(board, candidates, player, opponent, rows, cols):

    OWN_WEIGHT = 1.0
    BLOCK_WEIGHT = 1.2

    nearby_tiles = [
        (0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, 1), (1, -1),
        (0, -2), (0, 2), (-2, 0), (2, 0), (-2, -2), (-2, 2), (2, 2), (2, -2)
    ]
    scored = []
    score = 0

    for (r, c) in candidates:

        for dr, dc in nearby_tiles:
            nr = r + dr
            nc = c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                if board[nr][nc] == player:
                    score +=OWN_WEIGHT
                elif board[nr][nc] == opponent:
                    score +=BLOCK_WEIGHT

        scored.append(((r, c), score))
        score = 0

    scored.sort(key=lambda x:x[1], reverse=True)

    return [move for move, _ in scored]
        


def continuous_tiles(board, pos, ROW_COUNT, COL_COUNT, tile_registry):
    '''
    Checks streaks the current tile is connected to
    '''
    def get_tile(r, c, owner):
        if (r, c) not in tile_registry:
            tile_registry[(r, c)] = Tile((r, c), owner)
        return tile_registry[(r, c)]
    
    # Vertical, Horizontal, Descending, ascending
    DIRECTIONS = {
        "Horizontal": (0,1),
        "Vertical": (1,0),
        "Ascending": (1,-1), # 1,-1
        "Descending": (1,1)
    }

    # Row and column of current tile
    row, col = pos

    # Get player and opponent
    player = board[row][col]

    if player == 1: opponent = 2 
    else: opponent = 1

    start_tile = get_tile(row, col, player)

    streaks = []

    for direction, (dr, dc) in DIRECTIONS.items():

        # If the tile behind this tile belongs to the player, skip
        back_r, back_c = row - dr, col - dc
        if 0 <= back_r < ROW_COUNT and 0 <= back_c < COL_COUNT:
            open_start = board[back_r][back_c] != opponent
            if board[back_r][back_c] == player:
                continue
        else:
            open_start = False

        members = [start_tile]
        # walk forward
        r, c = row + dr, col + dc
        while 0 <= r < ROW_COUNT and 0 <= c < COL_COUNT and board[r][c] == player:
            new_tile = get_tile(r, c, player)
            if direction not in new_tile.streaks:
                members.append(new_tile)
            r += dr
            c += dc

        if len(members) <= 2:
            continue
        # If next tile is out of bounds or owned by opponent, mark as closed
        if 0 <= r < ROW_COUNT and 0 <= c < COL_COUNT:
            open_end =  board[r][c] != opponent
        else:
            open_end = False

        new_streak = Streak(members[0], members, open_end, open_start, direction)
        streaks.append(new_streak)
            
        for member in members:
            tile_registry[(member.position[0], member.position[1])].streaks[direction] = new_streak

    if len(streaks) > 1:
        fully_open = [s for s in streaks if s.open_end and s.open_start]
        if len(fully_open) >= 2:
            for s in fully_open:
                s.double_threat = True
        
    return streaks, tile_registry

def calculate_scores(streaks, player):
    '''
    Calculate scores for a player based on their streaks
    '''

    OWN_WEIGHT = 1
    BLOCK_WEIGHT = 1.2

    SCORE_3 = 100
    SCORE_4 = 1000

    OPEN_ENDS_4 = 5000

    DOUBLE_THREAT_3 = 3000
    DOUBLE_THREAT_4 = 7000

    SCORE_5 = 100_000_000
    score = 0

    len_scoring = {3:SCORE_3, 4:SCORE_4, 5:SCORE_5, 6:10_000_000, 7:10_000_000, 8:10_000_000, 9:10_000_000, 10:10_000_000}
    ends_multipliers = {(True, True): 10, (True, False): 1, (False, True): 1, (False, False): 0}

    if player == 1:
        weight = BLOCK_WEIGHT
    else:
        weight = OWN_WEIGHT

    for streak in streaks:
        length = len(streak.members)
        
        if length >= 5:
            score += SCORE_5 * weight 
            continue

        if streak.double_threat:
            if length == 3:

                score += DOUBLE_THREAT_3 * weight
            else:
                score += DOUBLE_THREAT_4 * weight

        elif streak.open_end and streak.open_start and len(streak.members) == 4:

            score += OPEN_ENDS_4 * weight

        else:
            len_score = len_scoring[len(streak.members)] * weight
            ends_multiplier = ends_multipliers[streak.open_end, streak.open_start]
            score += len_score*ends_multiplier

    return int(score)

def evaluate(board, ROW_COUNT, COL_COUNT, all_moves):
    '''
    Evaluate the situation on board by checking streaks of both players, and scoring them.
    '''
    ai_streaks = []
    player_streaks = []

    tile_registry = {}

    for r, c in all_moves:
        # Empty tile
        if board[r][c] == 0:
            continue
        # Streaks and tiles connected
        streaks, tile_registry = continuous_tiles(board, (r,c), ROW_COUNT, COL_COUNT, tile_registry)

        for streak in streaks:
            if streak.members[0].owner == 1:
                player_streaks.append(streak)
            else:
                ai_streaks.append(streak)

    player_score = calculate_scores(player_streaks, 1)
    ai_score = calculate_scores(ai_streaks, 2)

    return ai_score - player_score

def minimax(board, all_moves, depth, ROW_COUNT, COL_COUNT, move_ordering = False, maximizing = True, move = None):
    '''
    Default, unoptimized minimax algorithm
    '''
    if move:
        just_moved = 1 if maximizing else 2
        if check_win(board, move[0], move[1], just_moved, ROW_COUNT, COL_COUNT):
            win_score = 100_000_000 + depth
            return (win_score if just_moved == 2 else -win_score), move
        
        if depth == 0:
            return evaluate(board, ROW_COUNT, COL_COUNT, all_moves), move

    if maximizing:
        for move in candidates:
            board = place_mark(board, move, 2)
            all_moves.append(move)
            score, child_move = minimax(board, all_moves, depth - 1, ROW_COUNT, COL_COUNT, move_ordering, False, move)
            board = remove_mark(board, move)
            all_moves.pop()

            if score > max_score:
                max_score = score
                best_move = move

        return max_score, best_move
            
    else:
        min_score = inf
        best_move = None
        candidates = get_candidates(board, all_moves, ROW_COUNT, COL_COUNT, 1, 2, move_ordering)

        for move in candidates:
            board = place_mark(board, move, 1)
            all_moves.append(move)
            score, child_move = minimax(board, all_moves, depth - 1, ROW_COUNT, COL_COUNT, move_ordering, True, move)
            board = remove_mark(board, move)
            all_moves.pop()

            if score < min_score:
                min_score = score
                best_move = move

        return min_score, best_move

    
def alpha_beta(board, all_moves, depth, ROW_COUNT, COL_COUNT, move_ordering = False, maximizing = True, move = None, alpha = -inf, beta = inf):
    '''
    Minimax algorithm using alpha-beta pruning
    '''
    if move:
        if depth == 0:
            return evaluate(board, ROW_COUNT, COL_COUNT, all_moves), move

    if maximizing:
        max_score = -inf
        best_move = None
        candidates = get_candidates(board, all_moves, ROW_COUNT, COL_COUNT, 2, 1, move_ordering)

        for move in candidates:
            board = place_mark(board, move, 2)
            all_moves.append(move)
            score, child_move = alpha_beta(board, all_moves, depth - 1, ROW_COUNT, COL_COUNT, move_ordering, False, move, alpha, beta)
            board = remove_mark(board, move)
            all_moves.pop()

            if score > max_score:
                max_score = score
                best_move = move

            alpha = max(alpha, score)

            if alpha >= beta:
                break
        return max_score, best_move
            
    else:
        min_score = inf
        best_move = None
        candidates = get_candidates(board, all_moves, ROW_COUNT, COL_COUNT, 1, 2, move_ordering)

        for move in candidates:
            board = place_mark(board, move, 1)
            all_moves.append(move)
            score, child_move = alpha_beta(board, all_moves, depth - 1, ROW_COUNT, COL_COUNT, move_ordering, True, move, alpha, beta)
            board = remove_mark(board, move)
            all_moves.pop()

            if score < min_score:
                min_score = score
                best_move = move

            beta = min(beta, score)

            if alpha >= beta:
                break

        return min_score, best_move


        