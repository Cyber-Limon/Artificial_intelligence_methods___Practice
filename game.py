from board import Board
from checker import Checker
from checker import width, height
from prettytable import PrettyTable



class Game:
    def __init__(self):
        self.board = Board()

        self.w1 = Checker(0, 5, "white", self.board)
        self.w2 = Checker(2, 5, "white", self.board)
        self.w3 = Checker(4, 5, "white", self.board)
        self.w4 = Checker(1, 4, "white", self.board)
        self.w5 = Checker(3, 4, "white", self.board)
        self.w6 = Checker(5, 4, "white", self.board)

        self.b1 = Checker(0, 1, "black", self.board)
        self.b2 = Checker(2, 1, "black", self.board)
        self.b3 = Checker(4, 1, "black", self.board)
        self.b4 = Checker(1, 0, "black", self.board)
        self.b5 = Checker(3, 0, "black", self.board)
        self.b6 = Checker(5, 0, "black", self.board)

        self.color = "white"

        print("Игра началась")
        self.board.print()


    def evaluation_function(self, board, color):
        white_checkers = 0
        white_kings = 0
        black_checkers = 0
        black_kings = 0

        for i in range(len(height)):
            for j in range(len(width)):
                checker = board.cells[i][j]

                if checker is None:
                    continue

                if checker.color == "white":
                    if checker.king:
                        white_kings += 1
                    else:
                        white_checkers += len(width) - i + 1
                else:
                    if checker.king:
                        black_kings += 1
                    else:
                        black_checkers += i + 1

        if color == "white":
            value = 5 * (white_checkers - black_checkers) + 10 * (white_kings - black_kings)
        else:
            value = 3 * (black_checkers - white_checkers) + 6 * (black_kings - white_kings)

        return value


    def take_or_move(self, board, checker, move, flag):
        if flag:
            return board.apply_take(checker, move)
        else:
            return board.apply_move(checker, move)


    def minimax(self, board, moves, flag, color):
        values = []

        for checker, move in moves:
            for subsequence in move:
                new_board = board.__copy__()
                new_checker = new_board.find_checker(checker.x, checker.y)

                self.take_or_move(new_board, new_checker, subsequence, flag)

                values.append(self.evaluation_function(new_board, color))

        return values


    def play(self):
        num_move = 1
        while True:
            value = None
            checker_need = None
            move_need = None

            enemy_moves = []
            enemy_values = []

            moves, flag = self.board.get_all_moves(self.color)

            if len(moves) == 0:
                if self.color == "white":
                    print("Победа черных")
                    return
                else:
                    print("Победа белых")
                    return

            for checker, move in moves:
                for subsequence in move:

                    new_board = self.board.__copy__()
                    new_checker = new_board.find_checker(checker.x, checker.y)

                    self.take_or_move(new_board, new_checker, subsequence, flag)

                    new_color = "black" if self.color == "white" else "white"
                    new_moves, new_flag = new_board.get_all_moves(new_color)

                    enemy_moves.append(new_moves)

                    values = self.minimax(new_board, new_moves, new_flag, self.color)
                    print(values)
                    enemy_values.append(values)

                    if len(values) == 0:
                        current_value = self.evaluation_function(new_board, self.color)
                    else:
                        current_value = min(values)

                    if value is None or value < current_value:
                        value = current_value
                        checker_need = checker
                        move_need = subsequence

                    print(value)

            table = self.table(moves, enemy_moves, enemy_values, value)
            self.take_or_move(self.board, checker_need, move_need, flag)

            print(f"Ход {num_move}: {self.color}")
            self.board.print()
            print(table, "\n")

            if self.color == "white":
                self.color = "black"
            else:
                self.color = "white"
                num_move += 1


    def table(self, moves, enemy_moves, enemy_values, value):
        table = PrettyTable()

        rows = []
        rows_normalized = []

        columns = []
        columns_normalized = []

        for move in moves:
            for i in move[1]:
                if ((move[0].x, move[0].y), i) not in rows:
                    rows.append(((move[0].x, move[0].y), i))

        for move in enemy_moves:
            for subsequence in move:
                for i in subsequence[1]:
                    if ((subsequence[0].x, subsequence[0].y), i) not in columns:
                        columns.append(((subsequence[0].x, subsequence[0].y), i))

        values = [["-" for _ in columns] for _ in rows]

        for move in enemy_moves:
            for subsequence in move:
                for i in subsequence[1]:
                    for j in range(len(columns)):
                        if columns[j] == ((subsequence[0].x, subsequence[0].y), i):
                            values[enemy_moves.index(move)][j] = enemy_values[enemy_moves.index(move)][move.index(subsequence)]

        for row in rows:
            start = str(width[row[0][0]]) + str(height[row[0][1]])

            if isinstance(row[1], tuple):
                end = str(width[row[1][0]]) + str(height[row[1][1]])
            else:
                end = str(width[row[1][-1][1][0]]) + str(height[row[1][-1][1][1]])

            rows_normalized.append(f"{start}->{end}")

        for column in columns:
            start = str(width[column[0][0]]) + str(height[column[0][1]])

            if isinstance(column[1], tuple):
                columns_normalized.append(start + "->" + str(width[column[1][0]]) + str(height[column[1][1]]))
            else:
                end = ""
                for i in range(len(column[1])):
                    end += ("x" + str(width[column[1][i][0][0]]) + str(height[column[1][i][0][1]]) +
                           "->" + str(width[column[1][i][1][0]]) + str(height[column[1][i][1][1]]))
                columns_normalized.append(f"{start}{end}")

        columns_normalized.insert(0, "")
        columns_normalized.extend(["Оценка", "Выбор"])

        flag = True

        for i in range(len(values)):
            m = None

            for j in values[i]:
                if isinstance(j, int):
                    if m is None or m > j:
                        m = j

            if m is None:
                values[i].append(value)
            else:
                values[i].append(m)

            values[i].insert(0, rows_normalized[i])

            if flag and (m == value or m is None):
                flag = False
                values[i].append("x")
            else:
                values[i].append("")

            table.add_row(values[i])

        table.field_names = columns_normalized

        return table
