class Piece:
    def __init__(self, color, posx, posy):
        self.color = color
        self.posx = posx
        self.posy = posy

@staticmethod
def inbound(location):
    if 0 <= location[1] <= 7 and 0 <= location[0] <= 7:
        return True
    return False

def ischeck(self, board, enemies):
    if any (enemy.seesking(board) for enemy in enemies):
        return True
    return False

def movesondiag(self, board, dx, dy):
    ans = []
    y = self.posy + dy
    x = self.posx + dx
    while self.inbound((y, x)) and board[y][x] == 0:
        ans.append((y,x))
        y += dy
        x += dx
    if self.inbound((y, x)) and board[y][x] != 0 and board[y][x].color != self.color:
        ans.append((y, x))
        return ans

def horizontalnmoves(self, board, dx):
    ans = []
    x = self.posx + dx
    y = self.posy
    while self.inbound((y, x)) and board[y][x] == 0:
        ans.append((y,x))
        x += dx
    if self.inbound((y, x)) and board[y][x] != 0 and board[y][x].color != self.color:
        ans.append((y, x))
        return ans

def verticalmoves(self, board, dy):
    ans = []
    x = self.posx
    y = self.posy + dy
    while self.inbound((y, x)) and board[y][x] == 0:
        ans.append((y,x))
        y += dy
    if self.inbound((y, x)) and board[y][x] != 0 and board[y][x].color != self.color:
        ans.append((y, x))
        return ans


class N:
    color = 2

class King(Piece):
    def __init__(self, color, posx, posy):
        super().__init__(color, posx, posy)

    def checkmoves(self, board, enemies):
        ans = []
        for dx in range (-1, 2):
            for dy in range(-1, 2):
                location = (self.posy+dy, self.posx+dx)
            if not self.inbound(location):
                continue
        square = board[self.posy+dy][self.posx+dx]

        if square == 0 or square.color == (not self.color):
            if any(enemy.seespos(location, board) for enemy in enemies):
                continue
            else:
                ans.append((self.posy+dy, self.posx+dx))

        return ans


class Pawn(Piece):
def __init__(self, color, posx, posy):
super().__init__(color, posx, posy)
self.first_move = True
self.double_moved = False

def move(self):
self.first_move = False

def checkmoves(self, board, enemies):
ans = []
if self.color == 0:
location = (self.posy-1, self.posx) # move forward
square = board[location[0]][location[1]]
if self.inbound(location):
if square == 0:
ans.append(location)
location = (self.posy-1, self.posx+1) # en passant right
square = board[location[0]][location[1]]
if self.inbound(location):
if type(square) == Pawn and square.double_moved and square.color == 1:
ans.append(location)
location = (self.posy-1, self.posx-1) # en passant left
square = board[location[0]][location[1]]
if self.inbound(location):
if type(square) == Pawn and square.double_moved and square.color == 1:
ans.append(location)
location = (self.posy-1, self.posx-1) # capture left
square = board[location[0]][location[1]]
if self.inbound(location):
if type(square) == Pawn and square.color == 1:
ans.append(location)
location = (self.posy-1, self.posx+1) # capture right
square = board[location[0]][location[1]]
if self.inbound(location):
if type(square) == Pawn and square.color == 1:
ans.append(location)
location = (self.posy-2, self.posx) # double move
square = board[location[0]][location[1]]
if self.inbound(location):
if self.first_move and square == 0:
ans.append(location)
if self.color == 1:
location = (self.posy-1, self.posx) # move forward
square = board[location[0]][location[1]]
if self.inbound(location):
if square == 0:
ans.append(location)
location = (self.posy-1, self.posx+1) # en passant right
square = board[location[0]][location[1]]
if self.inbound(location):
if type(square) == Pawn and square.double_moved and square.color == 1:
ans.append(location)
location = (self.posy-1, self.posx-1) # en passant left
square = board[location[0]][location[1]]
if self.inbound(location):
if type(square) == Pawn and square.double_moved and square.color == 1:
ans.append((self.posy-1, self.posx-1))
location = (self.posy-1, self.posx-1) # capture left
square = board[location[0]][location[1]]
if self.inbound(location):
if type(square) == Pawn
and square.color == 1:
ans.append(location)
location = (self.posy-1, self.posx+1) # capture right
square = board[location[0]][location[1]]
if self.inbound(location):
if type(square) == Pawn and square.color == 1:
ans.append(location)
location = (self.posy-2, self.posx) # double move
square = board[location[0]][location[1]]
if self.inbound(location):
if self.first_move and square == 0:
ans.append(location)
for location in ans:
newboard = board.copy()
newboard[location[0]][location[1]] = newboard[self.posy][self.posx]
newboard[self.posy][self.posx] = 0
if self.ischeck(newboard, enemies):
ans.remove(location)
return ans

def seesking(self, board):
if self.color == 0: # white
square = board[self.posy-1][self.posx-1] # check to the left
if type(square) == King and square.color == (not self.color):
return True
square = board[self.posy-1][self.posx+1] # check to the right
if type(square) == King and square.color == (not self.color):
return True
else: # black
square = board[self.posy+1][self.posx-1]
if type(square) == King and square.color == (not self.color):
return True
square = board[self.posy+1][self.posx-1]
if type(square) == King and square.color == (not self.color):
return True

def seespos(self, pos, board):
if self.color == 0:
if pos in [(self.posy-1, self.posx-1), (self.posy-1, self.posx+1)]:
return True
if self.color == 1:
if pos in [(self.posy+1, self.posx-1), (self.posy+1, self.posx+1)]:
return True
return False


class Bishop(Piece):
def __init__(self, color, posx, posy):
super().__init__(color, posx, posy)

def checkmoves(self, board, enemies):
ans = []
for dx in range(-1, 2):
dy = dx
ans += self.movesondiag(board, dy, dx)
dy = -dx
ans += self.movesondiag(board, dy, dx)
for location in ans:
newboard = board.copy()
newboard[location[0]][location[1]] = newboard[self.posy][self.posx]
newboard[self.posy][self.posx] = 0
if self.ischeck(newboard, enemies):
ans.remove(location)
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
if type(board[location[0]][location[1]]) == King and board[location[0]][location[1]].color == (not self.color):
return True
return False


class Rook(Piece):
def __init__(self, color, posx, posy):
super().__init__(color, posx, posy)
self.first_move = True


class Queen(Piece):
def __init__(self, color, posx, posy):
super().__init__(color, posx, posy)


class Knight(Piece):
def __init__(self, color, posx, posy):
super().__init__(color, posx, posy)


board = []
for i in range(8):
k = King(1, 0, 0)
b1 = Bishop(1, 1, 1)
b2 = Bishop(0, 2, 2)
if i == 0:
board.append([k, 0, 0, 0, 0, 0, 0, 0])
elif i == 1:
board.append([0, b1, 0, 0, 0, 0, 0, 0])
elif i == 2:
board.append([0, 0, b2, 0, 0, 0, 0, 0])
else:
board.append([0, 0, 0, 0, 0, 0, 0, 0])
print(b1.checkmoves(board, [b2]))