width  = {0: "A", 1: "B", 2: "C", 3: "D", 4: "E", 5: "F"}
height = {0:   6, 1:   5, 2:   4, 3:   3, 4:   2, 5:   1}

#width  = {0: "A", 1: "B", 2: "C", 3: "D", 4: "E", 5: "F", 6: "G", 7: "H"}
#height = {0:   8, 1:   7, 2:   6, 3:   5, 4:   4, 5:   3, 6:   2, 7:   1}



class Checker:
    def __init__(self, w, h, color, board):
        self.x = w
        self.y = h

        self.color = color
        self.king = False

        self.board = board
        board.add(self)


    def move(self, w, h):
        self.board.delete(self)

        self.x = w
        self.y = h

        self.board.add(self)

        if (self.color == "white") and (self.y == 0):
            self.king = True
        if (self.color == "black") and (self.y == len(height) - 1):
            self.king = True


    def take(self, enemy, w, h):
        self.move(w, h)
        self.board.delete(enemy)


    def get_moves(self):
        moves = []
        directions = []

        if self.color == "white" or self.king:
            directions.append((-1, +1))
            directions.append((-1, -1))

        if self.color == "black" or self.king:
            directions.append((+1, +1))
            directions.append((+1, -1))

        for dy, dx in directions:
            length = 2

            if self.king:
                length = len(width) + 1

            for i in range(1, length):
                new_y = self.y + i * dy
                new_x = self.x + i * dx

                if not (0 <= new_x < len(width) and 0 <= new_y < len(height)):
                    break

                if self.board.cells[new_y][new_x] is None:
                    moves.append((new_x, new_y))
                else:
                    break

        return moves


    def get_captures(self):
        captures = []
        directions = [(-1, +1), (-1, -1), (+1, +1), (+1, -1)]

        for dy, dx in directions:
            length = 2

            if self.king:
                length = len(width) + 1

            for i in range(1, length):
                enemy_y = self.y + i * dy
                enemy_x = self.x + i * dx

                if not (0 <= enemy_x < len(width) and 0 <= enemy_y < len(height)):
                    break

                enemy = self.board.cells[enemy_y][enemy_x]

                if enemy is None:
                    continue

                if self.color == enemy.color:
                    break

                for j in range(i + 1, length + 1):
                    new_y = self.y + j * dy
                    new_x = self.x + j * dx

                    if not (0 <= new_x < len(width) and 0 <= new_y < len(height)):
                        break

                    if self.board.cells[new_y][new_x] is None:
                        captures.append(((enemy_x, enemy_y), (new_x, new_y)))
                    else:
                        break

                break

        return captures


    def get_full_captures(self, captures=None):
        if captures is None:
            captures = []

        current_captures = self.get_captures()

        if not current_captures:
            return [captures] if captures else []

        full_captures = []

        for (enemy_x, enemy_y), (new_x, new_y) in current_captures:
            new_board = self.board.__copy__()
            new_checker = new_board.find_checker(self.x, self.y)
            new_enemy = new_board.find_checker(enemy_x, enemy_y)

            new_checker.take(new_enemy, new_x, new_y)

            new_captures = captures + [((enemy_x, enemy_y), (new_x, new_y))]
            next_captures = new_checker.get_full_captures(new_captures)

            full_captures.extend(next_captures)

        return full_captures
