from board import Board
from datetime import datetime

sqs = [[' ', ' ', ' ', ' ', ' ', ' ', ' '],
       [' ', ' ', ' ', ' ', ' ', ' ', ' '],
       [' ', ' ', ' ', ' ', ' ', ' ', ' '],
       [' ', ' ', ' ', ' ', ' ', ' ', ' '],
       [' ', ' ', ' ', ' ', ' ', ' ', ' '],
       [' ', ' ', ' ', ' ', ' ', ' ', ' ']]
my_board = Board(sqs)
# SINGLE PLAYER
while True:
    my_board.print_board()
    userInput = 0
    while True:
        userInput = int(input(f'Enter column: ')) - 1
        if 6 >= userInput >= 0 and not my_board.is_full(userInput):
            break
    last_move = my_board.place_piece(userInput, '●')
    if my_board.check_win(last_move) == -10:
        my_board.print_board()
        print(f'PLAYER ● WINS')
        exit()

    start_time = datetime.now()
    best_move = my_board.get_best_move()
    end_time = datetime.now()
    print(f'Duration: {format(end_time - start_time)}')

    last_move = my_board.place_piece(best_move, '○')
    if my_board.check_win(last_move) == 10:
        my_board.print_board()
        print(f'PLAYER ○ WINS')
        exit()


# MULTIPLAYER
# turn = '●'
# while True:
#     userInput = 0
#     while True:
#         userInput = int(input(f'Enter column for {turn}: ')) - 1
#         if 6 >= userInput >= 0 and not my_board.is_full(userInput):
#             break
#     last_move = my_board.place_piece(userInput, turn)
#     my_board.print_board()
#     if abs(my_board.check_win(last_move)) == 10:
#         print(f'PLAYER {turn} WINS')
#         exit()
#     turn = '●' if turn == '○' else '○'
