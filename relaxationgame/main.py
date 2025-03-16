import pygame
import random

pygame.init()
pygame.mixer.init()

pygame.mixer.music.load("relaxationgame\\ambient.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

sw = 300
sh = 500

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BG_COLOR = (213, 229, 213)
GRID = (95, 192, 174)
WIN = (173, 178, 212)
LOSE = (235, 198, 195)
TEXT = (102, 108, 183)

font = pygame.font.SysFont("verdana", 50)
font2 = pygame.font.SysFont("verdana", 15)

win = pygame.display.set_mode((sw, sh), pygame.NOFRAME)
pygame.display.set_caption("Breakout")

brickHitSound = pygame.mixer.Sound("relaxationgame\hit.wav")
brickHitSound.set_volume(.1)
bounceSound = pygame.mixer.Sound("relaxationgame\hitGameSound.wav")
bounceSound.set_volume(.2)

clock = pygame.time.Clock()
gameover = False
victory = False

class Paddle(object):
    def __init__(self, x, y, w, h, color):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = color

    def draw(self, win):
        pygame.draw.rect(win, self.color, [self.x, self.y, self.w, self.h])

class Ball(object):
    def __init__(self, x, y, w, h, color):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = color
        self.xv = random.choice([2, 3, 4, -2, -3, -4])
        self.yv = random.randint(3, 4)

    def draw(self, win):
        pygame.draw.rect(win, self.color, [self.x, self.y, self.w, self.h])

    def move(self):
        self.x += self.xv
        self.y += self.yv

class Brick(object):
    def __init__(self, x, y, w, h, color):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = color
        self.visible = True
        self.pregnant = random.randint(0, 20) < 2  # Decreased chance

    def draw(self, win):
        pygame.draw.rect(win, self.color, [self.x, self.y, self.w, self.h])

bricks = []
def init():
    global bricks
    bricks = []
    for i in range(4):  # Reduce number of brick rows
        for j in range(5):  # Reduce number of brick columns
            bricks.append(Brick(10 + j * 58, 50 + i * 30, 50, 20, (95, 192, 174)))  # Adjusted brick size and positions

def lost_game():
    popup = pygame.Rect(50, 140, sw - 100, sh - 350)
    pygame.draw.rect(win, BLACK, popup)  # Changed popup background color
    pygame.draw.rect(win, LOSE, popup, 2)

    game_over = font2.render("TOUGH LUCK!", True, WHITE)  # Text in white for better visibility
    option1 = font2.render("Press r to restart", True, LOSE)
    option2 = font2.render("Press q to quit", True, LOSE)

    win.blit(game_over, (sw / 2 - game_over.get_width() / 2, 150))
    win.blit(option1, (sw / 2 - option1.get_width() / 2, 210))  # Moved up the option text
    win.blit(option2, (sw / 2 - option2.get_width() / 2, 250))  # Moved up the option text


def won_game():
    popup = pygame.Rect(50, 140, sw - 100, sh - 350)
    pygame.draw.rect(win, BLACK, popup)  # Changed popup background color
    pygame.draw.rect(win, WIN, popup, 2)

    game_over = font2.render("CONGRATS!", True, WHITE)  # Text in white for better visibility
    option1 = font2.render("Press r to restart", True, LOSE)
    option2 = font2.render("Press q to quit", True, LOSE)

    win.blit(game_over, (sw / 2 - game_over.get_width() / 2, 150))
    win.blit(option1, (sw / 2 - option1.get_width() / 2, 210))  # Moved up the option text
    win.blit(option2, (sw / 2 - option2.get_width() / 2, 250))  # Moved up the option text

def redrawGameWindow():
    win.fill((102, 108, 183))  # Updated background color (#666CB7)
    player.draw(win)
    for ball in balls:
        ball.draw(win)
    for b in bricks:
        b.draw(win)

    if gameover and victory:
        won_game()
    
    elif gameover and not victory:
        lost_game()

    pygame.display.update()

player = Paddle(sw/2 - 35, sh - 50, 70, 20, (0, 255, 100))  # Adjusted paddle size and position
ball = Ball(sw/2 - 10, sh - 100, 20, 20, (255, 255, 255))  # Adjusted ball position
balls = [ball]
init()

run = True
while run:
    clock.tick(100)
    
    if not gameover:
        for ball in balls:
            ball.move()
        if pygame.mouse.get_pos()[0] - player.w//2 < 0:
            player.x = 0
        elif pygame.mouse.get_pos()[0] + player.w//2 > sw:
            player.x = sw - player.w
        else:
            player.x = pygame.mouse.get_pos()[0] - player.w //2

        for ball in balls:
            if (ball.x >= player.x and ball.x <= player.x + player.w) or (ball.x + ball.w >= player.x and ball.x + ball.w <= player.x + player.w):
                if ball.y + ball.h >= player.y:
                    ball.yv *= -1
                    ball.y = player.y - ball.h - 1
                    bounceSound.play()

            if ball.x + ball.w >= sw or ball.x < 0:
                bounceSound.play()
                ball.xv *= -1
            if ball.y <= 0:
                bounceSound.play()
                ball.yv *= -1
            if ball.y > sh:
                balls.remove(ball)

        for brick in bricks:
            for ball in balls:
                if (ball.x >= brick.x and ball.x <= brick.x + brick.w) or (ball.x + ball.w >= brick.x and ball.x + ball.w <= brick.x + brick.w):
                    if (ball.y >= brick.y and ball.y <= brick.y + brick.h) or (ball.y + ball.h >= brick.y and ball.y + ball.h <= brick.y + brick.h):
                        brick.visible = False
                        if brick.pregnant:
                            balls.append(Ball(brick.x, brick.y, 20, 20, (255, 255, 255)))
                        ball.yv *= -1
                        brickHitSound.play()
                        break

        bricks = [brick for brick in bricks if brick.visible]

        # If all bricks are destroyed, set victory flag
        if len(bricks) == 0:
            gameover = True
            victory = True

        if len(balls) == 0:
            gameover = True
            victory = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_r]:  # Restart game
        gameover = False
        victory = False
        balls = [Ball(sw/2 - 10, sh - 100, 20, 20, (255, 255, 255))]  
        init()

    if keys[pygame.K_q]:  # Quit game
        run = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    redrawGameWindow()

pygame.quit()
