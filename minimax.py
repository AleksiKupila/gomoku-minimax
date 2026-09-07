from math import inf

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


def get_candidates(board, ROW_COUNT, COL_COUNT):

    # Adjacent tiles within 1 tile
    nearby_tiles = [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, 1), (1, -1)]
    candidates = []
    for r in range(ROW_COUNT):
        for c in range(COL_COUNT):
            if board[r][c] == 1 or board[r][c] == 2:

                for tile in nearby_tiles:
                    candidate = (r + tile[0], c + tile[1])

                    # Make sure within range
                    if candidate[0] > ROW_COUNT - 1 or candidate[0] < 0 or candidate[1] > COL_COUNT - 1 or candidate[1] < 0:
                        continue 

                    # Make sure is empty
                    if board[candidate[0]][candidate[1]] != 0:
                        continue

                    # Make sure not in list already
                    if candidate in candidates:
                        continue

                    candidates.append(candidate)

    #print(f"candidates: {len(candidates)}")
    #print(candidates)
    return candidates

class Tile():
    def __init__(self, position=None, owner=None):
        self.position = position
        self.owner = owner
        self.streaks = {}

    def __lt__(self, other):
        return  self.position < other.position
    
class Streak():
    def __init__(self, parent=None, members = None, open_end = True, open_start = True, style = None):
        self.parent = parent
        self.members = members
        self.open_end = open_end
        self.open_start = open_start
        self.style = style

        self.streak = len(members) + 1

def continuous_tiles(board, pos, ROW_COUNT, COL_COUNT, tile_registry):
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
    opponent = None
    player = board[row][col]
    if player == 1: opponent = 2 
    else: opponent = 1

    start_tile = get_tile(row, col, player)

    streaks = []

    for direction, (dr, dc) in DIRECTIONS.items():

        back_r, back_c = row - dr, col - dc
        if 0 <= back_r < ROW_COUNT and 0 <= back_c < COL_COUNT:
            if board[back_r][back_c] == player:
                continue

        members = [start_tile]
        open_end = True
        open_start = True
        # walk forward
        r, c = row + dr, col + dc
        while 0 <= r < ROW_COUNT and 0 <= c < COL_COUNT and board[r][c] == player:
            new_tile = get_tile(r, c, player)
            if direction not in new_tile.streaks:
                members.append(new_tile)
            r += dr
            c += dc
        # If next tile is out of bounds or owned by opponent, mark as closed
        if 0 > r or ROW_COUNT <= r or 0 > c or COL_COUNT <= c:
            open_end = False

        elif board[r][c] == opponent:
            open_end = False
    
        if 0 <= back_r < ROW_COUNT and 0 <= back_c < COL_COUNT:
            open_start = board[back_r][back_c] != opponent
        else:
            open_start = False

        if len(members) > 1:
            new_streak = Streak(members[0], members, open_end, open_start, direction)
            streaks.append(new_streak)
            
            for member in members:
                tile_registry[(member.position[0], member.position[1])].streaks[direction] = new_streak

    return streaks, tile_registry

def calculate_scores(streaks):
    score = 0
    len_scoring = {1:0, 2:2, 3:6, 4:60, 5:1_000_000}
    ends_multipliers = {(True, True): 3, (True, False): 1, (False, True): 1, (False, False): 0}

    for streak in streaks:
        len_score = len_scoring[len(streak.members)]
        ends_multiplier = ends_multipliers[streak.open_end, streak.open_start]
        score += len_score*ends_multiplier

    return score

def evaluate(board, ROW_COUNT, COL_COUNT):
    ai_streaks = []
    player_streaks = []

    tile_registry = {}


    for r in range(ROW_COUNT):
        for c in range(COL_COUNT):
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

    player_score = calculate_scores(player_streaks)
    ai_score = calculate_scores(ai_streaks)

    return ai_score - player_score


def minimax(board, depth, ROW_COUNT, COL_COUNT, maximizing = True, move = None):

    if move:
        if depth == 0 or check_win(board, move[0], move[1], 2):
            return evaluate(board, ROW_COUNT, COL_COUNT), move

    if maximizing:
        best = -inf
        goat_move = None
        candidates = get_candidates(board, ROW_COUNT, COL_COUNT)
        for move in candidates:
            board = place_mark(board, move, 2)
            score, best_move = minimax(board, depth - 1, ROW_COUNT, COL_COUNT, False, move)
            board = remove_mark(board, move)
            if score > best:
                best = score
                goat_move = best_move
        return best, goat_move
            
    else:
        best = inf
        candidates = get_candidates(board, ROW_COUNT, COL_COUNT)
        for move in candidates:
            board = place_mark(board, move, 1)
            score, best_move = minimax(board, depth - 1, ROW_COUNT, COL_COUNT, True, move)
            board = remove_mark(board, move)
            if score > best:
                best = score
        return best, best_move
        