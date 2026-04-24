import pygame
import sys
import math

pygame.init()

SCREEN_W, SCREEN_H = 900, 650
TOOLBAR_H = 60
CANVAS_H = SCREEN_H - TOOLBAR_H

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)

PALETTE = [
    (0,0,0), (255,0,0), (0,255,0), (0,0,255),
    (255,255,0), (255,165,0), (128,0,255)
]

TOOLS = ["pencil", "rect", "circle", "square", "right_tri", "eq_tri", "rhombus", "eraser"]

screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
pygame.display.set_caption("Simple Paint")

clock = pygame.time.Clock()


class Paint:
    def __init__(self):
        self.canvas = pygame.Surface((SCREEN_W, CANVAS_H))
        self.canvas.fill(WHITE)

        self.color = BLACK
        self.tool = "pencil"
        self.size = 5

        self.drawing = False
        self.start = None
        self.prev = None
        self.snapshot = None

    def handle(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.down(event.pos)
        elif event.type == pygame.MOUSEMOTION and self.drawing:
            self.move(event.pos)
        elif event.type == pygame.MOUSEBUTTONUP:
            self.up(event.pos)

    def to_canvas(self, pos):
        return pos[0], pos[1] - TOOLBAR_H

    def down(self, pos):
        x, y = pos

        if y < TOOLBAR_H:
            self.click_toolbar(x, y)
            return

        self.drawing = True
        cp = self.to_canvas(pos)
        self.start = cp
        self.prev = cp

        if self.tool in ["rect", "circle", "square", "right_tri", "eq_tri", "rhombus"]:
            self.snapshot = self.canvas.copy()

        if self.tool == "pencil":
            pygame.draw.circle(self.canvas, self.color, cp, self.size)

        if self.tool == "eraser":
            pygame.draw.circle(self.canvas, WHITE, cp, self.size)

    def move(self, pos):
        cp = self.to_canvas(pos)

        if self.tool == "pencil":
            pygame.draw.line(self.canvas, self.color, self.prev, cp, self.size * 2)
            self.prev = cp

        elif self.tool == "eraser":
            pygame.draw.circle(self.canvas, WHITE, cp, self.size)
            self.prev = cp

        elif self.tool in ["rect", "circle", "square", "right_tri", "eq_tri", "rhombus"]:
            self.canvas.blit(self.snapshot, (0,0))
            self.draw_shape(self.start, cp, self.canvas)

    def up(self, pos):
        if not self.drawing:
            return

        cp = self.to_canvas(pos)

        if self.tool in ["rect", "circle", "square", "right_tri", "eq_tri", "rhombus"]:
            self.canvas.blit(self.snapshot, (0,0))
            self.draw_shape(self.start, cp, self.canvas)

        self.drawing = False
        self.start = None
        self.prev = None
        self.snapshot = None

    def draw_shape(self, p1, p2, surf):
        x1, y1 = p1
        x2, y2 = p2

        # RECTANGLE
        if self.tool == "rect":
            rect = pygame.Rect(min(x1,x2), min(y1,y2), abs(x2-x1), abs(y2-y1))
            pygame.draw.rect(surf, self.color, rect, 2)

        # SQUARE
        elif self.tool == "square":
            size = min(abs(x2-x1), abs(y2-y1))
            rect = pygame.Rect(x1, y1,
                               size if x2>x1 else -size,
                               size if y2>y1 else -size)
            rect.normalize()
            pygame.draw.rect(surf, self.color, rect, 2)

        # CIRCLE
        elif self.tool == "circle":
            cx = (x1 + x2)//2
            cy = (y1 + y2)//2
            r = int(math.hypot(x2-x1, y2-y1)/2)
            pygame.draw.circle(surf, self.color, (cx,cy), r, 2)

        # RIGHT TRIANGLE
        elif self.tool == "right_tri":
            points = [(x1,y1), (x1,y2), (x2,y2)]
            pygame.draw.polygon(surf, self.color, points, 2)

        # EQUILATERAL TRIANGLE
        elif self.tool == "eq_tri":
            base = x2 - x1
            height = int(abs(base) * math.sqrt(3)/2)

            points = [
                (x1, y2),
                (x2, y2),
                ((x1+x2)//2, y2 - height)
            ]
            pygame.draw.polygon(surf, self.color, points, 2)

        # RHOMBUS
        elif self.tool == "rhombus":
            cx = (x1 + x2)//2
            cy = (y1 + y2)//2

            dx = abs(x2 - x1)//2
            dy = abs(y2 - y1)//2

            points = [
                (cx, cy - dy),
                (cx + dx, cy),
                (cx, cy + dy),
                (cx - dx, cy)
            ]
            pygame.draw.polygon(surf, self.color, points, 2)

    def click_toolbar(self, x, y):
        # palette
        for i,c in enumerate(PALETTE):
            if 10 + i*30 <= x <= 35 + i*30:
                self.color = c
                return

        # tools
        for i,t in enumerate(TOOLS):
            if 300 + i*90 <= x <= 380 + i*90:
                self.tool = t
                return

        # size controls
        if 780 <= x <= 810:
            self.size = max(1, self.size - 1)
        if 820 <= x <= 850:
            self.size = min(40, self.size + 1)

        # clear
        if 860 <= x <= 890:
            self.canvas.fill(WHITE)

    def draw(self, surf):
        surf.blit(self.canvas, (0, TOOLBAR_H))

        pygame.draw.rect(surf, GRAY, (0,0,SCREEN_W,TOOLBAR_H))

        # palette
        for i,c in enumerate(PALETTE):
            pygame.draw.rect(surf, c, (10 + i*30, 15, 20, 20))

        # tools
        for i,t in enumerate(TOOLS):
            col = (100,160,255) if t == self.tool else (150,150,150)
            pygame.draw.rect(surf, col, (300 + i*90, 15, 80, 25))
            label = pygame.font.SysFont("Arial", 14).render(t, True, BLACK)
            surf.blit(label, (305 + i*90, 18))

        # size buttons
        pygame.draw.rect(surf, WHITE, (780, 15, 30, 25))
        pygame.draw.rect(surf, WHITE, (820, 15, 30, 25))
        pygame.draw.rect(surf, WHITE, (860, 15, 30, 25))

        font = pygame.font.SysFont("Arial", 14)
        surf.blit(font.render("-", True, BLACK), (790, 18))
        surf.blit(font.render("+", True, BLACK), (830, 18))
        surf.blit(font.render("C", True, BLACK), (870, 18))

        surf.blit(font.render(str(self.size), True, BLACK), (750, 18))

        if self.tool == "eraser":
            mx,my = pygame.mouse.get_pos()
            pygame.draw.circle(surf, (120,120,120), (mx,my), self.size, 1)


def main():
    app = Paint()

    while True:
        clock.tick(60)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            app.handle(e)

        screen.fill(WHITE)
        app.draw(screen)
        pygame.display.flip()


if __name__ == "__main__":
    main()
