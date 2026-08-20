import chess.pgn
from pathlib import Path

def one_game():

    def check_int(value):
        try:
            return int(value)
        except (TypeError, ValueError):
            return None
    total_game = 0
    game_id = 0
    chess_result = ["1-0", "1/2-1/2", "0-1"]
    base_dir = Path(__file__).resolve().parent
    data_dir = base_dir / "data" / "raw"
    pgn_path = data_dir / "lichess_db_broadcast_2025-12.pgn"
    with open(pgn_path, encoding="utf-8") as pgn_file:
        while True:
            
            game = chess.pgn.read_game(pgn_file)
            if game is None or game_id >= 1000:
                print(f"읽은 전체 경기수 : {total_game}")
                print(f"마지막 game_id : {game_id}")
                return
            
            total_game += 1 
            white_elo = check_int(game.headers.get("WhiteElo"))
            black_elo = check_int(game.headers.get("BlackElo"))
            if white_elo is None or black_elo is None:
                continue

            
            if white_elo < 2300 or black_elo < 2300:
                continue

            white_fide_id = game.headers.get("WhiteFideId")
            black_fide_id = game.headers.get("BlackFideId")
            if white_fide_id is None or black_fide_id is None:
                continue

            result = game.headers.get("Result")
            if result not in chess_result:
                continue

            variant = game.headers.get("Variant", "standard")
            if variant.lower() != "standard":
                continue

            game_id += 1
            # board = game.board()
            # for move in game.mainline_moves():
            #     board.push(move)



if __name__ == "__main__":
    one_game()