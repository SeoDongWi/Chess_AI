import chess

import first_milestone as milestone


def create_checkmate_board():
    """백이 체크메이트된 Fool's Mate 보드를 만든다."""
    board = chess.Board()

    for move in ["f2f3", "e7e5", "g2g4", "d8h4"]:
        board.push_uci(move)

    return board


# ISSUE 2: 체스판 생성, 차례 및 FEN


def test_initial_board():
    board = chess.Board()

    assert board.fen() == chess.STARTING_FEN
    assert len(list(board.legal_moves)) == 20


def test_who_is_turn():
    board = chess.Board()

    assert milestone.who_is_turn(board) is True

    board.push_uci("e2e4")

    assert milestone.who_is_turn(board) is False


# ISSUE 3: 사용자 입력


def test_valid_user_input(monkeypatch):
    board = chess.Board()

    monkeypatch.setattr(
        "builtins.input",
        lambda _: "e2e4",
    )

    move = milestone.user_input(board)

    assert move == chess.Move.from_uci("e2e4")


def test_invalid_input_then_valid_input(monkeypatch):
    board = chess.Board()
    answers = iter(["abc", "e2e5", "e2e4"])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(answers),
    )

    move = milestone.user_input(board)

    assert move == chess.Move.from_uci("e2e4")


def test_quit(monkeypatch):
    board = chess.Board()

    monkeypatch.setattr(
        "builtins.input",
        lambda _: "quit",
    )

    assert milestone.user_input(board) is None


# ISSUE 4: 랜덤 AI


def test_random_choice_is_legal():
    board = chess.Board()
    legal_moves = list(board.legal_moves)

    move = milestone.random_choice(board)

    assert move in legal_moves


def test_random_choice_when_game_is_over():
    board = create_checkmate_board()

    move = milestone.random_choice(board)

    assert move is None


# ISSUE 5: 게임 상태 판정


def test_game_is_in_progress():
    board = chess.Board()

    assert milestone.game_state(board) is True


def test_check():
    board = chess.Board()

    for move in ["e2e4", "f7f6", "d1h5"]:
        board.push_uci(move)

    result = milestone.game_state(board)

    assert board.is_check()
    assert result is True


def test_checkmate():
    board = create_checkmate_board()

    result = milestone.game_state(board)

    assert board.is_checkmate()
    assert result is False


def test_stalemate():
    board = chess.Board(
        "7k/5Q2/6K1/8/8/8/8/8 b - - 0 1"
    )

    result = milestone.game_state(board)

    assert board.is_stalemate()
    assert result is False


def test_insufficient_material():
    board = chess.Board(
        "8/8/8/8/8/8/4K3/7k w - - 0 1"
    )

    result = milestone.game_state(board)

    assert board.is_insufficient_material()
    assert result is False


def test_fifty_move_rule():
    board = chess.Board(
        "8/8/8/8/8/8/R3K3/7k w - - 100 51"
    )

    result = milestone.game_state(board)

    assert board.can_claim_fifty_moves()
    assert result is False


def test_threefold_repetition():
    board = chess.Board()

    moves = [
        "g1f3",
        "g8f6",
        "f3g1",
        "f6g8",
    ] * 2

    for move in moves:
        board.push_uci(move)

    result = milestone.game_state(board)

    assert board.can_claim_threefold_repetition()
    assert result is False
    
