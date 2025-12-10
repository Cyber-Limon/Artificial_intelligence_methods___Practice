from checker import Checker
from checker import width, height



class Board:
    def __init__(self):
        self.cells = [[None for _ in range(len(width))] for _ in range(len(height))]
        self.output = [["O" for _ in range(len(width))] for _ in range(len(height))]


    def __copy__(self):
        new_board = Board()

        for i in range(len(height)):
            for j in range(len(width)):
                checker = self.cells[i][j]

                if checker is not None:
                    new_checker = Checker(checker.x, checker.y, checker.color, new_board)
                    new_checker.king = checker.king

        return new_board


    def find_checker(self, x, y):
        return self.cells[y][x]


    def print(self):
        for i in self.output:
            print(i)
        print("")


    def add(self, checker):
        self.cells[checker.y][checker.x] = checker

        if checker.color == "white":
            self.output[checker.y][checker.x] = "W"
        else:
            self.output[checker.y][checker.x] = "B"


    def delete(self, checker):
        self.cells[checker.y][checker.x] = None
        self.output[checker.y][checker.x] = "O"


    def apply_take(self, checker, move):
        for (enemy_x, enemy_y), (new_x, new_y) in move:
            enemy = self.find_checker(enemy_x, enemy_y)
            checker.take(enemy, new_x, new_y)


    def apply_move(self, checker, move):
            checker.move(*move)


    def get_all_moves(self, color):
        checkers = []
        captures = []
        moves = []

        for i in range(len(height)):
            for j in range(len(width)):
                checker = self.cells[i][j]

                if checker is not None and checker.color == color:
                    checkers.append(checker)

        for checker in checkers:
            take = checker.get_full_captures()
            move = checker.get_moves()

            if take:
                captures.append((checker, take))

            if move:
                moves.append((checker, move))

        if captures:
            return captures, True
        else:
            return moves, False
