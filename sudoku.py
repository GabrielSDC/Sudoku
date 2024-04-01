import pygame

pygame.init()

size    = width, height = 270, 270
screen  = pygame.display.set_mode(size)
clock   = pygame.time.Clock()
running = True
dt      = 0

thick_lines = []
limit = 0
while limit <= width:
    thick_lines.append((limit, 0))
    thick_lines.append((limit, height))
    thick_lines.append((0, limit))
    thick_lines.append((width, limit))
    limit += 90

thin_lines = []
limit = 0
while limit <= width:
    thin_lines.append((limit, 0))
    thin_lines.append((limit, height))
    thin_lines.append((0, limit))
    thin_lines.append((width, limit))
    limit += 30

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    screen.fill("white")

    for i in range(0, len(thick_lines), 2):
        pygame.draw.line(screen, (0, 0, 0), thick_lines[i], thick_lines[i + 1], 3)
    for i in range(0, len(thin_lines), 2):
        pygame.draw.line(screen, (0, 0, 0), thin_lines[i], thin_lines[i + 1], 1)

    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()