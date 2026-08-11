import chess
import random

#체스판 생성 ISSUE 2
# print(board)

# 차례가 누구인지 판별
def who_is_turn(board):
    if board.turn == chess.WHITE:
        print("백 차례")
        return True
    else:
        print("흑 차례")
        return False

# # fen 생성 (chess의 현재상태를 나타냄)
# fen = board.fen()
# print(fen)


# ISSUE 3
def user_input(board):


    while True:
        user = input(f"알맞은 수(UCI)를 입력해주세요:")
        if user == "quit":
            return None  
        try:
            move = chess.Move.from_uci(user)
        except ValueError:
            print("UCI형식에 맞지 않습니다!")
            continue
        if move not in board.legal_moves:
            print("불가능한 수 입니다")
            continue
        else:
            print("다음 차례를 진행합니다.")
            return move

# move = user_input()

# board.push(move)
# print(board)

# ISSUE 4
def random_choice(board):
    if board.is_game_over():
        print("경기가 종료된 상태입니다.")
        return None
    move = random.choice(list(board.legal_moves))
    print(f"랜덤 선택된 UCI는 :{move}")
    return move

# move = random_choice(board)
# if move is not None :
#     board.push(move)
#     print(board)

# ISSUE 5

def game_state(board):
    outcome = board.outcome(claim_draw = True)

    if outcome is None:
        if board.is_check():
            print(f"체크!")
        ## 게임이 진행중이니 True
        return True

    termination = outcome.termination
    if termination == chess.Termination.CHECKMATE:
        print("체크메이트!")
    elif termination == chess.Termination.STALEMATE:
        print("스테일메이트!")
    elif termination == chess.Termination.INSUFFICIENT_MATERIAL:
        print("기물 부족으로 무승부!")
    elif termination == chess.Termination.FIFTY_MOVES:
        print("50수 규칙으로 무승부!")
    elif termination == chess.Termination.THREEFOLD_REPETITION:
        print("3회 반복으로 무승부!")
    else:
        print(f"기타 종료 원인: {termination.name}!")

    result = outcome.result()
    if result == "1-0":
        print("WHITE WIN!!!")
    elif result == "0-1":
        print("BLACK WIN!!")
    else:
        print("DRAW!!!")

    ##게임이 끝났으니 False 
    return False

# ISSUE 6
def play_chess(board):
    print("체스 게임 스타트!")
    print("종료를 원하신다면 'quit'를 입력해주세요. ")
    while game_state(board):
        print(board)

        if who_is_turn(board):
            move = user_input(board)
            if move is None:
                print("게임이 종료되었습니다.")
                break
            board.push(move)
        else:
            move = random_choice(board)
            board.push(move)
    print(board)

if __name__ == "__main__":
    board = chess.Board()
    play_chess(board)


