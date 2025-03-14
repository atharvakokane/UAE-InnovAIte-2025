import pygame
import sys
import random

pygame.init()
screen = pygame.display.set_mode((500, 300))
clock = pygame.time.Clock()
pygame.display.set_caption("Dino Game")

game_font = pygame.font.Font("empowermentgame/assets/PressStart2P-Regular.ttf", 16)

class Cloud(pygame.sprite.Sprite):
    def __init__(self, image, x_pos, y_pos):
        super().__init__()
        self.image = pygame.transform.scale(image, (80, 30))
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))

    def update(self):
        self.rect.x -= 1

class Dino(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        super().__init__()
        self.running_sprites = []
        self.ducking_sprites = []
        self.running_sprites.append(pygame.transform.scale(
            pygame.image.load("empowermentgame/assets/Dino1.png"), (40, 50)))
        self.running_sprites.append(pygame.transform.scale(
            pygame.image.load("empowermentgame/assets/Dino2.png"), (40, 50)))
        self.ducking_sprites.append(pygame.transform.scale(
            pygame.image.load(f"empowermentgame/assets/DinoDucking1.png"), (55, 30)))
        self.ducking_sprites.append(pygame.transform.scale(
            pygame.image.load(f"empowermentgame/assets/DinoDucking2.png"), (55, 30)))
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.current_image = 0
        self.image = self.running_sprites[self.current_image]
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.velocity = 50
        self.gravity = 3.5
        self.jump_speed = 14
        self.is_jumping = False
        self.jump_count = 10
        self.ducking = False

    def jump(self):
        if not self.is_jumping and self.rect.centery >= 240:
            self.is_jumping = True
            self.velocity = self.jump_speed
            jump_sfx.play()

    def duck(self):
        self.ducking = True
        self.rect.centery = 220

    def unduck(self):
        self.ducking = False
        self.rect.centery = 240

    def apply_gravity(self):
        if self.rect.centery < 240:
            self.rect.centery += self.gravity

    def update(self):
        self.animate()
        if self.is_jumping:
            self.rect.centery -= self.velocity
            self.velocity -= 0.5
            if self.velocity <= 0:
                self.is_jumping = False
                self.velocity = self.jump_speed

        if not self.is_jumping:
            self.apply_gravity()

        if self.rect.centery >= 240:
            self.rect.centery = 240
            if not self.is_jumping:
                self.is_jumping = False

    def animate(self):
        self.current_image += 0.05
        if self.current_image >= 2:
            self.current_image = 0

        if self.ducking:
            self.image = self.ducking_sprites[int(self.current_image)]
        else:
            self.image = self.running_sprites[int(self.current_image)]

class Cactus(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        super().__init__()
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.sprites = []
        for i in range(1, 7):
            current_sprite = pygame.transform.scale(
                pygame.image.load(f"empowermentgame/assets/cacti/cactus{i}.png"), (40, 40))
            self.sprites.append(current_sprite)
        self.image = random.choice(self.sprites)
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))

    def update(self):
        self.x_pos -= game_speed
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))

class Ptero(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.x_pos = 1300
        self.y_pos = random.choice([180, 195, 250])
        self.sprites = []
        self.sprites.append(
            pygame.transform.scale(
                pygame.image.load("empowermentgame/assets/Ptero1.png"), (42, 31)))
        self.sprites.append(
            pygame.transform.scale(
                pygame.image.load("empowermentgame/assets/Ptero2.png"), (42, 31)))
        self.current_image = 0
        self.image = self.sprites[self.current_image]
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))

    def update(self):
        self.animate()
        self.x_pos -= game_speed
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))

    def animate(self):
        self.current_image += 0.025
        if self.current_image >= 2:
            self.current_image = 0
        self.image = self.sprites[int(self.current_image)]

game_speed = 3
jump_count = 10
player_score = 0
game_over = False
obstacle_timer = 0
obstacle_spawn = False
obstacle_cooldown = 1000

ground = pygame.image.load("empowermentgame/assets/ground.png")
ground = pygame.transform.scale(ground, (500, 10))
ground_x = 0
ground_rect = ground.get_rect(center=(250, 290))
cloud = pygame.image.load("empowermentgame/assets/cloud.png")
cloud = pygame.transform.scale(cloud, (80, 30))

cloud_group = pygame.sprite.Group()
obstacle_group = pygame.sprite.Group()
dino_group = pygame.sprite.GroupSingle()
ptero_group = pygame.sprite.Group()

dinosaur = Dino(50, 240)
dino_group.add(dinosaur)

death_sfx = pygame.mixer.Sound("empowermentgame/assets/sfx/lose.mp3")
points_sfx = pygame.mixer.Sound("empowermentgame/assets/sfx/100points.mp3")
jump_sfx = pygame.mixer.Sound("empowermentgame/assets/sfx/jump.mp3")

CLOUD_EVENT = pygame.USEREVENT
pygame.time.set_timer(CLOUD_EVENT, 3000)

def end_game():
    global player_score, game_speed
    game_over_text = game_font.render("Game Over!", True, "black")
    game_over_rect = game_over_text.get_rect(center=(250, 130))
    score_text = game_font.render(f"Score: {int(player_score)}", True, "black")
    score_rect = score_text.get_rect(center=(250, 160))
    screen.blit(game_over_text, game_over_rect)
    screen.blit(score_text, score_rect)
    game_speed = 5
    cloud_group.empty()
    obstacle_group.empty()

while True:
    keys = pygame.key.get_pressed()
    if keys[pygame.K_DOWN]:
        dinosaur.duck()
    else:
        if dinosaur.ducking:
            dinosaur.unduck()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == CLOUD_EVENT:
            current_cloud_y = random.randint(50, 150)
            current_cloud = Cloud(cloud, 500, current_cloud_y)
            cloud_group.add(current_cloud)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                dinosaur.jump()
                if game_over:
                    game_over = False
                    game_speed = 5
                    player_score = 0

    screen.fill("lightpink")

    if pygame.sprite.spritecollide(dino_group.sprite, obstacle_group, False):
        game_over = True
        death_sfx.play()
    if game_over:
        end_game()

    if not game_over:
        game_speed += 0.0015
        if round(player_score, 1) % 100 == 0 and int(player_score) > 0:
            points_sfx.play()

        if pygame.time.get_ticks() - obstacle_timer >= obstacle_cooldown:
            obstacle_spawn = True

        if obstacle_spawn:
            obstacle_random = random.randint(1, 50)
            if obstacle_random in range(1, 7):
                new_obstacle = Cactus(500, 240)
                obstacle_group.add(new_obstacle)
                obstacle_timer = pygame.time.get_ticks()
                obstacle_spawn = False
            elif obstacle_random in range(7, 10):
                new_obstacle = Ptero()
                obstacle_group.add(new_obstacle)
                obstacle_timer = pygame.time.get_ticks()
                obstacle_spawn = False

        player_score += 0.1
        player_score_surface = game_font.render(
            str(int(player_score)), True, ("black"))
        screen.blit(player_score_surface, (450, 10))

        cloud_group.update()
        cloud_group.draw(screen)

        ptero_group.update()
        ptero_group.draw(screen)

        dino_group.update()
        dino_group.draw(screen)

        obstacle_group.update()
        obstacle_group.draw(screen)

        ground_x -= game_speed

        screen.blit(ground, (ground_x, 290))
        screen.blit(ground, (ground_x + 500, 290))

        if ground_x <= -500:
            ground_x = 0

    clock.tick(120)
    pygame.display.update()
