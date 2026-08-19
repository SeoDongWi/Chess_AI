import chess
import random
import csv
from first_milestone import random_choice
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

game_result = {
    "white" : None, #minimax_ai
    "black" : None, #random_ai
    "result" : None, #1-0
    "termination" : None, #outcome = board.outcome(claim_draw = True).termination
    "moves" : None, #" ".join(move.uci() for move in board.move_stack)
    "moves_count" : None, #len(board.move_stack)
    "game_time" : None, # time.perf_counter() - start_time
    "white_search_time" : 0.00, #white_search_time + time.perf_counter() - start_time
    "black_search_time" : 0.00, #black_search_time + time.perf_counter() - start_time
    
}