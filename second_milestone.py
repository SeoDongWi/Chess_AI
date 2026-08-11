import chess
from first_milestone import game_state, who_is_turn, user_input

board = chess.Board()
def main():
    print("Minimax AI 모듈을  실행 합니다.")
    print(board)

piece_scores = {
    chess.PAWN : 1,
    chess.KNIGHT : 3,
    chess.BISHOP : 3,
    chess.ROOK : 5,
    chess.QUEEN : 9,
    chess.KING : 99
}
if __name__ == "__main__":
    main()