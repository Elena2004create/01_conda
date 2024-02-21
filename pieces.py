class Piece:
    def __init__(self, color, posx, posy, first_move=True, double_moved=False):
        self.color = color
        self.posx = posx
        self.posy = posy
        self.first_move = first_move
        self.double_moved = double_moved

    def islegal(self, board, enemies, ans):
        ans2 = ans.copy()
        for location in ans:
            newboard = self.clone(board)
            newboard[location[0]][location[1]] = newboard[self.posy][self.posx]
            newboard[self.posy][self.posx] = N()
            nenemies = []
            for i in range(8):
                for j in range(8):
                    if newboard[i][j].color == abs(self.color - 1):
                        square = newboard[i][j]
                        nenemies.append(type(square)(square.color, square.posx, square.posy))
            if self.ischeck(newboard, nenemies):
                ans2.remove(location)

        return ans2

    @staticmethod
    def inbound(location):
        if 0 <= location[1] <= 7 and 0 <= location[0] <= 7:
            return True
        return False

    def cloneenemies(self, enemies):
        ans = []
        for enemie in enemies:
            ans.append(type(enemie)(enemie.color, enemie.posx, enemie.posy))
        return ans

    def clone(self, board):
        newboard = [[0 for i in range(8)] for j in range(8)]
        for i in range(8):
            for j in range(8):
                square = board[i][j]
                newboard[i][j] = type(square)(square.color, square.posx, square.posy)
        return newboard

    def ischeck(self, board, enemies):
        for enemy in enemies:
            if enemy.seesking(board):
                print(enemy, enemy.posx, enemy.posy)
                return True
        return False

    def movesondiag(self, board, dx, dy):
        ans = []
        y = self.posy + dy
        x = self.posx + dx
        while self.inbound((y, x)) and board[y][x].color == 2:
            ans.append((y, x))
            y += dy
            x += dx
        if self.inbound((y, x)) and board[y][x].color != self.color:
            ans.append((y, x))
        return ans

    def horizontalnmoves(self, board, dx):
        ans = []
        x = self.posx + dx
        y = self.posy
        while self.inbound((y, x)) and board[y][x].color == 2:
            ans.append((y, x))
            x += dx
        if self.inbound((y, x)) and board[y][x].color != self.color:
            ans.append((y, x))
        return ans

    def verticalmoves(self, board, dy):
        ans = []
        x = self.posx
        y = self.posy + dy
        while self.inbound((y, x)) and board[y][x].color == 2:
            ans.append((y, x))
            y += dy
        if self.inbound((y, x)) and board[y][x].color != self.color:
            ans.append((y, x))
        return ans

    def knightmoves(self, board):
        x = self.posx
        y = self.posy
        ans = []
        moves = [(1, 2), (2, 1), (-1, 2), (-2, 1), (1, -2), (2, -1), (-1, -2), (-2, -1)]
        for dx, dy in moves:
            location = (y + dy, x + dx)
            if self.inbound(location):
                square = board[location[0]][location[1]]
                if square.color != self.color:
                    ans.append(location)

        return ans

    def __repr__(self):
        return self.sym


class N(Piece):
    color = 2

    def __init__(self, color=2, posx=-1, posy=-1):
        super().__init__(color, posx, posy)

    def __repr__(self):
        return "\u03C9"

    def checkmoves(self, board, enemies):
        pass


class King(Piece):
    def __init__(self, color, posx, posy):
        super().__init__(color, posx, posy)
        if color == 1:
            self.sym = "\u265A"
        else:
            self.sym = "\u2654"

    def checkmoves(self, board, enemies):
        ans = []
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                location = (self.posy + dy, self.posx + dx)
                if not self.inbound(location):
                    continue
                square = board[self.posy + dy][self.posx + dx]
                if square.color != self.color:
                    ans.append(location)
        ans = self.islegal(board, enemies, ans)
        return ans

    def seesking(self, board):
        for location in self.allmoves(board):
            if type(board[location[0]][location[1]]) == King and board[location[0]][location[1]].color == (
            not self.color):
                return True
        return False

    def allmoves(self, board):
        ans = []
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                location = (self.posy + dy, self.posx + dx)
                if not self.inbound(location):
                    continue
                square = board[self.posy + dy][self.posx + dx]
                if square.color != self.color:
                    ans.append(location)
        return ans

    def seespos(self, pos, board):
        if pos in self.allmoves(board):
            return True
        return False


