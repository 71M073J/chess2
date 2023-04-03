import pygame

rows = ["-B", "-A"] + ["A", "B", "C", "D", "E", "F", "G", "H"] + ["-H", "-G"]
cols = ["10", "9"] + [str(x + 1) for x in range(8)][::-1] + ["-1", "-2"]
width = 1280
height = 800
starts = "black"
white_colour = (170, 110, 150)
black_colour = (0, 0, 0)
background_colour = (118, 150, 86)
pieces = {}


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


def get_pieces(x_square_size, y_square_size):
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


def draw_letters(xoffset, yoffset, x_square_size, y_square_size, font):
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


def draw_piece(colour, piece, xoffset, yoffset, x_square_size, y_square_size, row, rank):
    # print(colour, piece, )
    img = pieces[colour][piece]
    rect = img.get_rect()
    rect.center = (xoffset + (row + 2. - 0.5) * x_square_size, yoffset + (rank + 2. - 0.5) * y_square_size)
    screen.blit(img, rect)


def draw_dot(colour, piece, xoffset, yoffset, x_square_size, y_square_size, row, rank):
    # print(colour, piece, )
    pygame.draw.circle(screen, black_colour,
                       (xoffset + (row + 2. - 0.5) * x_square_size, yoffset + (rank + 2. - 0.5) * y_square_size), 20)

    pygame.display.update()


def clear_square(i, j, xoffset, yoffset, x_square_size, y_square_size, piece, tile, override=False,
                 override_color=background_colour):
    print(i, j, "Cleared")
    if not override:
        if tile.passable or (1 < i < 10 and 1 < j < 10) or piece == "knight":
            pygame.draw.rect(screen, black_colour if (i + j) % 2 == 1 else white_colour,
                             (i * x_square_size + xoffset, j * y_square_size, x_square_size, y_square_size))
            tile.passable = True
        else:
            pygame.draw.rect(screen, background_colour,
                             (i * x_square_size + xoffset, j * y_square_size, x_square_size, y_square_size))
    else:
        pygame.draw.rect(screen, override_color,
                         (i * x_square_size + xoffset, j * y_square_size, x_square_size, y_square_size))


def move_piece(tox, toy, selected, xoffset, yoffset, x_square_size, y_square_size, playing_field, clicked):
    if clicked.piece is not None:
        clear_square(clicked.location[0], clicked.location[1], xoffset, yoffset, x_square_size, y_square_size,
                     selected.piece.type, selected)
    selected.piece.has_not_moved = False
    draw_piece(selected.piece.colour, selected.piece.type, xoffset, yoffset, x_square_size, y_square_size, tox - 1,
               toy - 1)

    clear_square(selected.location[0], selected.location[1], xoffset, yoffset, x_square_size, y_square_size,
                 selected.piece.type, selected)
    playing_field[tox][toy].piece = selected.piece
    playing_field[selected.location[0]][selected.location[1]].piece = None


