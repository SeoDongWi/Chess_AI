import chess
import time
import pandas as pd
from pathlib import Path
from first_milestone import random_choice, game_state
from second_milestone import choose_best_move

def random_agent(board, depth):
    return random_choice(board, False)

def minimax_agent(board, depth):
    return choose_best_move(board, depth, False)

random_ai = {
    "name" : "random_v1",
    "depth" : None,
    "choose_move" : random_agent,
}

minimax_ai = {
    "name" : "minimax_depth_2",
    "depth" : 2,
    "choose_move" : minimax_agent,
}

# move = random_ai["choose_move"](board, random_ai["depth"]) 
# move = minimax_ai["choose_move"](board, minimax_ai["depth"])

# white_name = random_ai["name"]
# black_name = random_ai["name"]


def play_chess_without_user(white_ai, black_ai, board, verbose=False):

    game_result = {
    "white" : None, #minimax_ai
    "black" : None, #random_ai
    "result" : None, #1-0
    "termination" : None, #outcome = board.outcome(claim_draw = True).termination.name
    "moves" : None, #" ".join(move.uci() for move in board.move_stack)
    "moves_count" : None, #len(board.move_stack)
    "white_moves_count" : None,
    "black_moves_count" : None,
    "game_time" : None, # time.perf_counter() - start_time
    "white_average_search_time" : None,
    "white_search_time" : 0.00, #white_search_time + time.perf_counter() - start_time
    "black_average_search_time" : None,
    "black_search_time" : 0.00, #black_search_time + time.perf_counter() - start_time


    }

    game_result["white"] = white_ai["name"]
    game_result["black"] = black_ai["name"]
    game_start_time = time.perf_counter()

    while game_state(board, verbose):
        
        if board.turn == chess.WHITE:
            white_time = time.perf_counter()
            move = white_ai["choose_move"](board, white_ai["depth"])
            game_result["white_search_time"] += time.perf_counter() - white_time
            board.push(move)

        else:
            black_time = time.perf_counter()
            move =  black_ai["choose_move"](board, black_ai["depth"])
            game_result["black_search_time"] += time.perf_counter()- black_time
            board.push(move)

    outcome = board.outcome(claim_draw = True)
    length = len(board.move_stack)

    game_result["result"] = outcome.result()
    game_result["termination"] = outcome.termination.name
    game_result["moves"] = " ".join(move.uci() for move in board.move_stack)
    game_result["moves_count"] = length
    game_result["white_moves_count"] = (length + 1) // 2
    game_result["black_moves_count"] = length // 2
    game_result["game_time"] = time.perf_counter() - game_start_time

    if game_result["white_moves_count"] > 0:
        game_result["white_average_search_time"] = round(
        game_result["white_search_time"] / game_result["white_moves_count"], 6)
    else:
        game_result["white_average_search_time"] = 0.000000
    
    game_result["white_search_time"] = round(game_result["white_search_time"], 2)

    if game_result["black_moves_count"] > 0:
        game_result["black_average_search_time"] = round(
            game_result["black_search_time"] / game_result["black_moves_count"], 6)
    else:
        game_result["black_average_search_time"] = 0.000000

    game_result["black_search_time"] = round(game_result["black_search_time"], 2)
    
    return game_result

def make_csv_file(game_results):

    base_dir = Path(__file__).resolve().parent
    data_dir = base_dir / "data" / "results"
    csv_path = data_dir / "game_results.csv"
    data_dir.mkdir(parents=True,exist_ok=True)

    dataframe = pd.DataFrame(game_results)

    dataframe.to_csv(
        csv_path,
        index=False,
        encoding="utf-8-sig",
        mode="w",
    )

    loaded_dataframe = pd.read_csv(csv_path)

    return loaded_dataframe

def make_ai_data_csv(data):

    base_dir = Path(__file__).resolve().parent
    data_dir = base_dir / "data" / "results"
    csv_path = data_dir / "ai_results.csv"
    data_dir.mkdir(parents=True,exist_ok=True)

    data.to_csv(
        csv_path,
        index=False,
        encoding="utf-8-sig",
        mode="w",
    )
 
def calculate_performance_statistics(data):

    data = data.copy()

    data["winner"] = "draw"
    data["loser"] = "draw"
    white_win = data["result"] == "1-0"
    black_win = data["result"] == "0-1"

    data.loc[white_win, "winner"] = data.loc[white_win, "white"]
    data.loc[white_win, "loser"] = data.loc[white_win, "black"]

    data.loc[black_win, "winner"] = data.loc[black_win, "black"]
    data.loc[black_win, "loser"] = data.loc[black_win, "white"]

    win_counts = data["winner"].value_counts()
    loss_counts = data["loser"].value_counts()
    draw_count = (data["result"] == "1/2-1/2").sum()
    total_games = len(data)

    average_game_length = (
        (data["moves_count"] + 1) // 2
    ).mean()

    white_search = data[
        ["white", "white_search_time", "white_moves_count"]
    ].rename(columns={
        "white" : "ai",
        "white_search_time" : "search_time",
        "white_moves_count" : "move_count",
    })

    black_search = data[
        ["black", "black_search_time", "black_moves_count"]
    ].rename(columns={
        "black" : "ai",
        "black_search_time" : "search_time",
        "black_moves_count" : "move_count",
    })

    all_search = pd.concat([white_search, black_search], ignore_index=True,)

    ai_search_groupby = all_search.groupby(
        "ai",
        as_index=False,
    ).agg(
        total_search_time=("search_time", "sum"),
        total_move_count=("move_count", "sum"),
    )

    ai_search_groupby["average_search_time"] = (
        ai_search_groupby["total_search_time"] / ai_search_groupby["total_move_count"]
    )

    ai_search_groupby["average_search_time"] = (
        ai_search_groupby["average_search_time"].round(6)
    )

    ai_search_groupby["total_search_time"] = (
        ai_search_groupby["total_search_time"].round(6)
    )

    ai_performance = ai_search_groupby.copy()

    ai_performance["wins"] = (
        ai_performance["ai"].map(win_counts).fillna(0).astype(int)
    )

    ai_performance["draws"] = draw_count

    ai_performance["losses"] = (
        ai_performance["ai"].map(loss_counts).fillna(0).astype(int)
    )

    ai_performance["win_rate"] = (
        ai_performance["wins"] / total_games * 100
    ).round(2)

    ai_performance["draw_rate"] = (
        ai_performance["draws"] / total_games * 100
    ).round(2)

    ai_performance["loss_rate"] = (
        ai_performance["losses"] / total_games * 100
    ).round(2)

    ai_performance["average_game_length"] = round(
    average_game_length, 2
    )

    ai_performance = ai_performance[[
        "ai",
        "wins",
        "draws",
        "losses",
        "win_rate",
        "draw_rate",
        "loss_rate",
        "average_game_length",
        "average_search_time",
        "total_search_time",
    ]]

    return ai_performance
if __name__ == "__main__":
    game_results = []
    
    for i in range(4):
        board = chess.Board()
        if (i % 2) == 0:
            game_results.append(play_chess_without_user(random_ai, minimax_ai, board, False))
        else:
            game_results.append(play_chess_without_user(minimax_ai, random_ai, board, False))
    data = make_csv_file(game_results)
    ai_data = calculate_performance_statistics(data)
    make_ai_data_csv(ai_data)