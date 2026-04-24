import pygame
import random
import sys

pygame.init()

SCREEN_W, SCREEN_H = 400, 600
FPS = 60

ROAD_LEFT = 60
ROAD_RIGHT = 340
LANE_W = (ROAD_RIGHT - ROAD_LEFT) // 3

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (70, 70, 70)
GREEN = (0, 200, 0)
RED = (200, 0, 0)

screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
pygame.display.set_caption("Racer")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 20)

def random_lane_x(w):
    lane = random.randint(0, 2)
    return ROAD_LEFT + lane * LANE_W + (LANE_W - w) // 2


# ── ROAD ─────────────────────────────────────────────
class Road:
    def __init__(self):
        self.offset = 0
        self.speed = 5

    def update(self):
        self.offset = (self.offset + self.speed) % 40

    def draw(self, s):
        s.fill((20, 20, 20))
        pygame.draw.rect(s, GRAY, (ROAD_LEFT, 0, ROAD_RIGHT - ROAD_LEFT, SCREEN_H))

        for i in range(1, 3):
            x = ROAD_LEFT + i * LANE_W
            for y in range(-40, SCREEN_H, 40):
                pygame.draw.rect(s, WHITE, (x - 2, y + self.offset, 4, 20))


# ── PLAYER ───────────────────────────────────────────
class Player:
    W, H = 30, 50

    def __init__(self):
        self.x = SCREEN_W // 2 - self.W // 2
        self.y = SCREEN_H - 100
        self.spd = 5

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.x > ROAD_LEFT:
            self.x -= self.spd
        if keys[pygame.K_RIGHT] and self.x + self.W < ROAD_RIGHT:
            self.x += self.spd

    def draw(self, s):
        pygame.draw.rect(s, GREEN, (self.x, self.y, self.W, self.H), border_radius=6)

    def rect(self):
        return pygame.Rect(self.x, self.y, self.W, self.H)


# ── ENEMY ───────────────────────────────────────────
class Enemy:
    W, H = 30, 50

    def __init__(self, speed):
        self.x = random_lane_x(self.W)
        self.y = -self.H
        self.spd = speed

    def update(self):
        self.y += self.spd

    def draw(self, s):
        pygame.draw.rect(s, RED, (self.x, self.y, self.W, self.H), border_radius=6)

    def rect(self):
        return pygame.Rect(self.x, self.y, self.W, self.H)


# ── COIN (WEIGHTED) ─────────────────────────────────
class Coin:
    def __init__(self, speed):
        self.x = random.randint(ROAD_LEFT + 10, ROAD_RIGHT - 10)
        self.y = -10
        self.spd = speed

        # 🎯 weighted type
        r = random.random()
        if r < 0.1:
            self.value = 3
            self.color = (255, 215, 0)   # gold
        elif r < 0.4:
            self.value = 2
            self.color = (192, 192, 192) # silver
        else:
            self.value = 1
            self.color = (205, 127, 50)  # bronze

    def update(self):
        self.y += self.spd

    def draw(self, s):
        pygame.draw.circle(s, self.color, (self.x, self.y), 8)

    def rect(self):
        return pygame.Rect(self.x - 8, self.y - 8, 16, 16)


# ── HUD ─────────────────────────────────────────────
def draw_hud(s, score, coins):
    s.blit(font.render(f"Score: {score}", True, WHITE), (10, 10))
    s.blit(font.render(f"Coins: {coins}", True, (255, 215, 0)), (250, 10))


# ── MAIN ────────────────────────────────────────────
def main():
    road = Road()
    player = Player()

    enemies = []
    coins = []

    score = 0
    coin_count = 0

    base_speed = 4
    game_over = False

    enemy_timer = 0
    coin_timer = 0

    while True:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if not game_over:
            keys = pygame.key.get_pressed()
            player.move(keys)
            road.update()

            # ── SPEED BASED ON SCORE + COINS ──
            speed = base_speed + score // 5 + coin_count // 10

            road.speed = 5 + score // 8 + coin_count // 10

            # ── SPAWN ENEMIES ──
            enemy_timer += 1
            if enemy_timer > 60:
                enemies.append(Enemy(speed))
                enemy_timer = 0

            # ── SPAWN COINS ──
            coin_timer += 1
            if coin_timer > 100:
                coins.append(Coin(speed))
                coin_timer = 0

            # ── ENEMIES UPDATE ──
            for e in enemies[:]:
                e.update()
                if e.y > SCREEN_H:
                    enemies.remove(e)
                    score += 1
                elif e.rect().colliderect(player.rect()):
                    game_over = True

            # ── COINS UPDATE ──
            for c in coins[:]:
                c.update()
                if c.y > SCREEN_H:
                    coins.remove(c)
                elif c.rect().colliderect(player.rect()):
                    coins.remove(c)
                    coin_count += c.value   # 🔥 weighted coins

        # ── DRAW ──
        road.draw(screen)

        for e in enemies:
            e.draw(screen)

        for c in coins:
            c.draw(screen)

        player.draw(screen)
        draw_hud(screen, score, coin_count)

        if game_over:
            text = font.render("GAME OVER", True, RED)
            screen.blit(text, (120, 280))

        pygame.display.flip()


if __name__ == "__main__":
    main()
