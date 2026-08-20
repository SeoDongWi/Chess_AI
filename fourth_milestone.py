## 학습 목표

# 체스판의 현재 상태를 입력 받아 마스터가 선택한 다음 수를 예측한다.

## 데이터의 한 행

# game_id, fen, ply, turn, move_uci, result_label

# result_label = white_win 1, draw 0, black_win -1

# 원본은 data/raw, 가공 데이터는 data/processed 그 외의 train,validation등은 data/splits에 저장한다.
