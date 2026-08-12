import chess
import time
from first_milestone import game_state, who_is_turn, user_input

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
    board = chess.Board()
    for depth in [1,2,3,4]:
        start_time = time.perf_counter()
        move = choose_best_move(board, depth)
        taken_time = time.perf_counter() - start_time
        print(
            f"깊이 : {depth}",
            f"선택한 수 : {move}",
            f"탐색시간 : {taken_time:.5f}초",
        )
        print()

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


def minimax_alpha_beta_pruning(board, depth, alpha, beta): #alpha is qualified_max_value and beta is qualified_min_value.

    outcome = board.outcome(claim_draw=True)

    if depth <= 0 or outcome is not None:
        return board_scores(board)

    if board.turn == chess.WHITE:
        best_score = float("-inf")
        for move in board.legal_moves:
            board.push(move)
            score = minimax_alpha_beta_pruning(board, depth-1, alpha, beta)
            board.pop()
            best_score = max(best_score, score)
            alpha = max(alpha, best_score)
            if alpha >= beta:
                return best_score 
        return best_score

    else:
        best_score = float("inf")
        for move in board.legal_moves:
            board.push(move)
            score = minimax_alpha_beta_pruning(board, depth-1, alpha, beta)
            board.pop()
            best_score = min(best_score, score)
            beta = min(beta, best_score)
            if beta <= alpha:
                return best_score
        return best_score


def choose_best_move(board,depth):

    if board.turn == chess.WHITE:
        chosen_move = None
        score = float("-inf")
        for move in board.legal_moves:
            board.push(move)
            moved_score = minimax_alpha_beta_pruning(board, depth-1, float("-inf"), float("inf"))
            if score < moved_score:
                score = moved_score
                chosen_move = move
            board.pop()
        return chosen_move

    else:
        chosen_move = None
        score = float("inf")
        for move in board.legal_moves:
            board.push(move)
            moved_score = minimax(board, depth-1)
            if score > moved_score:
                score = moved_score
                chosen_move = move
            board.pop()
        return chosen_move
        



if __name__ == "__main__":
    main()