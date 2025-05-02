from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *  # Import all GLUT functions and constants
from OpenGL.GLUT.fonts import GLUT_BITMAP_HELVETICA_18  # Explicitly import the font
import math


# Game state
cam_angle = 5
cam_height = 5.0
radius = 5.0  
ball_state = 'ready'  # 'ready', 'moving'
ball_target = [0, 0, -15]
ball_pos = [0, 0.2, -5.3]
goalkeeper_pos = [0, 0, -12]
goalkeeper_target = [0, 0, -12]
goalkeeper_state = 'ready'  # 'ready', 'moving'
player1_score = 0
player2_score = 0
current_turn = 'player1_shoot'  # 'player1_shoot', 'player2_shoot'
shots_taken = {'player1': 0, 'player2': 0}
max_shots_per_player = 5
game_state = 'normal'  # 'normal', 'sudden_death', 'ended'
winner = None
game_paused = False
status_message = ""

def draw_ground():
    glColor3f(0.0, 0.6, 0.0)  
    glBegin(GL_QUADS)
    glVertex3f(-10, 0, -20)
    glVertex3f(10, 0, -20)
    glVertex3f(10, 0, 10)
    glVertex3f(-10, 0, 10)
    glEnd()

    glColor3f(1, 1, 1)
    glBegin(GL_LINE_STRIP)
    for i in range(0, 181, 5):
        angle_rad = math.radians(i)
        x = math.cos(angle_rad) * 2
        z = math.sin(angle_rad) * 2 - 4
        glVertex3f(x, 0.01, z)
    glEnd()

    glPushMatrix()
    glColor3f(1, 1, 1)
    glTranslatef(0, 0.01, -5.3)
    glScalef(0.2, 0.2, 0.2)
    draw_cube()
    glPopMatrix()

    glBegin(GL_LINE_LOOP)
    glVertex3f(-7, 0.01, -20)
    glVertex3f(7, 0.01, -20)
    glVertex3f(7, 0.01, -4)
    glVertex3f(-7, 0.01, -4)
    glEnd()
    
    glBegin(GL_LINE_LOOP)
    glVertex3f(-5, 0.01, -10)
    glVertex3f(5, 0.01, -10)
    glVertex3f(5, 0.01, -20)
    glVertex3f(-5, 0.01, -20)
    glEnd()

def draw_goalkeeper():
    glPushMatrix()
    glTranslatef(goalkeeper_pos[0], goalkeeper_pos[1], goalkeeper_pos[2])
    
    glColor3f(0.9, 0.1, 0.1)
    glPushMatrix()
    glTranslatef(0, 1.2, 0)
    glScalef(0.6, 1.2, 0.3)
    draw_cube()
    glPopMatrix()

    glColor3f(1.0, 0.8, 0.6)
    glPushMatrix()
    glTranslatef(0, 2.2, 0)
    glutSolidSphere(0.25, 16, 16)
    glPopMatrix()

    glColor3f(0.9, 0.1, 0.1)
    glPushMatrix()
    glTranslatef(-0.5, 1.2, 0)
    glScalef(0.2, 1.0, 0.2)
    draw_cube()
    glPopMatrix()

    glPushMatrix()
    glTranslatef(0.5, 1.2, 0)
    glScalef(0.2, 1.0, 0.2)
    draw_cube()
    glPopMatrix()

    glColor3f(0.1, 0.1, 0.9)
    glPushMatrix()
    glTranslatef(-0.2, 0.3, 0)
    glScalef(0.2, 0.6, 0.2)
    draw_cube()
    glPopMatrix()

    glPushMatrix()
    glTranslatef(0.2, 0.3, 0)
    glScalef(0.2, 0.6, 0.2)
    draw_cube()
    glPopMatrix()

    glPopMatrix()

