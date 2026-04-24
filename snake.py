import pygame
import random
import time

pygame.init()

WIDTH, HEIGHT = 600, 400
CELL = 20

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")

clock = pygame.time.Clock()

WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
BLACK = (0, 0, 0)

font = pygame.font.SysFont("Arial", 20)

snake = [(100, 100), (80, 100), (60, 100)]
direction = (CELL, 0)

# ── FOOD SYSTEM ───────────────────────────────
def generate_food():
    x = random.randrange(0, WIDTH, CELL)
    y = random.randrange(0, HEIGHT, CELL)

    # weighted food types
    r = random.random()
    if r < 0.6:
        return (x, y, 1, (255, 0, 0))      # apple
    elif r < 0.9:
        return (x, y, 2, (0, 255, 0))      # grapes
    else:
        return (x, y, 3, (255, 255, 0))    # watermelon


food = generate_food()
food_spawn_time = time.time()
FOOD_LIFETIME = 5   # seconds

score = 0
level = 1
speed = 7

running = True

# ── GAME LOOP ───────────────────────────────
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != (0, CELL):
                direction = (0, -CELL)
            elif event.key == pygame.K_DOWN and direction != (0, -CELL):
                direction = (0, CELL)
            elif event.key == pygame.K_LEFT and direction != (CELL, 0):
                direction = (-CELL, 0)
            elif event.key == pygame.K_RIGHT and direction != (-CELL, 0):
                direction = (CELL, 0)

    # ── MOVE SNAKE ──
    head_x = snake[0][0] + direction[0]
    head_y = snake[0][1] + direction[1]
    new_head = (head_x, head_y)

    if head_x < 0 or head_x >= WIDTH or head_y < 0 or head_y >= HEIGHT:
        running = False

    if new_head in snake:
        running = False

    snake.insert(0, new_head)

    fx, fy, fvalue, fcolor = food

    # ── EAT FOOD ──
    if new_head == (fx, fy):
        score += fvalue
        food = generate_food()
        food_spawn_time = time.time()

        if score % 4 == 0:
            level += 1
            speed += 1
    else:
        snake.pop()

    # ── TIMER LOGIC (food disappears) ──
    if time.time() - food_spawn_time > FOOD_LIFETIME:
        food = generate_food()
        food_spawn_time = time.time()

    # ── DRAW ──
    screen.fill(BLACK)

    for segment in snake:
        pygame.draw.rect(screen, GREEN, (*segment, CELL, CELL))

    # food
    pygame.draw.rect(screen, fcolor, (fx, fy, CELL, CELL))

    # HUD
    score_text = font.render(f"Score: {score}", True, WHITE)
    level_text = font.render(f"Level: {level}", True, WHITE)

    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (10, 30))

    pygame.display.update()
    clock.tick(speed)

pygame.quit()
