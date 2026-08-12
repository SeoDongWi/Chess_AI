import chess

import second_milestone as milestone


def create_black_win_board():
    """Fool's Mate로 흑이 승리한 보드를 만든다."""
    board = chess.Board()

    for move in ["f2f3", "e7e5", "g2g4", "d8h4"]:
        board.push_uci(move)

    return board


def create_white_win_board():
    """Scholar's Mate로 백이 승리한 보드를 만든다."""
    board = chess.Board()

    for move in [
        "e2e4",
        "e7e5",
        "d1h5",
        "b8c6",
        "f1c4",
        "g8f6",
        "h5f7",
    ]:
        board.push_uci(move)

    return board


# ISSUE 9~11: 기물 점수와 보드 평가


def test_piece_scores_include_all_piece_types():
    expected_piece_types = {
        chess.PAWN,
        chess.KNIGHT,
        chess.BISHOP,
        chess.ROOK,
        chess.QUEEN,
        chess.KING,
    }

    assert set(milestone.piece_scores) == expected_piece_types


def test_initial_piece_scores_are_equal():
    board = chess.Board()

    assert milestone.calculate_scores(board) == [138, 138]
    assert milestone.board_scores(board) == 0


def test_white_material_advantage_is_positive():
    board = chess.Board(
        "7k/8/8/8/8/8/4Q3/4K3 w - - 0 1"
    )

    assert milestone.board_scores(board) == 9


def test_black_material_advantage_is_negative():
    board = chess.Board(
        "7k/4q3/8/8/8/8/8/4K3 w - - 0 1"
    )

    assert milestone.board_scores(board) == -9


# ISSUE 12: 종료된 포지션 평가


def test_white_checkmate_win_score():
    assert milestone.board_scores(create_white_win_board()) == 999


def test_black_checkmate_win_score():
    assert milestone.board_scores(create_black_win_board()) == -999


def test_draw_score_is_zero():
    board = chess.Board(
        "8/8/8/8/8/8/4K3/7k w - - 0 1"
    )

    assert board.is_insufficient_material()
    assert milestone.board_scores(board) == 0


# ISSUE 13~16: Minimax와 Alpha-Beta Pruning


def test_minimax_does_not_change_board():
    board = chess.Board()
    original_fen = board.fen()

    score = milestone.minimax(board, 2)

    assert score == 0
    assert board.fen() == original_fen


def test_alpha_beta_matches_minimax():
    board = chess.Board()

    minimax_score = milestone.minimax(board, 2)
    alpha_beta_score = milestone.minimax_alpha_beta_pruning(
        board,
        2,
        float("-inf"),
        float("inf"),
    )

    assert alpha_beta_score == minimax_score


def test_alpha_beta_does_not_change_board():
    board = chess.Board()
    original_fen = board.fen()

    milestone.minimax_alpha_beta_pruning(
        board,
        2,
        float("-inf"),
        float("inf"),
    )

    assert board.fen() == original_fen


# ISSUE 14~17: 최적 수 선택과 대국 연결


def test_choose_best_move_is_legal_and_preserves_board(capsys):
    board = chess.Board()
    original_fen = board.fen()

    move = milestone.choose_best_move(board, 2)
    output = capsys.readouterr().out

    assert move in board.legal_moves
    assert board.fen() == original_fen
    assert "선택한 수" in output
    assert "평가 점수" in output


def test_choose_best_move_returns_none_when_game_over():
    board = create_black_win_board()

    assert milestone.choose_best_move(board, 2) is None


def test_play_chess_can_quit(monkeypatch, capsys):
    board = chess.Board()
    monkeypatch.setattr("builtins.input", lambda _: "quit")

    milestone.play_chess_with_minimax(board)
    output = capsys.readouterr().out

    assert "게임이 종료되었습니다!" in output
    assert len(board.move_stack) == 0
