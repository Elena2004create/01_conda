from pieces import *
import pygame


class Game:
    def get_promotion(self):
        t = input("Write promoted piece (B = Bishop, Q = Queen, K = Knight, R = Rook): ")
        a = "qbkrQBKR"
        while t not in a:
            t = input("Write promoted piece (B = Bishop, Q = Queen, K = Knight, R = Rook): ")
        return t.lower()

    def move(self, board, piece, location, whites, blacks):
        target = board[location[0]][location[1]]
        if piece.color == 0:
            if target.color == 1:
                del (blacks[blacks.index(target)])
            if location[0] < 7:
                en_passant = board[location[0] + 1][location[1]]
                if type(en_passant) == Pawn and en_passant.color == 1 and en_passant.double_moved and en_passant.posy == piece.posy and type(
                        piece) == Pawn:
                    del (blacks[blacks.index(en_passant)])
        else:
            if target.color == 0:
                del (whites[whites.index(target)])
            if location[0] > 0:
                en_passant = board[location[0] - 1][location[1]]
                if type(en_passant) == Pawn and en_passant.color == 0 and en_passant.double_moved and en_passant.posy == piece.posy and type(
                        piece) == Pawn:
                    del (whites[whites.index(en_passant)])
        board[location[0]][location[1]] = piece

        board[piece.posy][piece.posx] = N()
        piece.posy, piece.posx = location[0], location[1]

    def startgame(self):
        pygame.init()
        pygame.font.init()
        WIDTH = 800
        HEIGHT = 800
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Chess")
        clock = pygame.time.Clock()
        board_s = pygame.image.load("111.jpg").convert()
        board_s = pygame.transform.scale(board_s, (800, 800))
        board_rect = board_s.get_rect()
        circle = pygame.image.load("3.png").convert()
        circle = pygame.transform.scale(circle, (50, 50))
        screen.blit(board_s, board_rect)
        running = True
        board, blacks, whites = self.setboard()
        f1 = pygame.font.Font("2.ttf", 50)
        pygame.display.update()
        MOVE = 0
        SELECTED = N()
        availible = ()
        while running:
            MOVED = False
            screen.blit(board_s, board_rect)
            for piece in blacks + whites:
                if piece.color == 0:
                    c = (255, 0, 0)
                else:
                    c = (66, 66, 66)
                board[piece.posy][piece.posx] = piece
                text1 = f1.render(piece.sym, True, c)
                text_rect = text1.get_rect(center=(piece.posx * 100 + 50, piece.posy * 100 + 50))
                screen.blit(text1, text_rect)
            if availible and SELECTED.color == MOVE:
                for y, x in availible:
                    circle_r = circle.get_rect(center=(x * 100 + 50, y * 100 + 50))
                    screen.blit(circle, circle_r)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if type(SELECTED) != N and SELECTED.color == MOVE:
                        pos = event.pos
                        posy = pos[1]
                        posx = pos[0]
                        location = (posy // 100, posx // 100)
                        if SELECTED.color == 1:
                            enemies = whites
                        else:
                            enemies = blacks
                        availible = SELECTED.checkmoves(board, enemies)
                        MOVED = True
                        if not availible:
                            print("No fuck no deselect!")
                            continue
                        elif location in availible:
                            dif = abs(location[0] - SELECTED.posy)
                            self.move(board, SELECTED, location, whites, blacks)
                            MOVE = not MOVE
                            if type(SELECTED) == Pawn:
                                SELECTED.first_move = False
                                l = {"q": Queen, "b": Bishop, "r": Rook, "k": Knight}
                                if SELECTED.color == 1 and SELECTED.posy == 7:
                                    t = self.get_promotion(l[t])
                                    q = SELECTED.promote(l[t])
                                    blacks[blacks.index(SELECTED)] = q
                                if SELECTED.color == 0 and SELECTED.posy == 0:
                                    t = self.get_promotion()
                                    q = SELECTED.promote(l[t])
                                    whites[whites.index(SELECTED)] = q
                                if dif == 2:
                                    SELECTED.double_moved = True
                            if MOVE == 0:
                                for i in whites:
                                    if type(i) == Pawn:
                                        i.double_moved = False
                            else:
                                for i in blacks:
                                    if type(i) == Pawn:
                                        i.double_moved = False
                        else:
                            print("No fuck no deselect")
                            continue
                    else:
                        pos = event.pos
                        posy = pos[1]
                        posx = pos[0]
                        piece = board[posy // 100][posx // 100]
                        if piece.color == MOVE:
                            print(piece, posy, posx)
                            print(posy // 100, posx // 100)
                        SELECTED = piece
                        if SELECTED.color == 1:
                            enemies = whites
                        else:
                            enemies = blacks
                        availible = SELECTED.checkmoves(board, enemies)
                if event.type == pygame.QUIT:
                    running = False
            if MOVED:
                MOVED = False
                board = [[N() for i in range(8)] for j in range(8)]
                SELECTED = N()
                availible = ()
            pygame.display.update()
            clock.tick(60)

    def createpieces(self, color):
        if color == 1:
            firstrow = 0
            secondrow = 1
        else:
            firstrow = 7
            secondrow = 6

        LR = Rook(color, 0, firstrow)  # Left black rook
        LK = Knight(color, 1, firstrow)
        LB = Bishop(color, 2, firstrow)
        Q = Queen(color, 3, firstrow)
        Kin = King(color, 4, firstrow)
        RB = Bishop(color, 5, firstrow)
        RK = Knight(color, 6, firstrow)
        RR = Rook(color, 7, firstrow)
        Pawns = []
        for i in range(8):
            Pawns.append(Pawn(color, i, secondrow))

        Allpieces = [LR, LK, LB, Q, Kin, RB, RK, RR]
        Allpieces += Pawns
        return Allpieces

    def setboard(self):
        board = [[N() for i in range(8)] for j in range(8)]
        blacks = self.createpieces(1)
        whites = self.createpieces(0)
        allpieces = blacks + whites

        for piece in allpieces:
            board[piece.posy][piece.posx] = piece

        return board, blacks, whites


g = Game()
g.startgame()