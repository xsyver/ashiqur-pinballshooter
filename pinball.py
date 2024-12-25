from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

# Initialize constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
BALL_RADIUS = 10
PAD_WIDTH = 100
PAD_HEIGHT = 10
GRAVITY = 0.05
BOUNCE_STRENGTH = 9.0
INITIAL_BALL_SPEED = 3.0

# Game state variables
ball_x = 400
ball_y = 300
ball_dx = 3.0
ball_dy = -3.0
pad_x = 350
pad_y = 50

score = 0
high_score = 0
lives = 3
game_over = False

# Power-ups
active_power_ups = [
    {"x": random.randint(100, 700), "y": random.randint(200, 500), "type": "extra_life", "active": True},
    {"x": random.randint(100, 700), "y": random.randint(200, 500), "type": "wide_paddle", "active": True}
]

# Floating balls (formerly bars)
floating_balls = [
    {"x": 200, "y": 400, "hit": False},
    {"x": 450, "y": 450, "hit": False},
    {"x": 300, "y": 500, "hit": False}
]

# Midpoint Circle Drawing Algorithm
def draw_circle_midpoint(cx, cy, radius):
    x = 0
    y = radius
    p = 1 - radius

    def plot_circle_points(cx, cy, x, y):
        points = [
            (cx + x, cy + y), (cx - x, cy + y),
            (cx + x, cy - y), (cx - x, cy - y),
            (cx + y, cy + x), (cx - y, cy + x),
            (cx + y, cy - x), (cx - y, cy - x)
        ]
        for px, py in points:
            glVertex2f(px, py)

    glBegin(GL_POINTS)
    plot_circle_points(cx, cy, x, y)
    while x < y:
        x += 1
        if p < 0:
            p += 2 * x + 1
        else:
            y -= 1
            p += 2 * (x - y) + 1
        plot_circle_points(cx, cy, x, y)
    glEnd()

# Draw the ball
def draw_ball():
    glColor3f(1.0, 0.0, 0.0)
    draw_circle_midpoint(ball_x, ball_y, BALL_RADIUS)

# Draw the paddle
def draw_pad():
    glColor3f(0.0, 1.0, 0.0)
    for x in range(pad_x, pad_x + PAD_WIDTH + 1):
        for y in range(pad_y, pad_y + PAD_HEIGHT + 1):
            glBegin(GL_POINTS)
            glVertex2f(x, y)
            glEnd()

# Draw floating balls
def draw_floating_balls():
    glColor3f(1.0, 1.0, 0.0)
    for ball in floating_balls:
        if not ball["hit"]:
            draw_circle_midpoint(ball["x"], ball["y"], 20)

# Draw walls using midpoint line algorithm
def draw_walls():
    def draw_line_midpoint(x0, y0, x1, y1):
        dx = x1 - x0
        dy = y1 - y0
        d = 2 * dy - dx
        x, y = x0, y0

        glBegin(GL_POINTS)
        while x <= x1:
            glVertex2f(x, y)
            x += 1
            if d < 0:
                d += 2 * dy
            else:
                y += 1
                d += 2 * (dy - dx)
        glEnd()

    glColor3f(1.0, 1.0, 1.0)
    draw_line_midpoint(50, 50, WINDOW_WIDTH - 50, 50)
    draw_line_midpoint(50, WINDOW_HEIGHT - 50, WINDOW_WIDTH - 50, WINDOW_HEIGHT - 50)
    draw_line_midpoint(50, 50, 50, WINDOW_HEIGHT - 50)
    draw_line_midpoint(WINDOW_WIDTH - 50, 50, WINDOW_WIDTH - 50, WINDOW_HEIGHT - 50)

# Draw power-ups
def draw_power_ups():
    for power_up in active_power_ups:
        if power_up["active"]:
            if power_up["type"] == "extra_life":
                glColor3f(0.0, 0.0, 1.0)  # Blue for extra life
            elif power_up["type"] == "wide_paddle":
                glColor3f(0.0, 1.0, 0.0)  # Green for wide paddle
            draw_circle_midpoint(power_up["x"], power_up["y"], 10)

