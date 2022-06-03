import pygame, sys


class Ball: 

    def __init__(self,screen, color, px, py, radius):

        self._screen = screen
        self._color = color
        self._px = px
        self._py = py
        self._radius = radius
        self._dx = 0
        self._dy = 0
        self.display()

    def display(self):
        pygame.draw.circle(self._screen, self._color, (self._px, self._py), self._radius)


    def start_moving(self):
        self._dx = 0.15 
        self._dy = 0.050

    def move_ball(self):
        self._px += self._dx
        self._py += self._dy

    def collisions(self):
       self._dx = -self._dx

    def wall_collision(self):
        self._dy = -self._dy

    def reset_position(self):
        self._px = WIDTH/2 
        self._py = HEIGHT/2
        self._dx = 0
        self._dy = 0
        self.display()

class Paddle:

    def __init__(self, screen, color, px, py, width, height):

        self._screen = screen
        self._color = color
        self._px = px
        self._py = py
        self._width = width
        self._height = height

        self._action = "stopped"

        self.display()

    def display(self):

        pygame.draw.rect(self._screen, self._color, (self._px, self._py, self._width, self._height))

    def move_paddle(self):
        if self._action == "up":
            self._py -= 0.4
        elif self._action == "down":
            self._py += 0.4


    def clamp(self):
        if self._py <= 0:
            self._py = 0

        if self._py + self._height >= HEIGHT:
            self._py = HEIGHT - self._height

    def reset_paddles(self):
        self._py = HEIGHT/2 - self._height/2
        self._action = "stopped"
        self.display()

class ControlCollisions():
    def ball_and_paddleLeft(self, ball, paddleLeft):
        if ball._py + ball._radius > paddleLeft._py and ball._py - ball._radius < paddleLeft._py + paddleLeft._height:
            if ball._px - ball._radius <= paddleLeft._px + paddleLeft._width:
                return True
        return False

    def ball_and_paddleRight(self, ball, paddleRight):
        if ball._py + ball._radius > paddleRight._py and ball._py - ball._radius < paddleRight._py + paddleRight._height:
            if ball._px + ball._radius >= paddleRight._px:
                return True
        return False

    def ball_and_walls(self, ball):
        #top collsion
        if ball._py - ball._radius <= 0:
            return True
         
        #bottom collision 
        if ball._py + ball._radius >= HEIGHT:
            return True
        
        return False

    def check_paddleLeft_score(self, ball):
        return ball._px - ball._radius >= WIDTH

    def check_paddleRight_score(self, ball):
        return ball._px + ball._radius <= 0

class Score:
    def __init__(self, screen, points, px, py):
        self._screen = screen
        self._points = points 
        self._px = px
        self._py = py
        self._font = pygame.font.SysFont("inkfree", 60, bold= True)
        self._label = self._font.render(self._points, 0, WHITE)
        self.display()
    
    def display(self):
        self._screen.blit(self._label, (self._px - self._label.get_rect().width/2, self._py))

    def add_points(self):
        points = int(self._points) + 1
        self._points = str(points)
        self._label = self._font.render(self._points, 0, BLUE)

    def reset(self):
        self._points = "0"
        self._label = self._font.render(self._points, 0, WHITE)



pygame.init()

WIDTH= 700
HEIGHT= 450
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0,255,255)
YELLOW = (227,207,87)



screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PONG")


def make_screen():
    screen.fill((BLACK))
    pygame.draw.line(screen, WHITE, (WIDTH/2, 0), (WIDTH/2, HEIGHT), 5 )

def restart():
    make_screen()
    score1.reset()
    score2.reset()
    ball.reset_position()
    paddleLeft.reset_paddles()
    paddleRight.reset_paddles()

make_screen()


ball = Ball(screen, BLUE, WIDTH/2, HEIGHT/2, 15 )
paddleLeft = Paddle(screen, YELLOW, 15, HEIGHT/2 - 60, 20, 120)
paddleRight = Paddle(screen, YELLOW, WIDTH - 20 - 15, HEIGHT/2 - 60, 20, 120)
collision = ControlCollisions()
score1 = Score(screen, "0", WIDTH/4, 15)
score2 = Score(screen, "0", WIDTH - WIDTH/4, 15)



#Variables
playing = False


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                ball.start_moving()
                playing = True


            if event.key == pygame.K_a:
                restart()
                playing = False
    
            if event.key == pygame.K_w:
                paddleLeft._action = "up"
                
            if event.key == pygame.K_s:
                paddleLeft._action = "down"

            if event.key == pygame.K_UP:
                paddleRight._action = "up"
            if event.key == pygame.K_DOWN:
                paddleRight._action = "down"

        if event.type == pygame.KEYUP:
            paddleLeft._action = "stopped"
            paddleRight._action = "stopped"

    if playing: 
        #ball moves
        make_screen()
        ball.move_ball()
        ball.display()

        #left paddle
        paddleLeft.move_paddle()
        paddleLeft.clamp()
        paddleLeft.display()

        #right paddle
        paddleRight.move_paddle()
        paddleRight.clamp()
        paddleRight.display()

        #check collisions
        if collision.ball_and_paddleLeft(ball, paddleLeft):
            ball.collisions()

        if collision.ball_and_paddleRight(ball, paddleRight):
            ball.collisions()

        if collision.ball_and_walls(ball):
            ball.wall_collision()

        if collision.check_paddleLeft_score(ball):
            make_screen()
            score1.add_points()
            ball.reset_position()
            paddleLeft.reset_paddles()
            paddleRight.reset_paddles()
            playing = False

        if collision.check_paddleRight_score(ball):
            make_screen()
            score2.add_points()
            ball.reset_position()
            paddleRight.reset_paddles()
            paddleLeft.reset_paddles()
            playing = False

    #keep scoreboard
    score1.display()
    score2.display()



    pygame.display.update()
