from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

#fixed
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 700
BALL_RADIUS = 10
PAD_WIDTH = 100
PAD_HEIGHT = 10
GRAVITY = 0.05
BOUNCE_STRENGTH = 9.0
INITIAL_BALL_SPEED = 3.0
#ballpadscore
ball_x, ball_y = 400, 300
ball_dx, ball_dy = 3.0, -3.0
pad_x, pad_y = 350, 50 #p1
pad2_x, pad2_y = 350, 50  #p2
score, high_score, lives = 0, 0, 3 
game_over = False

active_power_ups = [
    {"x": 150, "y": 300, "type": "extra_life", "active": True},
    {"x": 250, "y": 600, "type": "wide_paddle", "active": True},
    {"x": 350, "y": 600, "type": "extra_life", "active": True},
    {"x": 450, "y": 500, "type": "wide_paddle", "active": True},
    {"x": 150, "y": 300, "type": "extra_life", "active": True},
    {"x": 250, "y": 400, "type": "wide_paddle", "active": True},
    {"x": 350, "y": 200, "type": "extra_life", "active": True},
    {"x": 450, "y": 500, "type": "wide_paddle", "active": True}
    #{"x": 600, "y": 300, "type": "larger_ball", "active": True}crash
]
floating_balls = [
    {"x": 200, "y": 400, "hit": False},
    {"x": 850, "y": 450, "hit": False},
    {"x": 300, "y": 500, "hit": False},
    {"x": 200, "y": 300, "hit": False},
    {"x": 150, "y": 450, "hit": False},
    {"x": 200, "y": 500, "hit": False},
    {"x": 450, "y": 450, "hit": False},
    {"x": 500, "y": 500, "hit": False},
    {"x": 400, "y": 400, "hit": False},
    {"x": 200, "y": 400, "hit": False},
    {"x": 450, "y": 450, "hit": False},
    {"x": 300, "y": 500, "hit": False},
    {"x": 200, "y": 300, "hit": False},
    {"x": 150, "y": 450, "hit": False},
    {"x": 200, "y": 500, "hit": False},
    {"x": 350, "y": 500, "hit": False},
    {"x": 450, "y": 350, "hit": False},
    {"x": 650, "y": 200, "hit": False},
    {"x": 450, "y": 600, "hit": False},
    {"x": 450, "y": 250, "hit": False},
    {"x": 550, "y": 500, "hit": False},
    {"x": 650, "y": 405, "hit": False},
    {"x": 600, "y": 450, "hit": False},
    {"x": 450, "y": 500, "hit": False},
    {"x": 600, "y": 450, "hit": False}
]

# Drawing Functions
def draw_circle_midpoint(cx, cy, radius): #mpc
    x, y = 0, radius #ini
    p = 1 - radius #d

    def plot_circle_points(cx, cy, x, y):
        points = [
            (cx + x, cy + y), (cx - x, cy + y),
            (cx + x, cy - y), (cx - x, cy - y),
            (cx + y, cy + x), (cx - y, cy + x),
            (cx + y, cy - x), (cx - y, cy - x)
        ]
        for px, py in points: #L
            glVertex2f(px, py)

    glBegin(GL_POINTS) #Startdp
    plot_circle_points(cx, cy, x, y)
    while x < y: #Loop
        x += 1
        if p < 0:
            p += 2 * x + 1
        else:
            y -= 1
            p += 2 * (x - y) + 1
        plot_circle_points(cx, cy, x, y)
    glEnd()

def draw_line_midpoint(x0, y0, x1, y1):
    dx, dy = abs(x1 - x0), abs(y1 - y0) # x vs y
    sx, sy = (1 if x0 < x1 else -1), (1 if y0 < y1 else -1) #direction
    err = dx - dy

    glBegin(GL_POINTS)
    while True:
        glVertex2f(x0, y0)
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * err
        if e2 > -dy: #hriz
            err -= dy
            x0 += sx
        if e2 < dx: #vert
            err += dx
            y0 += sy
    glEnd()
    
    
#IMPORTANT
def draw_pad():
    glColor3f(1.0, 0.0, 1.0)
    for x in range(pad_x, pad_x + PAD_WIDTH + 1):
        for y in range(pad_y, pad_y + PAD_HEIGHT + 1):
            glBegin(GL_POINTS)
            glVertex2f(x, y)
            glEnd()

def draw_pad2():
    glColor3f(0.0, 1.0, 0.0)  # Green color for second paddle
    for x in range(pad2_x, pad2_x + PAD_WIDTH + 1):
        for y in range(pad2_y, pad2_y + PAD_HEIGHT + 1):
            glBegin(GL_POINTS)
            glVertex2f(x, y)
            glEnd()

def draw_floating_balls():
    glColor3f(1.0, 1.0, 0.0)
    for ball in floating_balls:
        if not ball["hit"]:
            draw_circle_midpoint(ball["x"], ball["y"], 20)

def draw_walls():
    glColor3f(1.0, 1.0, 1.0)
    draw_line_midpoint(50, 50, WINDOW_WIDTH - 50, 50)
    draw_line_midpoint(50, WINDOW_HEIGHT - 50, WINDOW_WIDTH - 50, WINDOW_HEIGHT - 50)
    draw_line_midpoint(50, 50, 50, WINDOW_HEIGHT - 50)
    draw_line_midpoint(WINDOW_WIDTH - 50, 50, WINDOW_WIDTH - 50, WINDOW_HEIGHT - 50)