class Pawn(Piece):
    def __init__(self, color, posx, posy):
        super().__init__(color, posx, posy)
        self.first_move = True
        self.double_moved = False
        if color == 1:
            self.sym = "\u265F"
        else:
            self.sym = "\u2659"

    def promote(self, to):
        return to(self.color, self.posx, self.posy)

    def move(self):
        self.first_move = False

    def checkmoves(self, board, enemies):
        ans = []
        if self.color == 0:
            location = (self.posy - 1, self.posx)  # move forward
            if self.inbound(location):
                square = board[location[0]][location[1]]
                if square.color == 2:
                    ans.append(location)

            location = (self.posy - 1, self.posx + 1)  # en passant right
            if self.inbound(location):
                square = board[location[0]][location[1]]
                square2 = board[self.posy][self.posx + 1]
                if type(square2) == Pawn and square2.double_moved and square2.color == 1:
                    ans.append(location)

            location = (self.posy - 1, self.posx - 1)  # en passant left
            if self.inbound(location):
                square = board[location[0]][location[1]]
                square2 = board[self.posy][self.posx - 1]
                if type(square2) == Pawn and square2.double_moved and square2.color == 1:
                    ans.append(location)

            location = (self.posy - 1, self.posx - 1)  # capture left
            if self.inbound(location):
                square = board[location[0]][location[1]]
                if square.color == 1:
                    ans.append(location)

            location = (self.posy - 1, self.posx + 1)  # capture right
            if self.inbound(location):
                square = board[location[0]][location[1]]
                if square.color == 1:
                    ans.append(location)

            location = (self.posy - 2, self.posx)  # double move
            if self.inbound(location):
                square = board[location[0]][location[1]]
                if self.first_move and square.color == 2:
                    ans.append(location)
        if self.color == 1:
            location = (self.posy + 1, self.posx)  # move forward
            if self.inbound(location):
                square = board[location[0]][location[1]]
                if square.color == 2:
                    ans.append(location)
            location = (self.posy + 1, self.posx + 1)  # en passant right
            if self.inbound(location):
                square = board[location[0]][location[1]]
                square2 = board[self.posy][self.posx + 1]
                if type(square2) == Pawn and square2.double_moved and square2.color == 0:
                    ans.append(location)
            location = (self.posy + 1, self.posx - 1)  # en passant left
            if self.inbound(location):
                square = board[location[0]][location[1]]
                square2 = board[self.posy][self.posx - 1]
                if type(square2) == Pawn and square2.double_moved and square2.color == 0:
                    ans.append(location)

            location = (self.posy + 1, self.posx - 1)  # capture left
            if self.inbound(location):
                square = board[location[0]][location[1]]
                if square.color == 0:
                    ans.append(location)
            location = (self.posy + 1, self.posx + 1)  # capture right
            if self.inbound(location):
                square = board[location[0]][location[1]]
                if square.color == 0:
                    ans.append(location)
            location = (self.posy + 2, self.posx)  # double move
            if self.inbound(location):
                square = board[location[0]][location[1]]
                if self.first_move and square.color == 2:
                    ans.append(location)
        ans = self.islegal(board, enemies, ans)

        return ans

    def seesking(self, board):
        if self.color == 0:  # white
            if self.inbound((self.posy - 1, self.posx - 1)):
                square = board[self.posy - 1][self.posx - 1]  # check to the left
                if type(square) == King and square.color == 1:
                    return True
            if self.inbound((self.posy - 1, self.posx + 1)):
                square = board[self.posy - 1][self.posx + 1]  # check to the right
                if type(square) == King and square.color == 1:
                    return True
        else:  # black
            if self.inbound((self.posy + 1, self.posx - 1)):
                square = board[self.posy + 1][self.posx - 1]
                if type(square) == King and square.color == 0:
                    return True
            if self.inbound((self.posy + 1, self.posx + 1)):
                square = board[self.posy + 1][self.posx + 1]
                if type(square) == King and square.color == 0:
                    return True

    def seespos(self, pos, board):
        if self.color == 0:
            if pos in [(self.posy - 1, self.posx - 1), (self.posy - 1, self.posx + 1)]:
                return True
        if self.color == 1:
            if pos in [(self.posy + 1, self.posx - 1), (self.posy + 1, self.posx + 1)]:
                return True
        return False


