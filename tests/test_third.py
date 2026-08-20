import chess
import pandas as pd

import third_milestone as milestone


WHITE_MATE_MOVES = ["f2f3", "g2g4"]
BLACK_MATE_MOVES = ["e7e5", "d8h4"]


def create_scripted_ai(name, moves):
    """정해진 합법 수를 순서대로 선택하는 테스트용 AI를 만든다."""
    moves = iter(moves)

    def choose_move(board, depth):
        move = chess.Move.from_uci(next(moves))
        assert move in board.legal_moves
        return move

    return {
        "name": name,
        "depth": None,
        "choose_move": choose_move,
    }


def create_sample_results():
    """통계와 CSV 저장을 검증할 네 경기의 결과를 만든다."""
    return [
        {
            "white": "minimax_depth_2",
            "black": "random_v1",
            "result": "1-0",
            "termination": "CHECKMATE",
            "moves": "e2e4 e7e5",
            "moves_count": 20,
            "white_moves_count": 10,
            "black_moves_count": 10,
            "game_time": 2.1,
            "white_average_search_time": 0.2,
            "white_search_time": 2.0,
            "black_average_search_time": 0.01,
            "black_search_time": 0.1,
        },
        {
            "white": "random_v1",
            "black": "minimax_depth_2",
            "result": "0-1",
            "termination": "CHECKMATE",
            "moves": "d2d4 d7d5",
            "moves_count": 30,
            "white_moves_count": 15,
            "black_moves_count": 15,
            "game_time": 3.2,
            "white_average_search_time": 0.013333,
            "white_search_time": 0.2,
            "black_average_search_time": 0.2,
            "black_search_time": 3.0,
        },
        {
            "white": "minimax_depth_2",
            "black": "random_v1",
            "result": "1/2-1/2",
            "termination": "STALEMATE",
            "moves": "c2c4 c7c5",
            "moves_count": 40,
            "white_moves_count": 20,
            "black_moves_count": 20,
            "game_time": 4.4,
            "white_average_search_time": 0.2,
            "white_search_time": 4.0,
            "black_average_search_time": 0.02,
            "black_search_time": 0.4,
        },
        {
            "white": "random_v1",
            "black": "minimax_depth_2",
            "result": "1/2-1/2",
            "termination": "STALEMATE",
            "moves": "g1f3 g8f6",
            "moves_count": 10,
            "white_moves_count": 5,
            "black_moves_count": 5,
            "game_time": 1.1,
            "white_average_search_time": 0.02,
            "white_search_time": 0.1,
            "black_average_search_time": 0.2,
            "black_search_time": 1.0,
        },
    ]


# ISSUE 28: AI가 합법적인 수만 선택하는지 검사


def test_random_agent_selects_legal_move_without_changing_board():
    board = chess.Board()
    original_fen = board.fen()

    move = milestone.random_agent(board, None)

    assert move in board.legal_moves
    assert board.fen() == original_fen


def test_minimax_agent_selects_legal_move_without_changing_board():
    board = chess.Board()
    original_fen = board.fen()

    move = milestone.minimax_agent(board, 1)

    assert move in board.legal_moves
    assert board.fen() == original_fen


# ISSUE 28: 색상 교대와 결과 형식 검사


def test_automatic_game_result_format():
    white_ai = create_scripted_ai("agent_a", WHITE_MATE_MOVES)
    black_ai = create_scripted_ai("agent_b", BLACK_MATE_MOVES)

    result = milestone.play_chess_without_user(
        white_ai,
        black_ai,
        chess.Board(),
    )

    expected_fields = {
        "white",
        "black",
        "result",
        "termination",
        "moves",
        "moves_count",
        "white_moves_count",
        "black_moves_count",
        "game_time",
        "white_average_search_time",
        "white_search_time",
        "black_average_search_time",
        "black_search_time",
    }

    assert set(result) == expected_fields
    assert result["white"] == "agent_a"
    assert result["black"] == "agent_b"
    assert result["result"] == "0-1"
    assert result["termination"] == "CHECKMATE"
    assert result["moves"] == "f2f3 e7e5 g2g4 d8h4"
    assert result["moves_count"] == 4
    assert result["white_moves_count"] == 2
    assert result["black_moves_count"] == 2
    assert result["game_time"] >= 0


def test_automatic_game_uses_swapped_colors():
    first_result = milestone.play_chess_without_user(
        create_scripted_ai("agent_a", WHITE_MATE_MOVES),
        create_scripted_ai("agent_b", BLACK_MATE_MOVES),
        chess.Board(),
    )
    second_result = milestone.play_chess_without_user(
        create_scripted_ai("agent_b", WHITE_MATE_MOVES),
        create_scripted_ai("agent_a", BLACK_MATE_MOVES),
        chess.Board(),
    )

    assert first_result["white"] == second_result["black"] == "agent_a"
    assert first_result["black"] == second_result["white"] == "agent_b"
    assert first_result["result"] in {"1-0", "0-1", "1/2-1/2"}
    assert second_result["result"] in {"1-0", "0-1", "1/2-1/2"}


# ISSUE 28: CSV 저장 및 지표 계산 테스트


def test_csv_save_and_reload(monkeypatch, tmp_path):
    game_results = create_sample_results()
    monkeypatch.setattr(
        milestone,
        "Path",
        lambda _: tmp_path / "third_milestone.py",
    )

    loaded_data = milestone.make_csv_file(game_results)
    csv_path = tmp_path / "data" / "game_results.csv"

    assert csv_path.exists()
    assert len(loaded_data) == len(game_results)
    assert list(loaded_data.columns) == list(game_results[0])
    assert loaded_data.loc[0, "white"] == "minimax_depth_2"
    assert loaded_data.loc[1, "result"] == "0-1"


def test_performance_statistics():
    data = pd.DataFrame(create_sample_results())

    performance = milestone.calculate_performance_statistics(data)
    performance = performance.set_index("ai")

    minimax = performance.loc["minimax_depth_2"]
    random = performance.loc["random_v1"]

    assert minimax["wins"] == 2
    assert minimax["draws"] == 2
    assert minimax["losses"] == 0
    assert minimax["win_rate"] == 50.0
    assert minimax["draw_rate"] == 50.0
    assert minimax["loss_rate"] == 0.0
    assert minimax["average_game_length"] == 12.5
    assert minimax["total_search_time"] == 10.0
    assert minimax["average_search_time"] == 0.2

    assert random["wins"] == 0
    assert random["draws"] == 2
    assert random["losses"] == 2
    assert random["win_rate"] == 0.0
    assert random["draw_rate"] == 50.0
    assert random["loss_rate"] == 50.0
    assert random["average_game_length"] == 12.5
    assert random["total_search_time"] == 0.8
    assert random["average_search_time"] == 0.016


def test_ai_statistics_csv_save(monkeypatch, tmp_path):
    data = pd.DataFrame(create_sample_results())
    performance = milestone.calculate_performance_statistics(data)
    monkeypatch.setattr(
        milestone,
        "Path",
        lambda _: tmp_path / "third_milestone.py",
    )

    milestone.make_ai_data_csv(performance)
    csv_path = tmp_path / "data" / "ai_results.csv"
    loaded_performance = pd.read_csv(csv_path)

    assert csv_path.exists()
    assert len(loaded_performance) == 2
    assert set(loaded_performance["ai"]) == {
        "minimax_depth_2",
        "random_v1",
    }
