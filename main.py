import pygame

rows = ["-B", "-A"] + ["A", "B", "C", "D", "E", "F", "G", "H"] + ["-H", "-G"]
cols = ["10", "9"] + [str(x + 1) for x in range(8)][::-1] + ["-1", "-2"]
width = 1280
height = 800
starts = "black"
white_colour = (170, 110, 150)
black_colour = (30, 30, 30)
background_colour = (118, 150, 86)
pieces = {}
queening = False
playing_field = None
xoffset, yoffset = None, None
x_square_size, y_square_size = None, None
moves = []


class Tile:
    def __init__(self, location, ttype="normal", passable=True):
        self.type = ttype
        self.passable = passable
        self.piece = None
        self.name = rows[location[0]] + cols[location[1]]
        self.location = location
        self.colour = "white" if ((location[0] + location[1]) % 2 == 1) else "black"


class Piece:
    def __init__(self, colour, ptype, direction):
        self.colour = colour
        self.type = ptype
        self.movement_direction = direction
        self.has_not_moved = True
        self.name = ("white " if colour == "w" else "black ") + self.type


def get_pieces():
    for sets in ["b", "w"]:
        pieces[sets] = {}
        for piece in ["pawn", "knight", "bishop", "rook", "queen", "king"]:
            img = pygame.image.load(f"./JohnPablok Cburnett Chess set/PNGs/No shadow/1x/{sets}_{piece}_1x_ns.png")
            img = pygame.transform.scale(img, (x_square_size * 0.8, y_square_size * 0.8))
            pieces[sets][piece] = img
        name = "sPawn"
        img = pygame.image.load(f"./JohnPablok Cburnett Chess set/PNGs/No shadow/1x/{sets}_pawn_1x_ns.png")
        img = pygame.transform.rotate(img, 180.)
        img = pygame.transform.scale(img, (x_square_size * 0.8, y_square_size * 0.8))
        pieces[sets][name] = img
    return pieces


def draw_letters(font):
    for i, r in enumerate(rows[2:-2]):
        text = font.render(r, True, (205, 205, 160, 50))
        textRect = text.get_rect()
        textRect.center = (xoffset + (i + 2 + 0.2) * x_square_size, (11 - 0.75) * y_square_size)
        screen.blit(text, textRect)
    for i, c in enumerate(cols[2:-2]):
        text = font.render(c, True, (205, 205, 160, 50))
        textRect = text.get_rect()
        textRect.center = (xoffset + (2 - 0.2) * x_square_size, (i + 3 - 0.75) * y_square_size)
        screen.blit(text, textRect)


def draw_piece(row, col):
    p = playing_field[row][col].piece
    colour, piece = p.colour, p.type
    # print(colour, piece, )
    img = pieces[colour][piece]
    rect = img.get_rect()
    rect.center = (xoffset + (row + 0.5) * x_square_size, yoffset + (col + 0.5) * y_square_size)
    screen.blit(img, rect)


def draw_dot(row, col):
    # print(colour, piece, )
    c = (100, 100, 100)
    pygame.draw.circle(screen, c, (xoffset + (row + 0.5) * x_square_size, yoffset + (col + 0.5) * y_square_size), 20)

    # pygame.display.update()


def move_piece(tox, toy, selected, ):
    selected.piece.has_not_moved = False

    playing_field[tox][toy].piece = selected.piece
    playing_field[selected.location[0]][selected.location[1]].piece = None
    draw_tile(selected.location[0], selected.location[1])
    draw_tile(tox, toy)
    # draw_tile(tox, toy)


def draw_tile(row, col):
    color = background_colour if not playing_field[row][
        col].passable else (white_colour if (row + col) % 2 == 0 else black_colour)
    pygame.draw.rect(screen, color,
                     (row * x_square_size + xoffset, col * y_square_size, x_square_size, y_square_size))
    if playing_field[row][col].piece is not None:
        draw_piece(row, col)
    ...


