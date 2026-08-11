import chess
from first_milestone import game_state, who_is_turn, user_input

board = chess.Board()

piece_scores = {
    chess.PAWN : 1,
    chess.KNIGHT : 3,
    chess.BISHOP : 3,
    chess.ROOK : 5,
    chess.QUEEN : 9,
    chess.KING : 99
}

def main():
    print("Minimax AI 모듈을  실행 합니다.")
    print(board)

def calculate_scores(board):
    white_score = 0
    black_score = 0
    for piece_type, score in piece_scores.items():
        white_count = len(board.pieces(piece_type, chess.WHITE))
        black_count = len(board.pieces(piece_type, chess.BLACK))
        white_score += score * white_count
        black_score += score * black_count
    return [white_score, black_score]
        
if __name__ == "__main__":
    main()