# Update ball physics
def update_ball():
    global ball_x, ball_y, ball_dx, ball_dy, score, lives, game_over, high_score
    global PAD_WIDTH

    ball_dy -= GRAVITY
    ball_x += ball_dx
    ball_y += ball_dy

    # Wall collisions
    if ball_x - BALL_RADIUS < 50 or ball_x + BALL_RADIUS > WINDOW_WIDTH - 50:
        ball_dx = -ball_dx
    if ball_y + BALL_RADIUS > WINDOW_HEIGHT - 50:
        ball_dy = -ball_dy

    # Paddle collision
    if pad_y <= ball_y - BALL_RADIUS <= pad_y + PAD_HEIGHT and pad_x <= ball_x <= pad_x + PAD_WIDTH:
        ball_dy = BOUNCE_STRENGTH
        score += 10

    # Power-up collision
    for power_up in active_power_ups:
        if power_up["active"] and (power_up["x"] - 10 <= ball_x <= power_up["x"] + 10) and (power_up["y"] - 10 <= ball_y <= power_up["y"] + 10):
            power_up["active"] = False
            if power_up["type"] == "extra_life":
                lives += 1
            elif power_up["type"] == "wide_paddle":
                PAD_WIDTH += 50

    # Floating ball collision
    for ball in floating_balls:
        if not ball["hit"] and (ball["x"] - 20 <= ball_x <= ball["x"] + 20) and (ball["y"] - 20 <= ball_y <= ball["y"] + 20):
            ball["hit"] = True
            ball_dy = -ball_dy
            score += 20

    # Ball falls below screen
    if ball_y < 0:
        lives -= 1
        if lives <= 0:
            game_over = True
            high_score = max(high_score, score)
        else:
            ball_x, ball_y = 400, 300
            ball_dx, ball_dy = 3.0, -3.0

# Display callback
def display():
    glClear(GL_COLOR_BUFFER_BIT)
    draw_ball()
    draw_pad()
    draw_walls()
    draw_power_ups()
    draw_floating_balls()

    # Display score and lives
    glColor3f(1.0, 1.0, 1.0)
    glRasterPos2f(10, WINDOW_HEIGHT - 20)
    for char in f"Score: {score}  Lives: {lives}  High Score: {high_score}":
        glutBitmapCharacter(GLUT_BITMAP_9_BY_15, ord(char))

    if game_over:
        glColor3f(1.0, 0.0, 0.0)
        glRasterPos2f(350, 400)
        for char in "Game Over!":
            glutBitmapCharacter(GLUT_BITMAP_9_BY_15, ord(char))

        glColor3f(0.0, 1.0, 0.0)
        glRasterPos2f(370, 270)
        for char in "Press 'V' to Restart":
            glutBitmapCharacter(GLUT_BITMAP_9_BY_15, ord(char))

    glFlush()

# Reset the game
def reset_game():
    global score, lives, ball_x, ball_y, ball_dx, ball_dy, pad_x, game_over, PAD_WIDTH, active_power_ups, floating_balls
    score = 0
    lives = 3
    ball_x, ball_y = 400, 300
    ball_dx, ball_dy = 3.0, -3.0
    pad_x = 350
    PAD_WIDTH = 100
    game_over = False

    # Reset power-ups
    for power_up in active_power_ups:
        power_up["x"] = random.randint(100, 700)
        power_up["y"] = random.randint(200, 500)
        power_up["active"] = True

    # Reset floating balls
    for ball in floating_balls:
        ball["hit"] = False

# Timer callback
def timer(value):
    if not game_over:
        update_ball()
    glutPostRedisplay()
    glutTimerFunc(16, timer, 0)

# Handle user input
def handle_input(key, x, y):
    global pad_x
    if key == b'a' or key == b'A':
        pad_x = max(50, pad_x - 20)
    elif key == b'd' or key == b'D':
        pad_x = min(WINDOW_WIDTH - PAD_WIDTH - 50, pad_x + 20)
    elif key == b'v' or key == b'V':
        if game_over:
            reset_game()

# Main function
def main():
    glutInit()
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    glutCreateWindow(b"Pinball Game with Power-Ups, Floating Balls, and High Score")
    glClearColor(0.0, 0.0, 0.0, 1.0)
    gluOrtho2D(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT)
    glutDisplayFunc(display)
    glutKeyboardFunc(handle_input)
    glutTimerFunc(16, timer, 0)
    glutMainLoop()

if __name__ == "__main__":
    main()