def can_move_here(origin, target, commit_move=True):  # TODO
    if target.piece is not None and target.piece.colour == origin.piece.colour and (
            origin.piece.type not in ["king", "bishop"]):
        return False, ""
    if not target.passable and origin.piece.type != "knight":
        return False, ""
    piece = origin.piece
    ptype = piece.type
    x, y = origin.location
    # print(x, y, target.location)
    if ptype == "pawn" or ptype == "sPawn":
        # TODO en passant is forced
        # TODO en passant actual condition kekw
        # TODO return also move name, if applicable (omega passant...)
        same_row = (moves[-1][2] == y) if moves else False
        if (((x, y + piece.movement_direction) == target.location) or
            ((x, y + (piece.movement_direction * 2)) == target.location and piece.has_not_moved)) \
                and target.piece is None:
            return True, "moveup"
        if (((x + 1, y + piece.movement_direction) == target.location) or
                ((x - 1, y + piece.movement_direction) == target.location)):
            if target.piece is not None:
                return True, "capture"
            elif same_row and moves and (piece.movement_direction * (y - 2) % 8 + (piece.movement_direction > 0)) == 5:
                if moves[-1][1] == x - 1:
                    if commit_move:
                        playing_field[x - 1][y].piece = None
                        draw_tile(x - 1, y)
                    return True, "enpassant"
                if moves[-1][1] == x + 1:
                    if commit_move:
                        playing_field[x + 1][y].piece = None
                        draw_tile(x + 1, y)
                    return True, "enpassant"
        if same_row and (piece.movement_direction * (y - 2) % 8 + (piece.movement_direction > 0)) == 5 and (
                (((x + 2, y + piece.movement_direction * 2) == target.location) and (moves[-1][1] > x)) or
                (((x - 2, y + piece.movement_direction * 2) == target.location) and (moves[-1][1] < x))) and (
                target.piece is None) and not collision(origin, target, ) and \
                not collision(origin, playing_field[moves[-1][-1]][3]):
            if commit_move:
                playing_field[moves[-1][1]][moves[-1][2]].piece = None
                draw_tile(moves[-1][1], moves[-1][2])
            return True, "omegapassant"
        if (y + piece.movement_direction < 0) or (y + piece.movement_direction > 11) or not playing_field[x][
            y + piece.movement_direction].passable:
            newname = "sPawn" if ptype == "pawn" else "pawn"
            for yoff in range(1, 12):
                if 0 <= (y - piece.movement_direction * yoff) <= 11:
                    if playing_field[x][y - piece.movement_direction * yoff].piece is None:
                        if target.location == (x, y - piece.movement_direction * yoff):
                            if commit_move:
                                playing_field[x][y - piece.movement_direction * yoff].piece = Piece(ptype=newname,
                                                                                                    direction=piece.movement_direction * -1,
                                                                                                    colour=piece.colour)
                                draw_tile(x, y - 1 - piece.movement_direction * yoff)
                            return True, "sPawn"
                        else:
                            break
        if (((x + 1, y) == target.location) or ((x - 1, y) == target.location)) and target.piece is None and \
                sum([(playing_field[x][y].piece.type in ["pawn", "sPawn"])
                     for x, y in [(target.location[0] + 1, target.location[1]),
                                  (target.location[0] - 1, target.location[1]),
                                  (target.location[0], target.location[1] + 1),
                                  (target.location[0], target.location[1] - 1)] if
                     playing_field[x][y].piece is not None]) >= 3:
            if commit_move:
                target.passable = False
                draw_tile(target.location[0], target.location[1])
            return True, "dig"

        ...
    elif ptype == "knight":
        if (target.location[0] + 1 == x and target.location[1] + 2 == y) or \
                (target.location[0] + 1 == x and target.location[1] - 2 == y) or \
                (target.location[0] - 1 == x and target.location[1] + 2 == y) or \
                (target.location[0] - 1 == x and target.location[1] - 2 == y) or \
                (target.location[0] + 2 == x and target.location[1] + 1 == y) or \
                (target.location[0] + 2 == x and target.location[1] - 1 == y) or \
                (target.location[0] - 2 == x and target.location[1] + 1 == y) or \
                (target.location[0] - 2 == x and target.location[1] - 1 == y):
            if commit_move:
                origin.passable = True
            return True, "nite"

        ...
    elif ptype == "bishop":
        # if ((x + y) % 2) == ((target.location[0] + target.location[1]) % 2) and \
        if not collision(origin, target, ) and ((target.location[0], target.location[1]) in
                                                [(x + mvs, y + mvs) for mvs in range(1, 12)] +
                                                [(x + mvs, y - mvs) for mvs in range(1, 12)] +
                                                [(x - mvs, y + mvs) for mvs in range(1, 12)] +
                                                [(x - mvs, y - mvs) for mvs in range(1, 12)]):
            if target.piece is not None:
                if target.piece.colour != piece.colour:
                    return True, "shop"
                else:
                    return False, ""
            else:
                return True, "shop"

        elif target.piece is not None and target.piece.colour == piece.colour and target.piece.type == piece.type:
            a = (target.location[0] - origin.location[0])
            b = (target.location[1] - origin.location[1])
            if abs(a) == 3 and b == 0:
                if a > 0 and playing_field[origin.location[0] + 1][origin.location[1]].piece is not None \
                        and playing_field[origin.location[0] + 2][origin.location[1]].piece is not None \
                        and playing_field[origin.location[0] + 1][origin.location[1]].piece.type == "pawn" \
                        and playing_field[origin.location[0] + 2][origin.location[1]].piece.type == "pawn" \
                        and playing_field[origin.location[0] + 1][origin.location[1]].piece.colour != piece.colour \
                        and playing_field[origin.location[0] + 2][origin.location[1]].piece.colour != piece.colour:
                    if commit_move:
                        playing_field[origin.location[0] + 1][origin.location[1]].piece = None
                        playing_field[origin.location[0] + 2][origin.location[1]].piece = None
                        draw_tile(origin.location[0] + 1, origin.location[1])
                        draw_tile(origin.location[0] + 2, origin.location[1])
                    return True, "il vaticano"

                elif playing_field[origin.location[0] - 1][origin.location[1]].piece is not None \
                        and playing_field[origin.location[0] - 2][origin.location[1]].piece is not None \
                        and playing_field[origin.location[0] - 1][origin.location[1]].piece.type == "pawn" \
                        and playing_field[origin.location[0] - 2][origin.location[1]].piece.type == "pawn" \
                        and playing_field[origin.location[0] - 1][origin.location[1]].piece.colour != piece.colour \
                        and playing_field[origin.location[0] - 2][origin.location[1]].piece.colour != piece.colour:
                    if commit_move:
                        playing_field[origin.location[0] - 1][origin.location[1]].piece = None
                        playing_field[origin.location[0] - 2][origin.location[1]].piece = None
                        draw_tile(origin.location[0] - 1, origin.location[1])
                        draw_tile(origin.location[0] - 2, origin.location[1])
                    return True, "il vaticano"
            elif a == 0 and abs(b) == 3:
                if b > 0 and playing_field[origin.location[0]][origin.location[1] + 1].piece is not None \
                        and playing_field[origin.location[0]][origin.location[1] + 2].piece is not None \
                        and playing_field[origin.location[0]][origin.location[1] + 1].piece.type == "pawn" \
                        and playing_field[origin.location[0]][origin.location[1] + 2].piece.type == "pawn" \
                        and playing_field[origin.location[0]][origin.location[1] + 1].piece.colour != piece.colour \
                        and playing_field[origin.location[0]][origin.location[1] + 2].piece.colour != piece.colour:
                    if commit_move:
                        playing_field[origin.location[0]][origin.location[1] + 1].piece = None
                        playing_field[origin.location[0]][origin.location[1] + 2].piece = None
                        draw_tile(origin.location[0], origin.location[1] + 1)
                        draw_tile(origin.location[0], origin.location[1] + 2)
                    return True, "il vaticano"

                elif playing_field[origin.location[0]][origin.location[1] - 1].piece is not None \
                        and playing_field[origin.location[0]][origin.location[1] - 2].piece is not None \
                        and playing_field[origin.location[0]][origin.location[1] - 1].piece.type == "pawn" \
                        and playing_field[origin.location[0]][origin.location[1] - 2].piece.type == "pawn" \
                        and playing_field[origin.location[0]][origin.location[1] - 1].piece.colour != piece.colour \
                        and playing_field[origin.location[0]][origin.location[1] - 2].piece.colour != piece.colour:
                    if commit_move:
                        playing_field[origin.location[0]][origin.location[1] - 1].piece = None
                        playing_field[origin.location[0]][origin.location[1] - 2].piece = None
                        draw_tile(origin.location[0], origin.location[1] - 1)
                        draw_tile(origin.location[0], origin.location[1] - 2)
                    return True, "il vaticano"
    elif ptype == "rook":
        if not collision(origin, target, ) and (
                (x == target.location[0]) ^ (y == target.location[1])):  # to je xor
            return True, "lethimcook"
        # elif 1 < piece.location[1] < 9 and target.location[0] == piece.location[0] and target.location[1]
        ...
        # if two rooks of either color are on neighbouring fields, a plane crashes into both of them, destroying them.
    elif ptype == "queen":
        coll, coords = collision(origin, target, ret_coord=True)
        if not coll and (
                (x == target.location[0]) ^ (y == target.location[1]) or ((target.location[0], target.location[1]) in
                                                                          [(x + mvs, y + mvs) for mvs in range(12)] +
                                                                          [(x + mvs, y - mvs) for mvs in range(12)] +
                                                                          [(x - mvs, y + mvs) for mvs in range(12)] +
                                                                          [(x - mvs, y - mvs) for mvs in range(12)])):
            return True, "qbeen"
        elif coll and target.piece is None:
            x1, y1 = origin.location
            x2, y2 = target.location
            d1, d2 = 1 if x1 > x2 else -1 if x2 > x1 else 0, 1 if y1 > y2 else -1 if y2 > y1 else 0
            spot = playing_field[target.location[0] + d1][target.location[1] + d2]
            if spot.piece is not None and spot.location == coords:
                if spot.piece.colour == origin.piece.colour:
                    if commit_move:
                        spot.piece = None
                        draw_tile(target.location[0] + d1, target.location[1] + d2)
                return True, "teleports behind you"
        ...
    elif ptype == "king":
        # print(x, target.location[0], y, target.location[1])
        a = origin.location[0] - target.location[0]
        b = origin.location[1] - target.location[1]
        if abs(a) == 1 and abs(b) == 1 and target.piece is None:
            if playing_field[origin.location[0]][target.location[1]].piece is not None:
                if commit_move:
                    playing_field[origin.location[0]][target.location[1]].piece.colour = piece.colour
                    draw_tile(origin.location[0], target.location[1])
                return True, "wololo"
            elif playing_field[origin.location[1]][target.location[0]].piece is not None:
                if commit_move:
                    playing_field[origin.location[1]][target.location[0]].piece.colour = piece.colour
                    playing_field[origin.location[1]][target.location[0]].piece.movement_direction *= -1
                    draw_tile(origin.location[1], target.location[0])
                return True, "wololo"

        if abs(x - target.location[0]) < 2 and abs(y - target.location[1]) < 2:
            if target.piece is not None:
                if target.piece.colour != piece.colour:  # \
                    # and 1 < target.location[0] < 10 and 1 < target.location[1] < 10:
                    return True, "kink"
            else:
                return True, "kink"

        elif piece.has_not_moved:
            # print(target.location)
            rownum = origin.location[1]
            if target.location[0] == 4 and target.location[1] == origin.location[1] and playing_field[2][
                rownum].piece is not None and playing_field[2][
                rownum].piece.has_not_moved:
                if commit_move:
                    move_piece(5, rownum, playing_field[2][rownum])
                return True, "castling"
            elif target.location[0] == 8 and target.location[1] == origin.location[1] and playing_field[9][
                rownum].piece is not None and playing_field[9][
                rownum].piece.has_not_moved:
                if commit_move:
                    move_piece(7, rownum, playing_field[9][rownum])
                return True, "castling"

    return False, ""


