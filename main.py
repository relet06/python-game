import pygame
import time
### MOVEMENT ###
### YELLOW: MOVEMENT: A S D W, LASER: L.SHIFT, BULLET: L.CTRL
### RED: MOWEMENT: ARROWS, LASER: R.SHIFT, BULLET: R.CTRL

pygame.init()
MAX_LASERS = 1
HEIGHT, WIDTH = 500, 900
health_red, health_yellow = 5, 5
FONT = pygame.font.SysFont("comisans", 30)
FONT2 = pygame.font.SysFont("times new roman", 60)
FONT_bullet = pygame.font.SysFont("times new roman", 40)
MAX_BULLETS = 3
PLAYER_HEIGHT, PLAYER_WIDTH = 50, 41
BORDER = pygame.Rect(WIDTH//2 - 5, 0, 5, HEIGHT)
VEL = 5
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Idols")
#images
RED_PLAYER = pygame.transform.rotate(pygame.transform.scale(pygame.image.load("images/spaceship_red.png"), (PLAYER_HEIGHT, PLAYER_WIDTH)), -90)
YELLOW_PLAYER = pygame.transform.rotate(pygame.transform.scale(pygame.image.load("images/spaceship_yellow.png"), (PLAYER_HEIGHT, PLAYER_WIDTH)), 90)
BG = pygame.transform.scale(pygame.image.load("images/space.png"), (WIDTH, HEIGHT))
bullet = pygame.transform.scale(pygame.image.load("images/bullet..png"), (36, 78))
class Bullet:
    def __init__(self, x, y, color, direction):
        self.x = x
        self.y = y
        self.direction = direction
        self.color = color
        self.speed = VEL * 2
    def move(self):
        if self.direction == "left":
            self.x -= self.speed
        elif self.direction == "right":
            self.x += self.speed

class Laser:
    def __init__(self, x, y, color, direction):
        self.x = x
        self.y = y
        self.color = color
        self.direction = direction
        self.charging = True
        self.charge_time = 1
        self.damage_time = 0.5
        self.start_time = time.time()
    def update(self):
        current_time = time.time()
        if self.charging and current_time - self.start_time >= self.charge_time:
            self.charging = False
            self.start_time = current_time
        elif not self.charging and current_time - self.start_time >= self.damage_time:
            return True
        return False


def draw_lasers(red_lasers, yellow_lasers):
    for laser in red_lasers:
        time_since_start = time.time() - laser.start_time
        if laser.charging:
            laser_width = int(1 * (time_since_start / laser.charge_time)) + 1
        else:
            laser_width = int(10 * (time_since_start / laser.damage_time)) + 1
        if laser.direction == "left":
            pygame.draw.line(WIN, "red", (0, laser.y), (laser.x, laser.y), laser_width)

    for laser in yellow_lasers:
        time_since_start = time.time() - laser.start_time
        if laser.charging:
            laser_width = int(1 * (time_since_start / laser.charge_time)) + 1
        else:
            laser_width = int(10 * (time_since_start / laser.damage_time)) + 1
        if laser.direction == "right":
            pygame.draw.line(WIN, "yellow", (laser.x, laser.y), (WIDTH, laser.y), laser_width)

def draw_bullets(red_bullets, yellow_bullets):
    for bullet in red_bullets:
        pygame.draw.rect(WIN, "red", (bullet.x, bullet.y, 10, 5))
    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, "yellow", (bullet.x, bullet.y, 10, 5))
