import pygame as pg

pg.init()

size    = width, height = 271, 271
screen  = pg.display.set_mode(size)
clock   = pg.time.Clock()
font    = pg.font.get_default_font()
bd_font = pg.font.SysFont(font, 28, True, False)
nm_font = pg.font.SysFont(font, 28, False, False)
running = True
dt      = 0

black   = (0,   0,   0  )
white   = (255, 255, 255)
blue    = (0,   0,   255)
lt_blue = (135, 206, 235)
red     = (255, 0,   0  )

selected = pg.Vector2(0, 0)

thick_lines = []
for limit in range(0, width + 1, 90):
    thick_lines.append([(limit, 0), (limit, height)])
    thick_lines.append([(0, limit), (width, limit)])

thin_lines = []
for limit in range(0, width + 1, 30):
    thin_lines.append([(limit, 0), (limit, height)])
    thin_lines.append([(0, limit), (width, limit)])

board = []
for i in range(9):
    board.append([])
    for j in range(9):
        aux = {
            "value": 0,
            "position": (j * 30 + 11, i * 30 + 7),
            "text": nm_font.render(' ', True, black)
        }
        board[i].append(aux)

conflicting_cells = []

def find_errors(x: int, y: int, value: int) -> bool:
    for i in range(9):
        if i != x and board[y][i]["value"] == value:
            conflicting_cells.append((x, y, i, y))
        if i != y and board[i][x]["value"] == value:
            conflicting_cells.append((x, y, x, i))
    
    section_x, section_y = (x // 3) * 3, (y // 3) * 3
    for i in range(section_y, section_y + 3):
        for j in range(section_x, section_x + 3):
            if (i != y or j != x) and board[i][j]["value"] == value:
                conflicting_cells.append((x, y, j, i))

def update_cell(x: int, y: int, value: int):
    if value == 0:
        board[y][x]["text"] = nm_font.render(' ', True, black)
        found_errors = []
        for error in conflicting_cells:
            (i, j, k, l) = error
            if i == x and j == y or k == x and l == y:
                found_errors.append(error)
        for err in found_errors:
            conflicting_cells.remove(err)
    else:
        board[y][x]["text"] = nm_font.render(str(value), True, black)
        find_errors(x, y, value)

    board[y][x]["value"] = value

def draw_colored_square(x: int, y: int, color: tuple):
    points = [(x, y), (x + 30, y), (x + 30, y + 30), (x, y + 30)]
    pg.draw.polygon(screen, color, points, 0)

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            x, y = int(selected.x // 30), int(selected.y // 30)
            if event.key == pg.K_BACKSPACE:
                update_cell(x, y, 0)
            if event.key > pg.K_0 and event.key <= pg.K_9:
                update_cell(x, y, event.key - pg.K_0)
            if event.key >= pg.K_KP1 and event.key <= pg.K_KP9:
                update_cell(x, y, event.key - pg.K_KP1 + 1)

            if event.key == pg.K_UP or event.key == pg.K_w:
                selected.y = max(0, selected.y - 30)
            if event.key == pg.K_DOWN or event.key == pg.K_s:
                selected.y = min(240, selected.y + 30)
            if event.key == pg.K_LEFT or event.key == pg.K_a:
                selected.x = max(0, selected.x - 30)
            if event.key == pg.K_RIGHT or event.key == pg.K_d:
                selected.x = min(240, selected.x + 30)

    click = pg.mouse.get_pressed()
    if click[0]:
        selected.x, selected.y = pg.mouse.get_pos()
        selected.x -= selected.x % 30
        selected.y -= selected.y % 30

    screen.fill(white)

    sec_x, sec_y = int(selected.x // 30), int(selected.y // 30)
    selected_value = board[sec_y][sec_x]["value"]
    for i in range(9):
        for j in range(9):
            if selected_value and board[i][j]["value"] == selected_value:
                draw_colored_square(j * 30, i * 30, lt_blue)

    for error in conflicting_cells:
        (i, j, k, l) = error
        draw_colored_square(i * 30, j * 30, red)
        draw_colored_square(k * 30, l * 30, red)

    draw_colored_square(selected.x, selected.y, blue)

    for line in board:
        for cell in line:
            screen.blit(cell["text"], cell["position"])

    for line in thick_lines:
        pg.draw.line(screen, black, line[0], line[1], 3)
    for line in thin_lines:
        pg.draw.line(screen, black, line[0], line[1], 1)

    pg.display.flip()
    dt = clock.tick(10) / 1000

pg.quit()