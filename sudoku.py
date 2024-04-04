import pygame as pg

pg.init()

size    = width, height = 271, 271
screen  = pg.display.set_mode(size)
clock   = pg.time.Clock()
font    = pg.font.get_default_font()
bd_font = pg.font.SysFont(font, 26, True, False)
nm_font = pg.font.SysFont(font, 26, False, False)
running = True
dt      = 0

black = (0,   0,   0)
white = (255, 255, 255)

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
            "position": (j * 30 + 11, i * 30 + 10),
            "text": nm_font.render(' ', True, black)
        }
        board[i].append(aux)

def update_cell(x: int, y: int, value: int):
    board[y][x]["value"] = value
    if value == 0:
        board[y][x]["text"] = nm_font.render(' ', True, black)
    else:
        board[y][x]["text"] = nm_font.render(str(value), True, black)

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
            if event.key > pg.K_KP0 and event.key <= pg.K_KP9:
                update_cell(x, y, event.key - pg.K_KP0)

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
        position = pg.mouse.get_pos()
        selected.x = position[0] - position[0] % 30
        selected.y = position[1] - position[1] % 30

    screen.fill(white)
    selected_points = [(selected.x, selected.y), (selected.x + 30, selected.y), (selected.x + 30, selected.y + 30), (selected.x, selected.y + 30)]
    pg.draw.polygon(screen, (0, 0, 255), selected_points, 0)

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