import pygame
import math

pygame.init()

SCREEN_W, SCREEN_H = 1000, 600
TOOLBAR_H = 80

screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
pygame.display.set_caption("Paint UI Version")
clock = pygame.time.Clock()

canvas = pygame.Surface((SCREEN_W, SCREEN_H - TOOLBAR_H))
canvas.fill((255, 255, 255))

font = pygame.font.SysFont("Arial", 14)

# ── STATE ─────────────────────────────
tool = "brush"
color = (0, 0, 0)
radius = 10
drawing = False
start_pos = None
last_pos = None

# ── BUTTONS ───────────────────────────
buttons = {
    "brush": pygame.Rect(10, 20, 60, 30),
    "eraser": pygame.Rect(80, 20, 60, 30),
    "rect": pygame.Rect(150, 20, 50, 30),
    "circle": pygame.Rect(210, 20, 60, 30),
    "square": pygame.Rect(280, 20, 60, 30),
    "right tri": pygame.Rect(350, 20, 70, 30),
    "eq tri": pygame.Rect(430, 20, 60, 30),
    "rhombus": pygame.Rect(500, 20, 70, 30),
    "clear": pygame.Rect(580, 20, 60, 30),

    "black": pygame.Rect(660, 20, 30, 30),
    "red": pygame.Rect(700, 20, 30, 30),
    "green": pygame.Rect(740, 20, 30, 30),
    "blue": pygame.Rect(780, 20, 30, 30),
}

# ── FUNCTIONS ─────────────────────────
def draw_line(surface, color, start, end, radius):
    if not start or not end:
        return
    dx, dy = end[0] - start[0], end[1] - start[1]
    steps = max(abs(dx), abs(dy))
    for i in range(int(steps) + 1):
        x = int(start[0] + i / steps * dx) if steps else start[0]
        y = int(start[1] + i / steps * dy) if steps else start[1]
        pygame.draw.circle(surface, color, (x, y), radius)

def get_pts(name, s, e):
    x1, y1 = s
    x2, y2 = e
    w, h = x2 - x1, y2 - y1

    if name == "square":
        side = max(abs(w), abs(h))
        sw = side if w > 0 else -side
        sh = side if h > 0 else -side
        return [(x1, y1), (x1+sw, y1), (x1+sw, y1+sh), (x1, y1+sh)]

    if name == "right tri":
        return [(x1, y1), (x1, y2), (x2, y2)]

    if name == "eq tri":
        return [(x1 + w//2, y1), (x2, y2), (x1, y2)]

    if name == "rhombus":
        return [(x1 + w//2, y1), (x2, y1 + h//2), (x1 + w//2, y2), (x1, y1 + h//2)]

    return []

def draw_button(name, rect, active=False):
    if name in ["black", "red", "green", "blue"]:
        color_btn = {
            "black": (0,0,0),
            "red": (255,0,0),
            "green": (0,255,0),
            "blue": (0,0,255)
        }[name]
    else:
        color_btn = (100, 100, 100) if active else (200, 200, 200)

    pygame.draw.rect(screen, color_btn, rect)
    pygame.draw.rect(screen, (0,0,0), rect, 1)

    text = font.render(name, True, (255,255,255) if name in ["black","blue","red","green"] else (0,0,0))
    screen.blit(text, (rect.x + 5, rect.y + 5))

# ── MAIN LOOP ─────────────────────────
while True:
    mx, my = pygame.mouse.get_pos()
    cur = (mx, my - TOOLBAR_H)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        # MOUSE DOWN
        if event.type == pygame.MOUSEBUTTONDOWN:
            if my < TOOLBAR_H:
                for name, rect in buttons.items():
                    if rect.collidepoint(mx, my):
                        if name == "clear":
                            canvas.fill((255, 255, 255))
                        elif name in ["black", "red", "green", "blue"]:
                            color = {
                                "black": (0,0,0),
                                "red": (255,0,0),
                                "green": (0,255,0),
                                "blue": (0,0,255)
                            }[name]
                        else:
                            tool = name
            else:
                drawing = True
                start_pos = cur
                last_pos = cur

        # MOUSE UP
        if event.type == pygame.MOUSEBUTTONUP:
            if drawing:
                if tool in ["square", "right tri", "eq tri", "rhombus"]:
                    pts = get_pts(tool, start_pos, cur)
                    pygame.draw.polygon(canvas, color, pts, 2)

                elif tool == "rect":
                    r = pygame.Rect(start_pos, (cur[0]-start_pos[0], cur[1]-start_pos[1]))
                    r.normalize()
                    pygame.draw.rect(canvas, color, r, 2)

                elif tool == "circle":
                    d = int(math.hypot(cur[0]-start_pos[0], cur[1]-start_pos[1]))
                    pygame.draw.circle(canvas, color, start_pos, d, 2)

                drawing = False

    # DRAWING (brush / eraser)
    if drawing and my >= TOOLBAR_H:
        if tool == "brush":
            draw_line(canvas, color, last_pos, cur, radius)
        elif tool == "eraser":
            draw_line(canvas, (255, 255, 255), last_pos, cur, radius)
        last_pos = cur

    # ── RENDER ──
    screen.fill((220, 220, 220))
    screen.blit(canvas, (0, TOOLBAR_H))

    # preview
    if drawing and my >= TOOLBAR_H:
        if tool in ["square", "right tri", "eq tri", "rhombus"]:
            pts = [(p[0], p[1] + TOOLBAR_H) for p in get_pts(tool, start_pos, cur)]
            pygame.draw.polygon(screen, color, pts, 2)

        elif tool == "rect":
            pygame.draw.rect(
                screen,
                color,
                (start_pos[0], start_pos[1]+TOOLBAR_H, mx-start_pos[0], my-TOOLBAR_H-start_pos[1]),
                2
            )

        elif tool == "circle":
            d = int(math.hypot(cur[0]-start_pos[0], cur[1]-start_pos[1]))
            pygame.draw.circle(screen, color, (start_pos[0], start_pos[1]+TOOLBAR_H), d, 2)

    pygame.draw.rect(screen, (180, 180, 180), (0, 0, SCREEN_W, TOOLBAR_H))

    for name, rect in buttons.items():
        draw_button(name, rect, tool == name)

    pygame.display.flip()
    clock.tick(60)
