from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import math

# Camera control 
cam_angle = 5
cam_height = 5.0
radius = 5.0  
ball_state = 'ready'  # 'ready', 'moving'
ball_target = [0, 0, -15]
ball_pos = [0, 0.2, -5.3]
score = 0




def draw_ground():
    # ground
    glColor3f(0.0, 0.6, 0.0)  
    glBegin(GL_QUADS)
    glVertex3f(-10, 0, -20)
    glVertex3f(10, 0, -20)
    glVertex3f(10, 0, 10)
    glVertex3f(-10, 0, 10)
    glEnd()

    # Dsemi circle 
    glColor3f(1, 1, 1)  # White for markings
    glBegin(GL_LINE_STRIP)
    for i in range(0, 181, 5):  # Draw semi-circle with finer steps
        angle_rad = math.radians(i)
        x = math.cos(angle_rad) * 2
        z = math.sin(angle_rad) * 2 - 4  # Shift arc back
        glVertex3f(x, 0.01, z)
    glEnd()


    # penalty spot
    glPushMatrix()
    glColor3f(1, 1, 1)  # White for penalty spot
    glTranslatef(0, 0.01, -5.3)  # Slightly above ground to avoid z-fighting
    glScalef(0.2, 0.2, 0.2)  # Scale down to make it small
    draw_cube()
    glPopMatrix()

    # Dbox
    glBegin(GL_LINE_LOOP)
    glVertex3f(-7, 0.01, -20)
    glVertex3f(7, 0.01, -20)
    glVertex3f(7, 0.01, -4)
    glVertex3f(-7, 0.01, -4)
    glEnd()
    
    # Little box
    glBegin(GL_LINE_LOOP)
    glVertex3f(-5, 0.01, -10)
    glVertex3f(5, 0.01, -10)
    glVertex3f(5, 0.01, -20)
    glVertex3f(-5, 0.01, -20)
    glEnd()

   
def draw_goalkeeper():
    glPushMatrix()
    glTranslatef(0, 0, -12)  # new
  # goalkeeper position

    
    glColor3f(0.9, 0.1, 0.1) 
    glPushMatrix()
    glTranslatef(0, 1.2, 0)
    glScalef(0.6, 1.2, 0.3)
    draw_cube()
    glPopMatrix()

    # Head
    glColor3f(1.0, 0.8, 0.6)  
    glPushMatrix()
    glTranslatef(0, 2.2, 0)
    glutSolidSphere(0.25, 16, 16)
    glPopMatrix()

    # Arms
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

    # Legs
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

    
    # back bar
    draw_bar(-half_width, goal_height / 2, front_z, post_thickness, goal_height, post_thickness)
    draw_bar(half_width, goal_height / 2, front_z, post_thickness, goal_height, post_thickness)

    # Upper bar
    draw_bar(0, goal_height, front_z, goal_width, post_thickness, post_thickness)

    # Bottom front bar
    draw_bar(0, 0, front_z, goal_width, post_thickness, 0.05)

    # front bar 
    draw_bar(-half_width, goal_height / 2, back_z, post_thickness, goal_height, post_thickness)
    draw_bar(half_width, goal_height / 2, back_z, post_thickness, goal_height, post_thickness)

    # roof
    draw_bar(0, goal_height, back_z, goal_width, post_thickness, post_thickness)
    

    # Side roof beams
    draw_bar(-half_width, goal_height, (front_z + back_z) / 2, post_thickness, post_thickness, goal_depth)
    draw_bar(half_width, goal_height, (front_z + back_z) / 2, post_thickness, post_thickness, goal_depth)
    # --- Net Colors ---
    glColor3f(0.8, 0.8, 0.8)
    net_div = 10

    glBegin(GL_LINES)

    #net
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
        # --- Left side net ---
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
    # Front
    glVertex3f(-0.5, -0.5, 0.5)
    glVertex3f(0.5, -0.5, 0.5)
    glVertex3f(0.5, 0.5, 0.5)
    glVertex3f(-0.5, 0.5, 0.5)
    # Back
    glVertex3f(-0.5, -0.5, -0.5)
    glVertex3f(-0.5, 0.5, -0.5)
    glVertex3f(0.5, 0.5, -0.5)
    glVertex3f(0.5, -0.5, -0.5)
    # Left
    glVertex3f(-0.5, -0.5, -0.5)
    glVertex3f(-0.5, -0.5, 0.5)
    glVertex3f(-0.5, 0.5, 0.5)
    glVertex3f(-0.5, 0.5, -0.5)
    # Right
    glVertex3f(0.5, -0.5, -0.5)
    glVertex3f(0.5, 0.5, -0.5)
    glVertex3f(0.5, 0.5, 0.5)
    glVertex3f(0.5, -0.5, 0.5)
    # Top
    glVertex3f(-0.5, 0.5, -0.5)
    glVertex3f(-0.5, 0.5, 0.5)
    glVertex3f(0.5, 0.5, 0.5)
    glVertex3f(0.5, 0.5, -0.5)
    # Bottom
    glVertex3f(-0.5, -0.5, -0.5)
    glVertex3f(0.5, -0.5, -0.5)
    glVertex3f(0.5, -0.5, 0.5)
    glVertex3f(-0.5, -0.5, 0.5)
    glEnd()
    #balls
def draw_ball():
    glColor3f(1.0, 1.0, 1.0)
    glPushMatrix()
    glTranslatef(ball_pos[0], ball_pos[1], ball_pos[2])
    glutSolidSphere(0.2, 20, 20)
    glPopMatrix()
def keyboard(key, x, y):
    global ball_state, ball_target
    if ball_state != 'ready':
        return

    key = key.decode('utf-8')

    if key == 'a':  # Bottom left corner
        ball_target = [-2.99, 0.5, -14.5]
    elif key == 'd':  # Bottom right corner
        ball_target = [2.99, 0.5, -14.5]
    elif key == 'w':  # Top right corner
        ball_target = [2.99, 3, -14.5]
    elif key == 's':  # Top left corner
        ball_target = [-2.99, 3, -14.5]
    else:
        return

    ball_state = 'moving'
    glutIdleFunc(update_ball)


def update_ball():
    global ball_pos, ball_target, ball_state, score

    speed = 0.2
    for i in range(3):
        diff = ball_target[i] - ball_pos[i]
        if abs(diff) > speed:
            ball_pos[i] += speed if diff > 0 else -speed
        else:
            ball_pos[i] = ball_target[i]

    if ball_pos == ball_target:
        ball_state = 'ready'
        score += 1
        print("GOAL! Score:", score)
        reset_ball()
        glutIdleFunc(None)  # Stop animation

    glutPostRedisplay()
def reset_ball():
    global ball_pos
    ball_pos = [0, 0.2, -5.3]




def display():
    global cam_angle, cam_height, radius
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    cam_x = radius * math.sin(math.radians(cam_angle))
    cam_z = radius * math.cos(math.radians(cam_angle))
    gluLookAt(cam_x, cam_height, cam_z, 0, 0, -10, 0, 1, 0)

    draw_ground()
    draw_ball()
    draw_goalkeeper()
    draw_goal_post()

    glutSwapBuffers()

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


# Initialize
glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
glutInitWindowSize(900, 700)
glutCreateWindow(b"Penalty Shooter")
init()
glutDisplayFunc(display)
glutReshapeFunc(reshape)
glutSpecialFunc(special_keys)
glutKeyboardFunc(keyboard)


glutMainLoop()