class Bishop(Piece):
    sym = "\u265D"

    def __init__(self, color, posx, posy):
        super().__init__(color, posx, posy)
        if color == 1:
            self.sym = "\u265D"
        else:
            self.sym = "\u2657"

    def checkmoves(self, board, enemies):
        ans = []
        for dx in range(-1, 2):
            dy = dx
            ans += self.movesondiag(board, dy, dx)
            dy = -dx
            ans += self.movesondiag(board, dy, dx)
        ans = self.islegal(board, enemies, ans)

        return ans

    def allmoves(self, board):
        ans = []
        for dx in range(-1, 2):
            dy = dx
            ans += self.movesondiag(board, dy, dx)
            dy = -dx
            ans += self.movesondiag(board, dy, dx)
        return ans

    def seespos(self, pos, board):
        if pos in self.allmoves(board):
            return True
        return False

    def seesking(self, board):
        for location in self.allmoves(board):
            if type(board[location[0]][location[1]]) == King and board[location[0]][location[1]].color == (
            not self.color):
                return True
        return False


class Rook(Piece):

    def __init__(self, color, posx, posy):
        super().__init__(color, posx, posy)
        self.first_move = True
        if color == 1:
            self.sym = "\u265C"
        else:
            self.sym = "\u2656"

    def checkmoves(self, board, enemies):
        ans = []
        for dx in range(-1, 2):
            ans += self.horizontalnmoves(board, dx)
        for dy in range(-1, 2):
            ans += self.verticalmoves(board, dy)

        ans = self.islegal(board, enemies, ans)

        return ans

    def allmoves(self, board):
        ans = []
        for dx in range(-1, 2):
            ans += self.horizontalnmoves(board, dx)
        for dy in range(-1, 2):
            ans += self.verticalmoves(board, dy)
        return ans

    def seesking(self, board):
        for location in self.allmoves(board):
            if type(board[location[0]][location[1]]) == King and board[location[0]][location[1]].color == (
            not self.color):
                return True
        return False

    def seespos(self, pos, board):
        if pos in self.allmoves(board):
            return True
        return False


class Queen(Piece):
    def __init__(self, color, posx, posy):
        super().__init__(color, posx, posy)
        if color == 1:
            self.sym = "\u265B"
        else:
            self.sym = "\u2655"

    def checkmoves(self, board, enemies):
        ans = []
        for dx in range(-1, 2):
            ans += self.horizontalnmoves(board, dx)
        for dy in range(-1, 2):
            ans += self.verticalmoves(board, dy)
        for dx in range(-1, 2):
            dy = dx
            ans += self.movesondiag(board, dy, dx)
            dy = -dx
            ans += self.movesondiag(board, dy, dx)
        ans = self.islegal(board, enemies, ans)

        return ans

    def allmoves(self, board):
        ans = []
        for dx in range(-1, 2):
            ans += self.horizontalnmoves(board, dx)
        for dy in range(-1, 2):
            ans += self.verticalmoves(board, dy)
        for dx in range(-1, 2):
            dy = dx
            ans += self.movesondiag(board, dy, dx)
            dy = -dx
            ans += self.movesondiag(board, dy, dx)
        return ans

    def seesking(self, board):
        for location in self.allmoves(board):
            if type(board[location[0]][location[1]]) == King and board[location[0]][location[1]].color == (
            not self.color):
                return True
        return False

    def seespos(self, pos, board):
        if pos in self.allmoves(board):
            return True
        return False


class Knight(Piece):
    def __init__(self, color, posx, posy):
        super().__init__(color, posx, posy)
        if color == 1:
            self.sym = "\u265E"
        else:
            self.sym = "\u2658"

    def checkmoves(self, board, enemies):
        ans = self.knightmoves(board)
        ans = self.islegal(board, enemies, ans)

        return ans

    def allmoves(self, board):
        return self.knightmoves(board)

    def seesking(self, board):
        for location in self.allmoves(board):
            if type(board[location[0]][location[1]]) == King and board[location[0]][location[1]].color == (
            not self.color):
                return True
        return False

    def seespos(self, pos, board):
        if pos in self.allmoves(board):
            return True
        return False
