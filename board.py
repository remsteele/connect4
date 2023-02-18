import collections
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

    # def __column_to_point(self, column):
    #     for i in range(len(self.sqs)):
    #         if self.sqs[len(self.sqs) - i - 1][column] == ' ':
    #             return len(self.sqs) - i - 1, column
    #     print('FULL COLUMN ERROR')
    #     return None

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
            return '-'
        else:
            return self.sqs[p[0] + row_inc][p[1] + col_inc]

    def get_best_move(self):
        max_eval = -1000
        best_moves = []
        # key: column
        # item: evaluation
        evals = {}
        for column in self.__get_valid_moves():
            last_move = self.place_piece(column, '○')
            curr_eval = self.__minimax(0, '●', last_move, -1000, 1000)
            self.remove_piece(column)
            evals[column] = curr_eval
            if curr_eval > max_eval:
                best_moves.clear()
                best_moves.append(column)
                max_eval = curr_eval
            elif curr_eval == max_eval:
                best_moves.append(column)
        print(f'Move evals: {evals}')
        if max([v for k, v in evals.items()]) == 0:
            moves = [k for k, v in evals.items() if v == 0]
            if len(moves) == 1:
                return moves[0]
            else:
                print(f'Drawing moves: {moves}')
                return self.__get_best_drawing_move(moves)
        else:
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

    def __get_best_drawing_move(self, best_moves):
        print('Choosing drawing move...')
        # check for three in a row
        for best_move in best_moves:
            point = self.place_piece(best_move, '○')
            if self.__point_contains(point, ['○', '○', '○', ' ']):
                self.remove_piece(best_move)
                print('Make 3 in a row')
                return best_move
            self.remove_piece(best_move)
        # check for opponent three in a row
        for best_move in best_moves:
            point = self.place_piece(best_move, '●')
            if self.__point_contains(point, ['●', '●', '●', ' ']):
                self.remove_piece(best_move)
                print('Block opponent 3 in a row')
                return best_move
            self.remove_piece(best_move)
        # check for two in a row
        for best_move in best_moves:
            for best_move in best_moves:
                point = self.place_piece(best_move, '○')
                if self.__point_contains(point, ['○', '○', ' ', ' ']):
                    self.remove_piece(best_move)
                    print('Make 2 in a row')
                    return best_move
                self.remove_piece(best_move)
        print('Random')
        # play random move
        return random.choice(best_moves)

    def __point_contains(self, point, args):
        for i in [[0, 1, 2, 3], [-1, 0, 1, 2], [-2, -1, 0, 1], [-3, -2, -1, 0]]:
            for j in [[0, 1], [1, 0], [1, 1], [-1, 1]]:
                values = []
                for inc in range(4):
                    values.append(self.__valid(point, j[0] * i[inc], j[1] * i[inc]))
                if collections.Counter(values) == collections.Counter(args):
                    return True
        return False

    def __get_valid_moves(self):
        valid_moves = []
        for i in range(len(self.sqs[0])):
            if not self.is_full(i):
                valid_moves.append(i)
        return valid_moves