def collision(source, stop, ret_coord=False):
    x1, y1 = source.location
    x2, y2 = stop.location
    # if not (1 < x2 < 10) or not (1 < y2 < 10):
    #    return True
    d1, d2 = 1 if x1 > x2 else -1 if x2 > x1 else 0, 1 if y1 > y2 else -1 if y2 > y1 else 0
    x1 -= d1
    y1 -= d2
    if not ret_coord:
        if (x1, y1) == stop.location:
            return False
        while x1 != x2 or y1 != y2:
            spot = playing_field[x1][y1]
            if spot.piece is not None or not spot.passable:
                return True
            x1 -= d1
            y1 -= d2
        return False
    else:
        if (x1, y1) == stop.location:
            return False, (x1, y1)
        while x1 != x2 or y1 != y2:
            spot = playing_field[x1][y1]
            if spot.piece is not None or not spot.passable:
                return True, (x1, y1)
            x1 -= d1
            y1 -= d2
        return False, (x1, y1)


def where_can_move(origin: Tile):
    defmap = [[False for x in range(12)] for y in range(12)]

    for i in range(12):
        for j in range(12):
            defmap[i][j] = can_move_here(origin, playing_field[i][j], commit_move=False)

    return defmap


def setup_playing_field(screen, ):
    # Fill the background with white*
    screen.fill(background_colour)
    pygame.draw.rect(screen, white_colour,
                     (2 * x_square_size + xoffset, 2 * y_square_size, 8 * x_square_size, 8 * y_square_size))
    for i in range(12):
        for j in range(12):
            if 1 < i < 10 and 1 < j < 10:
                if (i + j) % 2 == 1:
                    pygame.draw.rect(screen, black_colour,
                                     (i * x_square_size + xoffset, j * y_square_size, x_square_size, y_square_size))

    # Draw letters
    draw_letters(font)

    # Populate starting pieces' textures
    pieces = get_pieces()
    # draw pieces
    global playing_field
    global moves
    moves = []
    playing_field = [[Tile((i, j), passable=(1 < i < 10 and 1 < j < 10)) for j in range(12)] for i in range(12)]
    cmap = {"w": "white ", "b": "black "}
    for idx, colour in enumerate(["b", "w"] if starts == "white" else ["w", "b"]):
        if idx == 0:
            j = 7
            factor = 1
        else:
            j = 2
            factor = -1
        for piece in ["pawn", "knight", "bishop", "rook", "queen", "king"]:
            if piece == "pawn":
                for i in range(1, 9, 1):
                    playing_field[i + 1][j + 1].piece = Piece(colour, piece, -factor, )
                    draw_piece(i + 1, j + 1)
                j += factor
            elif piece == "knight":
                for i in [2, 7]:
                    playing_field[i + 1][j + 1].piece = Piece(colour, piece, -factor, )
                    draw_piece(i + 1, j + 1)
            elif piece == "bishop":
                for i in [3, 6]:
                    playing_field[i + 1][j + 1].piece = Piece(colour, piece, -factor, )
                    draw_piece(i + 1, j + 1)
            elif piece == "rook":
                for i in [1, 8]:
                    playing_field[i + 1][j + 1].piece = Piece(colour, piece, -factor, )
                    draw_piece(i + 1, j + 1)
            elif piece == "queen":
                i = 4
                playing_field[i + 1][j + 1].piece = Piece(colour, piece, -factor, )
                draw_piece(i + 1, j + 1)
            elif piece == "king":
                i = 5
                playing_field[i + 1][j + 1].piece = Piece(colour, piece, -factor, )
                draw_piece(i + 1, j + 1)

    # Flip the display
    pygame.display.flip()
    return pieces, cmap, None, None, 0


