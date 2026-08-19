import chess
import random
import csv
import time
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
    "white_search_time" : 0.00, #white_search_time + time.perf_counter() - start_time
    "white_average_search_time" : None,
    "black_search_time" : 0.00, #black_search_time + time.perf_counter() - start_time
    "black_average_search_time" : None,

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
        game_result["white_search_time"] / game_result["white_moves_count"], 6
        )
    else:
        game_result["white_average_search_time"] = 0.000000
    
    game_result["white_search_time"] = round(game_result["white_search_time"], 2)

    if game_result["black_moves_count"] > 0:
        game_result["black_average_search_time"] = round(
            game_result["black_search_time"] / game_result["black_moves_count"], 6
        )
    else:
        game_result["black_average_search_time"] = 0.000000

    game_result["black_search_time"] = round(game_result["black_search_time"], 2)
    
    return game_result



if __name__ == "__main__":
    game_results = []
    
    for i in range(4):
        board = chess.Board()
        if (i % 2) == 0:
            game_results.append(play_chess_without_user(random_ai, minimax_ai, board, False))
        else:
            game_results.append(play_chess_without_user(minimax_ai, random_ai, board, False))
    print(game_results)