def draw_shooter():
    glPushMatrix()
    glTranslatef(0, 0, -5.3)
    
    glColor3f(0.1, 0.9, 0.1)
    glPushMatrix()
    glTranslatef(0, 1.2, 0)
    glScalef(0.6, 1.2, 0.3)
    draw_cube()
    glPopMatrix()

    glColor3f(1.0, 0.8, 0.6)
    glPushMatrix()
    glTranslatef(0, 2.2, 0)
    glutSolidSphere(0.25, 16, 16)
    glPopMatrix()

    glColor3f(0.1, 0.9, 0.1)
    glPushMatrix()
    glTranslatef(-0.5, 1.2, 0)
    glScalef(0.2, 1.0, 0.2)
    draw_cube()
    glPopMatrix()

    glPushMatrix()
    glTranslatef(0.5, 1.2, 0)
    glScalef(0.2, 1.0, 0.2)
    draw_cube()
    glPopMatrix()

    glColor3f(0.1, 0.1, 0.1)
    glPushMatrix()
    glTranslatef(-0.2, 0.3, 0)
    glScalef(0.2, 0.6, 0.2)
    draw_cube()
    glPopMatrix()

    glPushMatrix()
    glTranslatef(0.2, 0.3, 0)
    glScalef(0.2, 0.6, 0.2)
    draw_cube()
    glPopMatrix()

    glPopMatrix()

def draw_goal_post():
    glColor3f(1, 1, 1)
    goal_width = 8.0
    goal_height = 4.0
    goal_depth = 2.0
    post_thickness = 0.1

    def draw_bar(x, y, z, sx, sy, sz):
        glPushMatrix()
        glTranslatef(x, y, z)
        glScalef(sx, sy, sz)
        draw_cube()
        glPopMatrix()

    half_width = goal_width / 2
    front_z = -15
    back_z = front_z + goal_depth
    
    draw_bar(-half_width, goal_height / 2, front_z, post_thickness, goal_height, post_thickness)
    draw_bar(half_width, goal_height / 2, front_z, post_thickness, goal_height, post_thickness)
    draw_bar(0, goal_height, front_z, goal_width, post_thickness, post_thickness)
    draw_bar(0, 0, front_z, goal_width, post_thickness, 0.05)
    draw_bar(-half_width, goal_height / 2, back_z, post_thickness, goal_height, post_thickness)
    draw_bar(half_width, goal_height / 2, back_z, post_thickness, goal_height, post_thickness)
    draw_bar(0, goal_height, back_z, goal_width, post_thickness, post_thickness)
    draw_bar(-half_width, goal_height, (front_z + back_z) / 2, post_thickness, post_thickness, goal_depth)
    draw_bar(half_width, goal_height, (front_z + back_z) / 2, post_thickness, post_thickness, goal_depth)
    
    glColor3f(0.8, 0.8, 0.8)
    net_div = 10
    glBegin(GL_LINES)
    for i in range(net_div + 1):
        x = -half_width + i * (goal_width / net_div)
        glVertex3f(x, 0, front_z)
        glVertex3f(x, goal_height, front_z)
    for j in range(net_div + 1):
        y = j * (goal_height / net_div)
        glVertex3f(-half_width, y, front_z)
        glVertex3f(half_width, y, front_z)
    
    for i in range(net_div + 1):
        x = -half_width + i * (goal_width / net_div)
        glVertex3f(x, goal_height, front_z)
        glVertex3f(x, goal_height, back_z)
    for j in range(net_div + 1):
        z = front_z + j * (goal_depth / net_div)
        glVertex3f(-half_width, goal_height, z)
        glVertex3f(half_width, goal_height, z)
    
    for i in range(net_div + 1):
        y = i * (goal_height / net_div)
        glVertex3f(-half_width, y, front_z)
        glVertex3f(-half_width, y, back_z)
    for j in range(net_div + 1):
        z = front_z + j * (goal_depth / net_div)
        glVertex3f(-half_width, 0, z)
        glVertex3f(-half_width, goal_height, z)
    
    for i in range(net_div + 1):
        y = i * (goal_height / net_div)
        glVertex3f(half_width, y, front_z)
        glVertex3f(half_width, y, back_z)
    for j in range(net_div + 1):
        z = front_z + j * (goal_depth / net_div)
        glVertex3f(half_width, 0, z)
        glVertex3f(half_width, goal_height, z)
    glEnd()