def draw_power_ups():
    for power_up in active_power_ups:
        if power_up["active"]:
            glColor3f(0.0, 0.0, 1.0) if power_up["type"] == "extra_life" else glColor3f(0.0, 1.0, 0.0)
            draw_circle_midpoint(power_up["x"], power_up["y"], 10)

def draw_pin():
    glColor3f(1.0, 0.0, 0.0)
    draw_circle_midpoint(ball_x, ball_y, BALL_RADIUS)
    draw_line_midpoint(ball_x, ball_y + BALL_RADIUS, ball_x, ball_y + BALL_RADIUS + 40)
    draw_line_midpoint(ball_x - 20, ball_y + BALL_RADIUS - 40, ball_x + 20, ball_y + BALL_RADIUS - 40)

# Physics and Logic
def update_ball():
    global ball_x, ball_y, ball_dx, ball_dy, score, lives, game_over, high_score, PAD_WIDTH

    ball_dy -= GRAVITY
    ball_x += ball_dx
    ball_y += ball_dy

    if ball_x - BALL_RADIUS < 50 or ball_x + BALL_RADIUS > WINDOW_WIDTH - 50:
        ball_dx = -ball_dx
    if ball_y + BALL_RADIUS > WINDOW_HEIGHT - 50:
        ball_dy = -ball_dy

    # Check collision with the top paddle
    if pad_y <= ball_y - BALL_RADIUS <= pad_y + PAD_HEIGHT and pad_x <= ball_x <= pad_x + PAD_WIDTH:
        ball_dy = BOUNCE_STRENGTH
        score += 10

    # Check collision with the bottom paddle (pad2)
    if pad2_y <= ball_y - BALL_RADIUS <= pad2_y + PAD_HEIGHT and pad2_x <= ball_x <= pad2_x + PAD_WIDTH:
        ball_dy = BOUNCE_STRENGTH  # Reverse direction
        score += 10

    # Power-ups and other floating balls logic...
    for power_up in active_power_ups:
        if power_up["active"] and (power_up["x"] - 10 <= ball_x <= power_up["x"] + 10) and (
                power_up["y"] - 10 <= ball_y <= power_up["y"] + 10):
            power_up["active"] = False
            if power_up["type"] == "extra_life":
                lives += 1
            elif power_up["type"] == "wide_paddle":
                PAD_WIDTH += 50
            #elif power_up["type"] == "larger_ball":
               # ball_radius += 5  # Increase ball size

    for ball in floating_balls:
        if not ball["hit"] and (ball["x"] - 20 <= ball_x <= ball["x"] + 20) and (
                ball["y"] - 20 <= ball_y <= ball["y"] + 20):
            ball["hit"] = True
            ball_dy = -ball_dy
            score += 20

    if ball_y < 0:
        lives -= 1
        if lives <= 0:
            game_over = True
            high_score = max(high_score, score)
        else:
            reset_ball()

def reset_ball():
    global ball_x, ball_y, ball_dx, ball_dy
    ball_x, ball_y = 400, 300
    ball_dx, ball_dy = 3.0, -3.0

def reset_game():
    global score, lives, game_over, PAD_WIDTH
    score, lives = 0, 3
    game_over = False
    PAD_WIDTH = 100
    reset_ball()
    for power_up in active_power_ups:
        power_up.update({"x": 150, "y": 300, "active": True})
    for ball in floating_balls:
        ball["hit"] = False

# Display and Input Handlers
def display():
    glClear(GL_COLOR_BUFFER_BIT)
    draw_pin()
    draw_pad()
    draw_pad2()  # Draw the second paddle
    draw_walls()
    draw_power_ups()
    draw_floating_balls()

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

def handle_input(key, x, y):
    global pad_x, pad2_x
    if key in [b'a', b'A']:  # Move left for top paddle
        pad_x = max(50, pad_x - 20)
    elif key in [b'd', b'D']:  # Move right for top paddle
        pad_x = min(WINDOW_WIDTH - PAD_WIDTH - 50, pad_x + 20)
    elif key in [b'j', b'J']:  # Move left for bottom paddle
        pad2_x = max(50, pad2_x - 20)
    elif key in [b'l', b'L']:  # Move right for bottom paddle
        pad2_x = min(WINDOW_WIDTH - PAD_WIDTH - 50, pad2_x + 20)
    elif key in [b'v', b'V'] and game_over:
        reset_game()

# Timer

def timer(value):
    if not game_over:
        update_ball()
    glutPostRedisplay()
    glutTimerFunc(16, timer, 0)

# Main Function
def main():
    glutInit()
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    glutCreateWindow(b"Pinball Game")
    glClearColor(0.0, 0.0, 0.0, 1.0)
    gluOrtho2D(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT)
    glutDisplayFunc(display)
    glutKeyboardFunc(handle_input)
    glutTimerFunc(16, timer, 0)
    glutMainLoop()

if __name__ == "__main__":
    main()