def can_move_here(origin, target, playing_field, moves, ):  # TODO
    if target.piece is not None and target.piece.colour == origin.piece.colour:
        return False, ""
    if not target.passable and origin.piece.type != "knight":
        return False, ""
    piece = origin.piece
    ptype = piece.type
    x, y = origin.location
    #print(x, y, target.location)
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
            elif same_row and moves:
                if moves[-1][1] == x - 1:
                    playing_field[x - 1][y].piece = None
                    clear_square(x - 1, y, xoffset, yoffset, x_square_size, y_square_size, ptype,
                                 playing_field[x - 1][y])
                    return True, "enpassant"
                if moves[-1][1] == x + 1:
                    playing_field[x + 1][y].piece = None
                    clear_square(x + 1, y, xoffset, yoffset, x_square_size, y_square_size, ptype,
                                 playing_field[x + 1][y])
                    return True, "enpassant"
        if same_row and ((((x + 2, y + piece.movement_direction * 2) == target.location) and (moves[-1][1] > x)) or
                         (((x - 2, y + piece.movement_direction * 2) == target.location) and (moves[-1][1] < x))) and (
                target.piece is None) and not collision(origin, target, playing_field):
            playing_field[moves[-1][1]][moves[-1][2]].piece = None
            clear_square(moves[-1][1], moves[-1][2], xoffset, yoffset, x_square_size, y_square_size, ptype,
                         playing_field[moves[-1][1]][moves[-1][2]])
            ...
            return True, "omegapassant"
        if (y + piece.movement_direction < 0) or (y + piece.movement_direction > 11) or not playing_field[x][y + piece.movement_direction].passable:
            newname = "sPawn" if ptype == "pawn" else "pawn"
            for yoff in range(1, 12):
                if 0 <= (y - piece.movement_direction * yoff) <= 11:
                    if playing_field[x][y - piece.movement_direction * yoff].piece is None:
                        if target.location == (x, y - piece.movement_direction * yoff):
                            playing_field[x][y - piece.movement_direction * yoff].piece = Piece(ptype=newname,
                                                                                                direction=piece.movement_direction * -1,
                                                                                                colour=piece.colour)
                            draw_piece(piece.colour, newname, xoffset, yoffset, x_square_size, y_square_size, x - 1,
                                       y - 1 - piece.movement_direction * yoff)
                            return True, "sPawn"
                        else:
                            break
        if (((x + 1, y) == target.location) or ((x - 1, y) == target.location)) and target.piece is None and\
                sum([(playing_field[x][y].piece.type in ["pawn", "sPawn"])
                     for x, y in [(target.location[0] + 1, target.location[1]),
                                  (target.location[0] - 1, target.location[1]),
                                  (target.location[0], target.location[1] + 1),
                                  (target.location[0], target.location[1] - 1)] if playing_field[x][y].piece is not None]) >= 3:
            target.passable = False
            clear_square(target.location[0], target.location[1], xoffset, yoffset, x_square_size, y_square_size, None,
                         None, override=True)
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
            return True, "nite"

        ...
    elif ptype == "bishop":
        # if ((x + y) % 2) == ((target.location[0] + target.location[1]) % 2) and \
        if not collision(origin, target, playing_field) and ((target.location[0], target.location[1]) in
                                                             [(x + mvs, y + mvs) for mvs in range(1, 12)] +
                                                             [(x + mvs, y - mvs) for mvs in range(1, 12)] +
                                                             [(x - mvs, y + mvs) for mvs in range(1, 12)] +
                                                             [(x - mvs, y - mvs) for mvs in range(1, 12)]):
            return True, "shop"
        ...
    elif ptype == "rook":
        if not collision(origin, target, playing_field) and (
                (x == target.location[0]) ^ (y == target.location[1])):  # to je xor
            return True, "lethimcook"
        #elif 1 < piece.location[1] < 9 and target.location[0] == piece.location[0] and target.location[1]
        ...
    elif ptype == "queen":
        coll, coords = collision(origin, target, playing_field, ret_coord=True)
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
                    spot.piece = None
                    clear_square(target.location[0] + d1, target.location[1] + d2, xoffset, yoffset, x_square_size,
                                 y_square_size, ptype,
                                 spot)
                return True, "teleports behind you"
        ...
    elif ptype == "king":
        # print(x, target.location[0], y, target.location[1])
        if abs(x - target.location[0]) < 2 and abs(y - target.location[1]) < 2:  # \
            # and 1 < target.location[0] < 10 and 1 < target.location[1] < 10:
            return True, "kink"
        ...
    return False, ""


def collision(source, stop, playing_field, ret_coord=False):
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


def where_can_move(origin: Tile, target: Tile, playing_field, ):
    defmap = [[False for x in range(12)] for y in range(12)]
    piece = origin.piece
    ptype = piece.type
    x, y = origin.location
    print(x, y)
    if ptype == "pawn":
        if 1 < (y + piece.movement_direction) < 10:
            if playing_field[x][y + piece.movement_direction].piece is None:
                defmap[x][y + piece.movement_direction] = True
        if piece.has_not_moved or True:
            if playing_field[x][y + (piece.movement_direction * 2)].piece is None:
                defmap[x][y + (piece.movement_direction * 2)] = True
        ...
    elif ptype == "knight":
        ...
    elif ptype == "bishop":
        ...
    elif ptype == "rook":
        ...
    elif ptype == "queen":
        ...
    elif ptype == "king":
        ...
    print(defmap)