def draw_cube():
    glBegin(GL_QUADS)
    glVertex3f(-0.5, -0.5, 0.5)
    glVertex3f(0.5, -0.5, 0.5)
    glVertex3f(0.5, 0.5, 0.5)
    glVertex3f(-0.5, 0.5, 0.5)
    glVertex3f(-0.5, -0.5, -0.5)
    glVertex3f(-0.5, 0.5, -0.5)
    glVertex3f(0.5, 0.5, -0.5)
    glVertex3f(0.5, -0.5, -0.5)
    glVertex3f(-0.5, -0.5, -0.5)
    glVertex3f(-0.5, -0.5, 0.5)
    glVertex3f(-0.5, 0.5, 0.5)
    glVertex3f(-0.5, 0.5, -0.5)
    glVertex3f(0.5, -0.5, -0.5)
    glVertex3f(0.5, 0.5, -0.5)
    glVertex3f(0.5, 0.5, 0.5)
    glVertex3f(0.5, -0.5, 0.5)
    glVertex3f(-0.5, 0.5, -0.5)
    glVertex3f(-0.5, 0.5, 0.5)
    glVertex3f(0.5, 0.5, 0.5)
    glVertex3f(0.5, 0.5, -0.5)
    glVertex3f(-0.5, -0.5, -0.5)
    glVertex3f(0.5, -0.5, -0.5)
    glVertex3f(0.5, -0.5, 0.5)
    glVertex3f(-0.5, -0.5, 0.5)
    glEnd()

def draw_ball():
    glColor3f(1.0, 1.0, 1.0)
    glPushMatrix()
    glTranslatef(ball_pos[0], ball_pos[1], ball_pos[2])
    glutSolidSphere(0.2, 20, 20)
    glPopMatrix()

def keyboard(key, x, y):
    global ball_state, ball_target, goalkeeper_state, goalkeeper_target, current_turn
    global game_state, game_paused, status_message

    key = key.decode('utf-8')

    # ---- Game control keys ----
    if key == 'p':  # Pause the game
        game_paused = True
        status_message = "Paused"
        print("[Game Paused]")
        return

    elif key == ' ':  # Play/Resume the game
        game_paused = False
        status_message = ""
        print("[Game Resumed]")
        return

    # If game is paused or ended, skip actions
    if game_paused or game_state == 'ended':
        return

    # ---- Player 1 shooter ----
    if current_turn == 'player1_shoot' and key in ['w', 'a', 's', 'd'] and ball_state == 'ready':
        if key == 'a': ball_target = [-2.99, 0.5, -14.5]
        elif key == 'd': ball_target = [2.99, 0.5, -14.5]
        elif key == 'w': ball_target = [2.99, 3, -14.5]
        elif key == 's': ball_target = [-2.99, 3, -14.5]
        ball_state = 'moving'
        glutIdleFunc(update_ball)

    # ---- Player 2 goalkeeper ----
    elif current_turn == 'player2_shoot' and key in ['w', 'a', 's', 'd'] and goalkeeper_state == 'ready':
        if key == 'a': goalkeeper_target = [-2.5, 0, -12]
        elif key == 'd': goalkeeper_target = [2.5, 0, -12]
        elif key == 'w': goalkeeper_target = [2.99, 2.0, -12]
        elif key == 's': goalkeeper_target = [-2.99, 2.0, -12]
        goalkeeper_state = 'moving'
        glutIdleFunc(update_goalkeeper)

    # ---- Player 2 shooter ----
    elif current_turn == 'player2_shoot' and key in ['i', 'j', 'k', 'l'] and ball_state == 'ready':
        if key == 'j': ball_target = [-2.99, 0.5, -14.5]
        elif key == 'l': ball_target = [2.99, 0.5, -14.5]
        elif key == 'i': ball_target = [2.99, 3, -14.5]
        elif key == 'k': ball_target = [-2.99, 3, -14.5]
        ball_state = 'moving'
        glutIdleFunc(update_ball)

    # ---- Player 1 goalkeeper ----
    elif current_turn == 'player1_shoot' and key in ['i', 'j', 'k', 'l'] and goalkeeper_state == 'ready':
        if key == 'j': goalkeeper_target = [-2.5, 0, -12]
        elif key == 'l': goalkeeper_target = [2.5, 0, -12]
        elif key == 'i': goalkeeper_target = [2.99, 2.0, -12]
        elif key == 'k': goalkeeper_target = [-2.99, 2.0, -12]
        goalkeeper_state = 'moving'
        glutIdleFunc(update_goalkeeper)