def shots(key_pressed, red, yellow, red_bullets, yellow_bullets):
    if key_pressed[pygame.K_RCTRL]:
        if len(red_bullets) < MAX_BULLETS:
            red_bullet = Bullet(red.x + PLAYER_WIDTH, red.y + PLAYER_HEIGHT // 2, "red", "left")
            red_bullets.append(red_bullet)
    if key_pressed[pygame.K_LCTRL]:
        if len(yellow_bullets) < MAX_BULLETS:
            yellow_bullet = Bullet(yellow.x + PLAYER_WIDTH, yellow.y + PLAYER_HEIGHT // 2, "yellow", "right")
            yellow_bullets.append(yellow_bullet)
def update_bullets(red_bullets, yellow_bullets):
    for bullet in red_bullets:
        bullet.move()
        if bullet.x < 0 or bullet.x > WIDTH:
            red_bullets.remove(bullet)
    for bullet in yellow_bullets:
        bullet.move()
        if bullet.x < 0 or bullet.x > WIDTH:
            yellow_bullets.remove(bullet)


def check_collisions(red, yellow, red_bullets, yellow_bullets, red_lasers, yellow_lasers):
    global health_red, health_yellow

    for bullet in red_bullets:
        if yellow.colliderect(pygame.Rect(bullet.x, bullet.y, 10, 5)):
            red_bullets.remove(bullet)
            health_yellow -= 1

    for bullet in yellow_bullets:
        if red.colliderect(pygame.Rect(bullet.x, bullet.y, 10, 5)):
            yellow_bullets.remove(bullet)
            health_red -= 1

    for laser in red_lasers[:]:
        if laser.direction == "left" and red.y < laser.y < red.y + PLAYER_HEIGHT:
            if laser.update():
                health_yellow -= 1
                red_lasers.remove(laser)

    for laser in yellow_lasers[:]:
        if laser.direction == "right" and yellow.y < laser.y < yellow.y + PLAYER_HEIGHT:
            if laser.update():
                health_red -= 1
                yellow_lasers.remove(laser)



def draw(red, yellow, red_bullets, yellow_bullets):
    red_health_text = FONT.render(f"Health: {health_red}", 1, "red")
    yellow_health_text = FONT.render(f"Health: {health_yellow}", 1, "yellow")
    red_game_over_text = FONT2.render(f"GAME OVER! YELLOW WINS", 1, "green")
    yellow_game_over_text = FONT2.render(f"GAME OVER! RED WINS", 1, "green")
    red_bullet_count = str(MAX_BULLETS - (len(red_bullets)))
    yellow_bullet_count = str(MAX_BULLETS - len(yellow_bullets))
    red_bullet_count_text = FONT.render(red_bullet_count, 1, "white")
    yellow_bullet_count_text = FONT.render(yellow_bullet_count, 1, "white")

    WIN.fill("grey")
    WIN.blit(BG, (0, 0))
    pygame.draw.rect(WIN, "white", BORDER)
    WIN.blit(RED_PLAYER, (red.x, red.y))
    WIN.blit(YELLOW_PLAYER, (yellow.x, yellow.y))
    WIN.blit(red_health_text, (WIDTH - 10 - red_health_text.get_width(), 10))
    WIN.blit(yellow_health_text, (10, 10))
    WIN.blit(bullet, (WIDTH - bullet.get_width() - 50, HEIGHT - 100))  # BULLET FOR RED PLAYER
    WIN.blit(bullet, (bullet.get_width(), HEIGHT - 100))  # BULLET FOR YELLOW PLAYER
    # COUNT OF BULLETS
    WIN.blit(red_bullet_count_text, (WIDTH - bullet.get_width() / 2 - 54, HEIGHT - 100 + bullet.get_height() / 2 - 10))
    WIN.blit(yellow_bullet_count_text, (0 + bullet.get_width() / 2 + 32, HEIGHT - 100 + bullet.get_height() / 2 - 10))
    if health_yellow <= 0:
        WIN.blit(yellow_game_over_text, (WIDTH//2 - yellow_game_over_text.get_width()//2, HEIGHT // 2))
    elif health_red <= 0:
        WIN.blit(red_game_over_text, (WIDTH//2 - red_game_over_text.get_width()//2, HEIGHT // 2 - 50))
    pygame.display.flip()
def movement(key_pressed, red, yellow):
     #  red MOVEMENT
    if key_pressed[pygame.K_LEFT] and red.x > WIDTH//2:   # left
        red.x -= VEL
    if key_pressed[pygame.K_RIGHT]  and red.x < WIDTH - PLAYER_WIDTH + 5:     # right
        red.x += VEL
    if key_pressed[pygame.K_UP] and red.y > 0:    # up
        red.y -= VEL
    if key_pressed[pygame.K_DOWN] and red.y < HEIGHT - PLAYER_HEIGHT:      # down
        red.y += VEL
     # yellow MOVEMENT
    if key_pressed[pygame.K_a] and yellow.x > 0:     # left
        yellow.x -= VEL
    if key_pressed[pygame.K_d] and yellow.x < WIDTH//2 - 45:     # rigth
        yellow.x += VEL
    if key_pressed[pygame.K_w] and yellow.y > 0:     # up
        yellow.y -= VEL
    if key_pressed[pygame.K_s] and yellow.y < HEIGHT - PLAYER_HEIGHT:     # down
        yellow.y += VEL
def main():
    red_lasers = []
    yellow_lasers = []
    red_bullets = []
    yellow_bullets = []
    red = pygame.Rect(700, 100, PLAYER_WIDTH, PLAYER_HEIGHT)
    yellow = pygame.Rect(100, 100, PLAYER_WIDTH, PLAYER_HEIGHT)
    clock = pygame.time.Clock()
    pygame.init()
    run = True
    while run:
        key_pressed = pygame.key.get_pressed()
        clock.tick(60)
        # funcs
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                # bullets
                if event.key == pygame.K_RCTRL or event.key == pygame.K_LCTRL:
                    shots({pygame.K_RCTRL: event.key == pygame.K_RCTRL, pygame.K_LCTRL: event.key == pygame.K_LCTRL},
                          red, yellow, red_bullets, yellow_bullets)
                # lasers
                if event.key == pygame.K_RSHIFT:  # RED LASER always shoots right
                    if len(red_lasers) < MAX_LASERS:
                        red_laser = Laser(red.x, red.y + PLAYER_HEIGHT // 2, "red", "left")
                        red_lasers.append(red_laser)
                if event.key == pygame.K_LSHIFT:  # YELLOW LASER
                    if len(yellow_lasers) < MAX_LASERS:
                        yellow_laser = Laser(yellow.x + PLAYER_WIDTH, yellow.y + PLAYER_HEIGHT // 2, "yellow", "right")
                        yellow_lasers.append(yellow_laser)
        for laser in red_lasers[:]:
            if laser.update():
                red_lasers.remove(laser)
        for laser in yellow_lasers[:]:
            if laser.update():
                yellow_lasers.remove(laser)

        draw(red, yellow, red_bullets, yellow_bullets)
        update_bullets(red_bullets, yellow_bullets)
        check_collisions(red, yellow, red_bullets, yellow_bullets, red_lasers, yellow_lasers)
        movement(key_pressed, red, yellow)
        draw_bullets(red_bullets, yellow_bullets)
        draw_lasers(red_lasers, yellow_lasers)
        pygame.display.update()
        # game over when
        if (health_red or health_yellow) < 1:
            time.sleep(1.2)
            run = False

    pygame.quit()

main()