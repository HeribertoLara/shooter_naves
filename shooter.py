import pygame, random

WIDTH = 800
HEIGHT = 600

BLACK = (0,0,0)
WHITE = (255,255,255)
GREEN = (0, 255, 0)

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Shooter")
clock = pygame.time.Clock()

# funcion drawshield
def draw_shield_bar(surface, x, y, percentage):
    BAR_LENGTH = 100
    BAR_HEIGTH = 10
    fill = (percentage/100) * BAR_LENGTH
    border = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGTH )
    fill = pygame.Rect(x, y, fill, BAR_HEIGTH)
    pygame.draw.rect(surface, GREEN, fill)
    pygame.draw.rect(surface, WHITE, border, 2)

#funcion de texo
def draw_text( surface, text, size, x, y):
    #screen.blit(backgrounds, [0,0])
    font = pygame.font.SysFont("serif", size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop= (x, y)
    surface.blit(text_surface, text_rect)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(). __init__()
        self.image = pygame.image.load("player.png").convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.centerx = WIDTH//2
        self.rect.bottom = HEIGHT -10
        self.speed_x = 0
        self.shield = 100

    def update(self):
        self.speed_x = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speed_x = -5
        if keystate[pygame.K_RIGHT]:
            self.speed_x =5
        self.rect.x += self.speed_x
        if self.rect.right>WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
    def shoot(self):
        bullet = Bullet( self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)
        laser_sound.play()

def show_game_over():
    draw_text(screen, "SHOOTER", 65, WIDTH // 2, HEIGHT // 4)
    draw_text(screen, "Instrucciones van aqui", 27, WIDTH // 2, HEIGHT // 2)
    draw_text(screen, "Press Key", 65, WIDTH // 2, HEIGHT -3/4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False


class Meteor(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = random.choice(meteor_images)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-140, -100)
        self.speedy = random.randrange(1,10)
        self.speedx = random.randrange(-5,5)
    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT +10 or self.rect.left < -40 or self.rect.right > WIDTH+25:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 10)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("laser1.png")
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()
class Explosion(pygame.sprite.Sprite):
    def __init__(self,center):
        super().__init__()
        self.image = explosion_anim[0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50 # Velocidad de la explosion
    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame +=1
            if self.frame == len(explosion_anim):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


# lista de meteoros = []
meteor_list = ["meteorGrey_big1.png", "meteorGrey_big2.png", "meteorGrey_big3.png", "meteorGrey_big4.png","meteorGrey_med1.png", "meteorGrey_med2.png","meteorGrey_small1.png","meteorGrey_small2.png", "meteorGrey_tiny1.png", "meteorGrey_tiny2.png"]
#meteor_list = ["meteorGrey_big1.png", "meteorGrey_big2.png", "meteorGrey_big3.png","meteorGrey_big4.png",]
meteor_images = [ ]
for img in meteor_list:
    meteor_images.append(pygame.image.load(img).convert())

#------Explosiones---------
explosion_anim = []
for i in range(9):
    file = "regularExplosion0{}.png".format(i)
    img = pygame.image.load(file).convert()
    img.set_colorkey(BLACK)
    img_scale = pygame.transform.scale(img, (70, 70))
    explosion_anim.append(img_scale)

backgrounds = pygame.image.load("background.png").convert()

# cargar sonidos
laser_sound = pygame.mixer.Sound("Laser_Gun.wav")
explosion = pygame.mixer.Sound("explosion.wav")
music = pygame.mixer.music.load("music_starship.wav ")
pygame.mixer.music.set_volume(0.1)

 
#  lista de meteoritos balas y todos los sprites

pygame.mixer.music.play(loops=1)# el alor de -1 va a crear un bucle infinito

running = True
game_over = True

while running:
    if game_over:
        show_game_over()
        game_over = False
        all_sprites = pygame.sprite.Group()
        meteor_list = pygame.sprite.Group()
        bullets = pygame.sprite.Group()

        player = Player()
        all_sprites.add(player)

        for i in range(8):
            meteor = Meteor()
            all_sprites.add(meteor)
            meteor_list.add(meteor)

        score = 0


    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    all_sprites.update()
    # colisiones - meteoro - laser
    hits = pygame.sprite.groupcollide(meteor_list, bullets, True, True)
    for hit in hits:
        score += 10
        explosion = Explosion(hit.rect.center)
        all_sprites.add(explosion)
        meteor = Meteor()
        all_sprites.add(meteor)
        meteor_list.add(meteor)

    # colisiones jugador meteoro

    hits = pygame.sprite.spritecollide(player,meteor_list, True)
    for hit in hits:
        player.shield -= 25
        if player.shield ==0:
            game_over = True

    screen.blit(backgrounds,[0,0])
    all_sprites.draw(screen)

    # Marcador Score pintar
    draw_text(screen, str(score), 25, WIDTH//2, 10)
    # dibujando escudo
    draw_shield_bar(screen, 5, 5, player.shield)

    pygame.display.flip()
pygame.quit()
