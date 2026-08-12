import chess
import random
import csv
from first_milestone import random_choice
from second_milestone import choose_best_move, minimax_alpha_beta_pruning, board_scores, calculate_scores

def random_agent(board, depth):
    return random_choice(board)

def minimax_agent(board, depth):
    return choose_best_move(board, depth)

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