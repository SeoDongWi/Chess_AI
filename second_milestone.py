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

def board_scores(board):
    outcome = board.outcome(claim_draw = True)
    if outcome is not None:
        result = outcome.result()
        if result == "1-0":
            return 999
        elif result == "0-1":
            return -999
        else:
            return 0

    scores = calculate_scores(board)
    board_score = scores[0] -  scores[1]
    return board_score

def minimax(board, depth):

    outcome = board.outcome(claim_draw=True)

    if depth <= 0 or outcome is not None:
        return board_scores(board)

    legal_score = []

    for move in board.legal_moves:
        board.push(move)
        legal_score.append(minimax(board,depth-1))
        board.pop()

    if board.turn == chess.WHITE:
        return max(legal_score)
    else:
        return min(legal_score)



if __name__ == "__main__":
    main()