def update_ball():
    global ball_pos, ball_target, ball_state, player1_score, player2_score
    global current_turn, shots_taken, game_state, winner
    speed = 0.2
    for i in range(3):
        diff = ball_target[i] - ball_pos[i]
        if abs(diff) > speed:
            ball_pos[i] += speed if diff > 0 else -speed
        else:
            ball_pos[i] = ball_target[i]

    # Improved Collision Detection
    ball_radius = 0.2
    goalkeeper_width = 0.6
    goalkeeper_height = 1.2
    goalkeeper_depth = 0.3

    # Check collision with goalkeeper (bounding box with margin for ball radius)
    if (goalkeeper_pos[0] - goalkeeper_width / 2 - ball_radius <= ball_pos[0] <= goalkeeper_pos[0] + goalkeeper_width / 2 + ball_radius and
        goalkeeper_pos[1] - ball_radius <= ball_pos[1] <= goalkeeper_pos[1] + goalkeeper_height + ball_radius and
        goalkeeper_pos[2] - goalkeeper_depth / 2 - ball_radius <= ball_pos[2] <= goalkeeper_pos[2] + goalkeeper_depth / 2 + ball_radius):
        ball_state = 'ready'
        print(f"SAVED!\nPlayer 1: {player1_score}\nPlayer 2: {player2_score}")
        end_turn()
        glutIdleFunc(None)
        return

    # Check if ball reached the target (within a small threshold)
    if all(abs(ball_pos[i] - ball_target[i]) < speed for i in range(3)):
        ball_state = 'ready'
        if current_turn == 'player1_shoot':
            player1_score += 1
        else:
            player2_score += 1
        print(f"GOAALL!\nPlayer 1: {player1_score}\nPlayer 2: {player2_score}")
        end_turn()
        glutIdleFunc(None)

    glutPostRedisplay()

def update_goalkeeper():
    global goalkeeper_pos, goalkeeper_target, goalkeeper_state
    speed = 0.2
    for i in range(3):
        diff = goalkeeper_target[i] - goalkeeper_pos[i]
        if abs(diff) > speed:
            goalkeeper_pos[i] += speed if diff > 0 else -speed
        else:
            goalkeeper_pos[i] = goalkeeper_target[i]

    if goalkeeper_pos == goalkeeper_target:
        goalkeeper_state = 'ready'
        glutIdleFunc(None)

    glutPostRedisplay()

def end_turn():
    global current_turn, shots_taken, game_state, winner
    if current_turn == 'player1_shoot':
        shots_taken['player1'] += 1
        current_turn = 'player2_shoot'
    else:
        shots_taken['player2'] += 1
        current_turn = 'player1_shoot'

    if shots_taken['player1'] >= max_shots_per_player and shots_taken['player2'] >= max_shots_per_player:
        if player1_score > player2_score:
            winner = 'Player 1'
            game_state = 'ended'
            print(f"Game Over! {winner} wins with {player1_score} goals to {player2_score}")
        elif player2_score > player1_score:
            winner = 'Player 2'
            game_state = 'ended'
            print(f"Game Over! {winner} wins with {player2_score} goals to {player1_score}")
        else:
            game_state = 'sudden_death'
            print("Sudden Death! Next goal wins if opponent misses.")

    # sudden death
    elif game_state == 'sudden_death' and shots_taken['player1'] == shots_taken['player2']:
        if player1_score > player2_score:
            winner = 'Player 1'
            game_state = 'ended'
            print(f"Game Over! {winner} wins with {player1_score} goals to {player2_score}")
        elif player2_score > player1_score:
            winner = 'Player 2'
            game_state = 'ended'
            print(f"Game Over! {winner} wins with {player2_score} goals to {player1_score}")
        else:
            print("Sudden Death continues! Next goal wins if opponent misses.")

    reset_ball()
    reset_goalkeeper()
    print(f"Turn: {'Player 1 shoots' if current_turn == 'player1_shoot' else 'Player 2 shoots'}, "
          f"Shots taken: P1-{shots_taken['player1']}, P2-{shots_taken['player2']}, "
          f"Game state: {game_state}")