def show_possible_moves(tile):
    map = where_can_move(tile)
    for i in range(12):
        for j in range(12):
            if map[i][j][0]:
                draw_dot(i, j)
    return map


def clear_possible_moves(map):
    for i in range(12):
        for j in range(12):
            if map[i][j][0]:
                draw_tile(i, j)


if __name__ == '__main__':
    pygame.init()

    font = pygame.font.Font('freesansbold.ttf', 22)
    font2 = pygame.font.Font('freesansbold.ttf', 18)
    # Set up the drawing window
    screen = pygame.display.set_mode([width, height])

    minv = min(width, height)
    xoffset = (width - height) // 2
    if xoffset < 0:
        xoffset = 0
    yoffset = 0
    x_square_size = minv // 12
    y_square_size = minv // 12

    current_map = [[(False,) for _ in range(12)] for _ in range(12)]
    pieces, cmap, selected, prev, clicked = setup_playing_field(screen, )
    # Run until the user asks to quit
    running = True
    # TODO moves has row/col of prev moves, for el passant and that shit
    while running:

        # Did the user click the window close button?
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                xp, yp = event.pos
                row = (xp - xoffset) // x_square_size
                col = (yp - yoffset) // y_square_size
                # print(rows[row], cols[col])
                if row < 0 or row > 11 or col < 0 or col > 11:
                    continue
                prev = clicked
                clicked = playing_field[row][col]
                if not queening:
                    if prev == clicked and selected is not None:
                        print(clicked.location, "Selected:", selected.name)
                    if selected is None:
                        if clicked.piece is not None and clicked.piece.colour == ("w" if len(moves) % 2 == 0 else "b"):
                            selected = clicked
                            print("Selected:", selected.name, selected.piece.type, clicked.location)
                            current_map = show_possible_moves(clicked)
                    else:
                        print(clicked.location, "Selected:", selected.name, selected.piece.name)
                        mv, action = can_move_here(selected, clicked)
                        if mv:
                            clear_possible_moves(current_map)
                            current_map = [[(False,) for _ in range(12)] for _ in range(12)]
                            pygame.draw.rect(screen, background_colour,
                                             (0, 0, xoffset, height))
                            text = font2.render(
                                selected.name + " " + selected.piece.name + " -> " + f"{rows[row]}{cols[col]}", True,
                                (205, 205, 160, 50))
                            moves.append((text, row, col, moves[-1][1] if moves else 0, moves[-1][2] if moves else 0,
                                          selected.piece))
                            for i, (t, _, _, _, _, _) in enumerate(moves[::-1]):
                                textRect = t.get_rect()
                                textRect.left = 20
                                textRect.top = 20 + i * y_square_size * 0.5
                                screen.blit(t, textRect)

                            # print("row, col:", row, col)
                            # where_can_move(selected, clicked, )
                            print(selected.name, selected.piece.name, "->", f"{rows[row]}{cols[col]}")
                            if action not in ["sPawn", "dig", "il vaticano"]:
                                move_piece(row, col, selected)
                            if clicked.piece is not None and clicked.piece.type in ["sPawn", "pawn"] and (
                                    (col + clicked.piece.movement_direction < 0) or (
                                    col + clicked.piece.movement_direction > 11)
                                    or not playing_field[row][col + clicked.piece.movement_direction].passable):
                                queening = True

                            selected = None


            elif event.type == pygame.MOUSEBUTTONUP and event.button == 3:
                if selected is not None:
                    prev = clicked
                    print("Deselecting", selected.name, selected.piece.name)

                    clear_possible_moves(current_map)
                    # playing_field[selected.location[0]][selected.location[1]] = selected.piece
                    selected = None
            elif selected is not None and event.type == pygame.MOUSEMOTION:
                # TODO convert pieces to sprites and only move sprite, then move selected piece with the mouse
                ...
            elif queening and event.type == pygame.KEYDOWN:
                # TODO actually show the possible pieces
                # TODO pawn -> king promotion
                newpiece = ""
                if event.key == pygame.K_p:
                    newpiece = "pawn"
                elif event.key == pygame.K_r:
                    newpiece = "rook"
                elif event.key == pygame.K_q:
                    newpiece = "queen"
                elif event.key == pygame.K_b:
                    newpiece = "bishop"
                elif event.key == pygame.K_k:
                    newpiece = "knight"

                if newpiece != "":
                    queening = False
                    draw_tile(moves[-1][1], moves[-1][2])
                    playing_field[moves[-1][1]][moves[-1][2]].piece = Piece(moves[-1][5].colour, newpiece,
                                                                            moves[-1][5].movement_direction)
                    draw_piece(moves[-1][1], moves[-1][2])




            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    pieces, cmap, selected, prev, clicked = \
                        setup_playing_field(screen, )
                    pygame.draw.rect(screen, background_colour, (0, 0, xoffset, height))

        draw_letters(font)
        pygame.display.flip()
    # Done! Time to quit.
    pygame.quit()
