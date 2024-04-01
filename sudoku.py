import pygame
import time

pygame.init()

size    = width, height = 271, 271
screen  = pygame.display.set_mode(size)
clock   = pygame.time.Clock()
running = True
dt      = 0

black = (0,   0,   0)
white = (255, 255, 255)

selected = pygame.Vector2(0, 0)

thick_lines = []
for limit in range(0, width + 1, 90):
    thick_lines.append([(limit, 0), (limit, height)])
    thick_lines.append([(0, limit), (width, limit)])

thin_lines = []
for limit in range(0, width + 1, 30):
    thin_lines.append([(limit, 0), (limit, height)])
    thin_lines.append([(0, limit), (width, limit)])

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    click = pygame.mouse.get_pressed()
    if click[0]:
        position = pygame.mouse.get_pos()
        selected.x = position[0] - position[0] % 30
        selected.y = position[1] - position[1] % 30

    keys_pressed = pygame.key.get_pressed()
    if keys_pressed[pygame.K_UP] or keys_pressed[pygame.K_w]:
        selected.y = max(0, selected.y - 30)
    if keys_pressed[pygame.K_DOWN] or keys_pressed[pygame.K_s]:
        selected.y = min(240, selected.y + 30)
    if keys_pressed[pygame.K_LEFT] or keys_pressed[pygame.K_a]:
        selected.x = max(0, selected.x - 30)
    if keys_pressed[pygame.K_RIGHT] or keys_pressed[pygame.K_d]:
        selected.x = min(240, selected.x + 30)

    screen.fill(white)
    selected_points = [(selected.x, selected.y), (selected.x + 30, selected.y), (selected.x + 30, selected.y + 30), (selected.x, selected.y + 30)]
    pygame.draw.polygon(screen, (0, 0, 255), selected_points, 0)

    for line in thick_lines:
        pygame.draw.line(screen, black, line[0], line[1], 3)
    for line in thin_lines:
        pygame.draw.line(screen, black, line[0], line[1], 1)

    pygame.display.flip()
    dt = clock.tick(10) / 1000

pygame.quit()