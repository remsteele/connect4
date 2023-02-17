import random


class Board:
    def __init__(self, sqs):
        self.sqs = sqs

    def print_board(self):
        for i in range(len(self.sqs)):
            print(
                f'| {self.sqs[i][0]} | {self.sqs[i][1]} | {self.sqs[i][2]} | {self.sqs[i][3]} '
                f'| {self.sqs[i][4]} | {self.sqs[i][5]} | {self.sqs[i][6]} |')
        print('  1   2   3   4   5   6   7   ')

    def is_full(self, column):
        for i in range(len(self.sqs)):
            if self.sqs[i][column] == ' ':
                return False
        return True

    def place_piece(self, column, player):
        for i in range(len(self.sqs)):
            if self.sqs[len(self.sqs) - i - 1][column] == ' ':
                self.sqs[len(self.sqs) - i - 1][column] = player
                return len(self.sqs) - i - 1, column
        print('CANT PLAY MOVE ERROR')
        return None

    def remove_piece(self, column):
        for i in range(len(self.sqs)):
            if self.sqs[i][column] != ' ':
                self.sqs[i][column] = ' '
                break

    def check_win(self, p):
        for i in [[0, 1, 2, 3], [-1, 0, 1, 2], [-2, -1, 0, 1], [-3, -2, -1, 0]]:
            for j in [[0, 1], [1, 0], [1, 1], [-1, 1]]:
                if self.__valid(p, j[0] * i[0], j[1] * i[0]) == self.__valid(p, j[0] * i[1], j[1] * i[1]) \
                        == self.__valid(p, j[0] * i[2], j[1] * i[2]) == self.__valid(p, j[0] * i[3], j[1] * i[3]):
                    if self.__valid(p, j[0] * i[0], j[1] * i[0]) == '○':
                        return 10
                    elif self.__valid(p, j[0] * i[0], j[1] * i[0]) == '●':
                        return -10
        return 0

    def __valid(self, p, row_inc, col_inc):
        if p[0] + row_inc < 0 or p[0] + row_inc > 5 \
                or p[1] + col_inc < 0 or p[1] + col_inc > 6:
            return ' '
        else:
            return self.sqs[p[0] + row_inc][p[1] + col_inc]

    def get_best_move(self):
        max_eval = -1000
        best_moves = []
        evals = {}
        for column in self.__get_valid_moves():
            last_move = self.place_piece(column, '○')
            curr_eval = self.__minimax(0, '●', last_move, -1000, 1000)
            self.remove_piece(column)
            evals[column + 1] = curr_eval
            if curr_eval > max_eval:
                best_moves.clear()
                best_moves.append(column)
                max_eval = curr_eval
            elif curr_eval == max_eval:
                best_moves.append(column)
        print(evals)
        return random.choice(best_moves)

    def __minimax(self, depth, turn, last_move, alpha, beta):
        valid_moves = self.__get_valid_moves()
        evaluation = self.check_win(last_move)
        if evaluation == 10:
            return evaluation - depth
        elif evaluation == -10:
            return evaluation + depth
        elif len(valid_moves) == 0 or depth == 8:
            return 0
        if turn == '○':
            max_eval = -1000
            for column in valid_moves:
                last_move = self.place_piece(column, '○')
                curr_eval = self.__minimax(depth + 1, '●', last_move, alpha, beta)
                self.remove_piece(column)
                max_eval = max(curr_eval, max_eval)
                alpha = max(alpha, curr_eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = 1000
            for column in valid_moves:
                last_move = self.place_piece(column, '●')
                curr_eval = self.__minimax(depth + 1, '○', last_move, alpha, beta)
                self.remove_piece(column)
                min_eval = min(curr_eval, min_eval)
                beta = min(beta, curr_eval)
                if beta <= alpha:
                    break
            return min_eval

    def __get_valid_moves(self):
        valid_moves = []
        for i in range(len(self.sqs[0])):
            if not self.is_full(i):
                valid_moves.append(i)
        return valid_moves