def setup_playing_field(screen, xoffset, yoffset, x_square_size, y_square_size, ):

    # Fill the background with white*
    screen.fill(background_colour)
    pygame.draw.rect(screen, white_colour,
                     (2 * x_square_size + xoffset, 2 * y_square_size, 8 * x_square_size, 8 * y_square_size))
    for i in range(12):
        for j in range(12):
            if 1 < i < 10 and 1 < j < 10:
                if (i + j) % 2 == 1:
                    pygame.draw.rect(screen, (0, 0, 0),
                                     (i * x_square_size + xoffset, j * y_square_size, x_square_size, y_square_size))

    # Draw letters
    draw_letters(xoffset, yoffset, x_square_size, y_square_size, font)

    # Populate starting pieces' textures
    pieces = get_pieces(x_square_size, y_square_size)
    # draw pieces
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
                    draw_piece(colour, piece, xoffset, yoffset, x_square_size, y_square_size, i, j)
                    playing_field[i + 1][j + 1].piece = Piece(colour, piece, -factor, )
                j += factor
            elif piece == "knight":
                for i in [2, 7]:
                    draw_piece(colour, piece, xoffset, yoffset, x_square_size, y_square_size, i, j)
                    playing_field[i + 1][j + 1].piece = Piece(colour, piece, -factor, )
            elif piece == "bishop":
                for i in [3, 6]:
                    draw_piece(colour, piece, xoffset, yoffset, x_square_size, y_square_size, i, j)
                    playing_field[i + 1][j + 1].piece = Piece(colour, piece, -factor, )
            elif piece == "rook":
                for i in [1, 8]:
                    draw_piece(colour, piece, xoffset, yoffset, x_square_size, y_square_size, i, j)
                    playing_field[i + 1][j + 1].piece = Piece(colour, piece, -factor, )
            elif piece == "queen":
                i = 4
                draw_piece(colour, piece, xoffset, yoffset, x_square_size, y_square_size, i, j)
                playing_field[i + 1][j + 1].piece = Piece(colour, piece, -factor, )
            elif piece == "king":
                i = 5
                draw_piece(colour, piece, xoffset, yoffset, x_square_size, y_square_size, i, j)
                playing_field[i + 1][j + 1].piece = Piece(colour, piece, -factor, )

    # Flip the display
    pygame.display.flip()
    return pieces, playing_field, cmap, [], None, None, 0


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

    pieces, playing_field, cmap, moves, selected, prev, clicked = setup_playing_field(screen, xoffset, yoffset,
                                                                                      x_square_size, y_square_size, )
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
                if prev == clicked and selected is not None:
                    print(clicked.location, "Selected:", selected.name)
                if selected is None:
                    if clicked.piece is not None and clicked.piece.colour == ("w" if len(moves) % 2 == 0 else "b"):
                        selected = clicked
                        print("Selected:", selected.name, selected.piece.type, clicked.location)
                else:
                    print(clicked.location, "Selected:", selected.name)
                    mv, action = can_move_here(selected, clicked, playing_field, moves)
                    if mv:
                        pygame.draw.rect(screen, background_colour,
                                         (0, 0, xoffset, height))
                        text = font2.render(
                            selected.name + " " + selected.piece.name + " -> " + f"{rows[row]}{cols[col]}", True,
                            (205, 205, 160, 50))
                        moves.append((text, row, col))
                        for i, (t, _, _) in enumerate(moves[::-1]):
                            textRect = t.get_rect()
                            textRect.left = 20
                            textRect.top = 20 + i * y_square_size * 0.5
                            screen.blit(t, textRect)

                        #print("row, col:", row, col)
                        # where_can_move(selected, clicked, playing_field)
                        print(selected.name, selected.piece.name, "->", f"{rows[row]}{cols[col]}")
                        if action not in ["sPawn", "dig"]:
                            move_piece(row, col, selected, xoffset, yoffset, x_square_size, y_square_size,
                                       playing_field,
                                       clicked)

                        selected = None

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 3:
                if selected is not None:
                    prev = clicked
                    print("Deselecting", selected.name, selected.piece.name)
                    # playing_field[selected.location[0]][selected.location[1]] = selected.piece
                    selected = None
            elif selected is not None and event.type == pygame.MOUSEMOTION:
                # TODO convert pieces to sprites and only move sprite, then move selected piece with the mouse
                ...
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:

                    pieces, playing_field, cmap, moves, selected, prev, clicked = \
                        setup_playing_field(screen, xoffset, yoffset, x_square_size, y_square_size, )
                    pygame.draw.rect(screen, background_colour, (0, 0, xoffset, height))

        draw_letters(xoffset, yoffset, x_square_size, y_square_size, font)
        pygame.display.flip()
    # Done! Time to quit.
    pygame.quit()