def reset_ball():
    global ball_pos
    ball_pos = [0, 0.2, -5.3]

def reset_goalkeeper():
    global goalkeeper_pos, goalkeeper_target, goalkeeper_state
    goalkeeper_pos = [0, 0, -12]
    goalkeeper_target = [0, 0, -12]
    goalkeeper_state = 'ready'

def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))


def display():
    global cam_angle, cam_height, radius

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # Set up 3D camera
    cam_x = radius * math.sin(math.radians(cam_angle))
    cam_z = radius * math.cos(math.radians(cam_angle))
    gluLookAt(cam_x, cam_height, cam_z, 0, 0, -10, 0, 1, 0)

    # Draw 3D elements
    draw_ground()
    draw_ball()
    draw_shooter()
    draw_goalkeeper()
    draw_goal_post()

    # --- Begin 2D Overlay ---
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, 800, 0, 600)  # Adjust if your window is different
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    glDisable(GL_DEPTH_TEST)  # Always on top

    # Draw scores
    glColor3f(1, 1, 1)  # White
    draw_text(10, 570, f"Player 1 Score: {player1_score}")
    draw_text(600, 570, f"Player 2 Score: {player2_score}")

    # Show pause message
    if game_paused:
        glColor3f(1, 1, 0)  # Yellow
        draw_text(340, 300, "Game Paused")

    # Show winner if game ended
    if game_state == 'ended':
        glColor3f(0, 1, 0)  # Green
        winner_text = "DRAW!"
        if winner == 'player1':
            winner_text = "PLAYER 1 WINS!"
        elif winner == 'player2':
            winner_text = "PLAYER 2 WINS!"
        draw_text(320, 320, winner_text)

    # Show help/instructions
    glColor3f(0.8, 0.8, 0.8)  # Light gray
    draw_text(10, 10, "P - Pause | SPACE - Play")

    # Cleanup
    glEnable(GL_DEPTH_TEST)
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    # --- End 2D Overlay ---

    glutSwapBuffers()
def draw_text(x, y, text):
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(ch))



def reshape(w, h):
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60, float(w)/float(h), 1.0, 100.0)
    glMatrixMode(GL_MODELVIEW)

def special_keys(key, x, y):
    global cam_angle, cam_height
    if key == GLUT_KEY_LEFT:
        cam_angle -= 5
    elif key == GLUT_KEY_RIGHT:
        cam_angle += 5
    elif key == GLUT_KEY_UP:
        cam_height += 0.5
    elif key == GLUT_KEY_DOWN:
        cam_height -= 0.5
    glutPostRedisplay()

def init():
    glClearColor(0.0, 0.4, 0.8, 1.0)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LINE_SMOOTH)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    light_pos = [0.0, 10.0, 0.0, 1.0]
    glLightfv(GL_LIGHT0, GL_POSITION, light_pos)
    glEnable(GL_COLOR_MATERIAL)

glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
glutInitWindowSize(900, 700)
glutCreateWindow(b"Penalty Shootout")
init()
glutDisplayFunc(display)
glutReshapeFunc(reshape)
glutSpecialFunc(special_keys)
glutKeyboardFunc(keyboard)
glutMainLoop()