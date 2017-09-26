"""Floyd Kots ~ github.com/floydkots"""
# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True
VEL = 3

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    horizontal = random.randrange(120, 140) / 60
    vertical = random.randrange(60, 180) / 60
    if (direction == RIGHT):
        ball_vel = [horizontal, vertical]
    else:
        ball_vel = [-horizontal, vertical]
    


# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    spawn_ball(RIGHT)
    score1 = 0
    score2 = 0
    paddle1_vel = 0
    paddle2_vel = 0
    paddle1_pos = [[HALF_PAD_WIDTH, HEIGHT / 2 - HALF_PAD_HEIGHT],
                   [HALF_PAD_WIDTH, HEIGHT / 2 + HALF_PAD_HEIGHT]]
    paddle2_pos = [[WIDTH - HALF_PAD_WIDTH, HEIGHT / 2 - HALF_PAD_HEIGHT],
                   [WIDTH - HALF_PAD_WIDTH, HEIGHT / 2 + HALF_PAD_HEIGHT]]

def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
 
        
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += - ball_vel[1]
    
    # bouncing off the top or bottom walls
    if ((ball_pos[1] - BALL_RADIUS <= 0) or 
    (ball_pos[1] + BALL_RADIUS >= HEIGHT)):
        ball_vel[1] = - ball_vel[1] 
        
    # collision with left or right gutters
    if (ball_pos[0] - BALL_RADIUS <= PAD_WIDTH): # left gutter
        if (paddle1_pos[0][1] <= ball_pos[1] <= paddle1_pos[1][1]):
            ball_vel[0] = - ball_vel[0]
            ball_vel[0] *= 1.1
            ball_vel[1] *= 1.1
        else:
            score2 += 1
            spawn_ball(RIGHT)
        
    if (ball_pos[0] + BALL_RADIUS >= WIDTH - PAD_WIDTH): # right gutter
        if (paddle2_pos[0][1] <= ball_pos[1] <= paddle2_pos[1][1]):
            ball_vel[0] = - ball_vel[0]
            ball_vel[0] *= 1.1
            ball_vel[1] *= 1.1
        else:
            score1 += 1
            spawn_ball(LEFT)
        
    
            
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 1, "White", "White")
    
    # update paddle's vertical position, keep paddle on the screen
    if ((paddle1_pos[0][1] + paddle1_vel > 0) and 
    (paddle1_pos[1][1] + paddle1_vel < HEIGHT)):
        paddle1_pos[0][1] += paddle1_vel
        paddle1_pos[1][1] += paddle1_vel
        
    if ((paddle2_pos[0][1] + paddle2_vel > 0) and 
    (paddle2_pos[1][1] + paddle2_vel < HEIGHT)):
        paddle2_pos[0][1] += paddle2_vel
        paddle2_pos[1][1] += paddle2_vel
    
    # draw paddles
    canvas.draw_line(paddle1_pos[0], paddle1_pos[1], PAD_WIDTH, "White")
    canvas.draw_line(paddle2_pos[0], paddle2_pos[1], PAD_WIDTH, "White")
    
    # determine whether paddle and ball collide  
    
    
    # draw scores
    canvas.draw_text(str(score1), [WIDTH / 10, HEIGHT / 10], 50, "Green")
    canvas.draw_text(str(score2), [9 * WIDTH / 10, HEIGHT / 10], 50, "Green")
        
def keydown(key):
    global paddle1_vel, paddle2_vel
    if (key == simplegui.KEY_MAP['w']):
        paddle1_vel = -VEL
    if (key == simplegui.KEY_MAP['s']):
        paddle1_vel = VEL
    if (key == simplegui.KEY_MAP['up']):
        paddle2_vel = -VEL
    if (key == simplegui.KEY_MAP['down']):
        paddle2_vel = VEL
   
def keyup(key):
    global paddle1_vel, paddle2_vel
    
    if ((key == simplegui.KEY_MAP['w']) or
    (key == simplegui.KEY_MAP['s'])):
        paddle1_vel = 0

    if ((key == simplegui.KEY_MAP['up']) or 
    (key == simplegui.KEY_MAP['down'])):
        paddle2_vel = 0


# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("Restart", new_game, 100)


# start frame
new_game()
frame.start()
