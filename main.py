import pygame

rows = ["-B", "-A"] + ["A", "B", "C", "D", "E", "F", "G", "H"] + ["-H", "-G"]
cols = ["-7", "-8"] + [str(x + 1) for x in range(8)][::-1] + ["-1", "-2"]
width = 1280
height = 800
starts = "black"
white_colour = (170, 110, 150)
black_colour = (0, 0, 0)
background_colour = (118, 150, 86)


class Tile:
    def __init__(self, location, ttype="normal"):
        self.type = ttype
        self.passable = True
        self.piece = None
        self.name = rows[location[0]] + cols[location[1]]
        self.location = location


class Piece:
    def __init__(self, colour, ptype, direction):
        self.colour = colour
        self.type = ptype
        self.movement_direction = direction
        self.has_not_moved = True
        self.name = ("white " if colour == "w" else "black ") + self.type

def get_pieces(x_square_size, y_square_size):
    pieces = {}
    for sets in ["b", "w"]:
        pieces[sets] = {}
        for piece in ["pawn", "knight", "bishop", "rook", "queen", "king"]:
            img = pygame.image.load(f"./JohnPablok Cburnett Chess set/PNGs/No shadow/1x/{sets}_{piece}_1x_ns.png")
            img = pygame.transform.scale(img, (x_square_size * 0.8, y_square_size * 0.8))
            pieces[sets][piece] = img

    return pieces


def draw_letters(xoffset, yoffset, x_square_size, y_square_size):
    font = pygame.font.Font('freesansbold.ttf', 22)
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
    pygame.draw.circle(screen, black_colour, (xoffset + (row + 2. - 0.5) * x_square_size, yoffset + (rank + 2. - 0.5) * y_square_size), 20)

    pygame.display.update()

def clear_square(i, j, xoffset, yoffset, x_square_size, y_square_size):
    pygame.draw.rect(screen, black_colour if (i + j) % 2 == 1 else white_colour,
                     (i * x_square_size + xoffset, j * y_square_size, x_square_size, y_square_size))


def move_piece(tox, toy, selected, xoffset, yoffset, x_square_size, y_square_size, playing_field, clicked):
    if clicked.piece is not None:
        clear_square(clicked.location[0], clicked.location[1], xoffset, yoffset, x_square_size, y_square_size)
    selected.piece.has_not_moved = False
    draw_piece(selected.piece.colour, selected.piece.type, xoffset, yoffset, x_square_size, y_square_size, tox - 1, toy - 1)

    clear_square(selected.location[0], selected.location[1], xoffset, yoffset, x_square_size, y_square_size)
    playing_field[tox][toy].piece = selected.piece
    playing_field[selected.location[0]][selected.location[1]].piece = None


def can_move_here(origin, target, playing_field, ):  # TODO
    piece = origin.piece
    ptype = piece.type
    x, y = origin.location
    print(x, y)
    if ptype == "pawn":
        if 1 < (y + piece.movement_direction) < 10:
            if (((x, y + piece.movement_direction) == target.location) or\
               ((x, y + (piece.movement_direction * 2)) == target.location and piece.has_not_moved))\
                    and target.piece is None:
                print("premik naravnost, brez požiranja")
                return True
            if (((x + 1, y + piece.movement_direction) == target.location) or\
                  ((x - 1, y + piece.movement_direction) == target.location)) and target.piece is not None:
                print("požiranje")
                return True
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
    return False

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


if __name__ == '__main__':
    pygame.init()

    # Set up the drawing window
    screen = pygame.display.set_mode([width, height])

    # Fill the background with white*
    screen.fill(background_colour)

    minv = min(width, height)
    xoffset = (width - height) // 2
    if xoffset < 0:
        xoffset = 0
    yoffset = 0
    x_square_size = minv // 12
    y_square_size = minv // 12
    pygame.draw.rect(screen, white_colour,
                     (2 * x_square_size + xoffset, 2 * y_square_size, 8 * x_square_size, 8 * y_square_size))
    for i in range(12):
        for j in range(12):
            if 1 < i < 10 and 1 < j < 10:
                if (i + j) % 2 == 1:
                    pygame.draw.rect(screen, (0, 0, 0),
                                     (i * x_square_size + xoffset, j * y_square_size, x_square_size, y_square_size))

    # Draw letters
    draw_letters(xoffset, yoffset, x_square_size, y_square_size)

    # Populate starting pieces' textures
    pieces = get_pieces(x_square_size, y_square_size)
    # draw pieces
    playing_field = [[Tile((i, j)) for j in range(12)] for i in range(12)]
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
    # Run until the user asks to quit
    running = True
    selected = None
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
                clicked = playing_field[row][col]
                if selected is None:
                    if clicked.piece is not None:
                        selected = clicked
                        # print(selected.piece.type, clicked.location)
                else:
                    if can_move_here(selected, clicked, playing_field):  # TODO namesto tega if (can_move_here)
                        print("row, col:", row, col)
                        #where_can_move(selected, clicked, playing_field)
                        print(selected.name, selected.piece.name, "->", f"{rows[row]}{cols[col]}")
                        move_piece(row, col, selected, xoffset, yoffset, x_square_size, y_square_size, playing_field, clicked)
                        selected = None

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 3:
                if selected is not None:
                    # playing_field[selected.location[0]][selected.location[1]] = selected.piece
                    selected = None
        pygame.display.flip()
    # Done! Time to quit.
    pygame.quit()
