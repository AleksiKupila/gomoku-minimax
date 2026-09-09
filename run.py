from argparse import ArgumentParser
import gomoku, gomoku_pvp

if __name__ == "__main__":

    parser = ArgumentParser(
        prog="Gomoku-Minimax",
        description="Minimax algorithm for Gomoku, built with Python"
    )
    parser.add_argument('-m', '--minimax', action='store_true', default=False, help="Play against minimax algorithm")
    parser.add_argument('-a', '--alpha_beta', action='store_true', default=False, help="Enable alpha-beta pruning")
    parser.add_argument('-d', '--depth', type=int, default=3, help="Algorithm search depth")
    parser.add_argument('-p', '--performance_metrics', action='store_true', default=False, help="Enable performance metrics")
    parser.add_argument('-r', '--row_count', type=int, default=10, help="Game board row count")
    parser.add_argument('-c', '--col_count', type=int, default=10, help="Game board column count")
    args = parser.parse_args()

    print(f"---------- GOMOKU-MINIMAX ----------")
    print(f"Minimax: {args.minimax}, alpha-beta pruning: {args.alpha_beta}, depth: {args.depth}, performance metrics: {args.performance_metrics}, rows: {args.row_count}, columns: {args.col_count}\n")
    if args.minimax:
        gomoku.play(args.alpha_beta, args.depth, args.performance_metrics, args.row_count, args.col_count)
    else:
        gomoku_pvp.play()

    
