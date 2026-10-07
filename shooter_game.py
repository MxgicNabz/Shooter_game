from pygame import *
from random import randint
sc_width = 700
sc_height = 500
screen_size = (sc_width, sc_height)
window = display.set_mode(screen_size)
display.set_caption('Shooter plane fighting(SPF)')
background = transform.scale(image.load('galaxy.jpg'), screen_size)

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_width, player_height, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (player_width, player_height))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < sc_width - 80:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 20, 30, -5)
        bullets.add(bullet)


class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global missed
        if self.rect.y >= sc_height:
            self.rect.x = randint(80, sc_width - 80)
            self.rect.y = 0
            missed += 1
            

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y <= 0:
            self.kill()

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

font.init()
text = font.Font(None, 36)
text_lose = font.Font(None, 80)
lose_screen = text_lose.render('YOU LOSE!',True, (255, 0, 0))
win_screen = text_lose.render('YOU WIN!', True, (0, 200, 0))

FPS = 60
clock = time.Clock()

player = Player('rocket.png', 5, 400, 80, 100, 10)
enemies = sprite.Group()
for i in range(1, 6):
    enemy = Enemy('ufo.png', randint(80, sc_width - 80), -20, 80, 50, randint(1, 5))
    enemies.add(enemy)

bullets = sprite.Group()

running = True
finish = False
score  = 0
missed = 0
while running:
    if not finish: 
        window.blit(background, (0, 0))
        player.update()
        player.reset()
        enemies.update()
        enemies.draw(window)
        bullets.update()
        bullets.draw(window)

        collisions = sprite.groupcollide(enemies, bullets, True, True)
        for collision in collisions:
            score += 1
            enemy = Enemy('ufo.png', randint(80, sc_width - 80), -20, 80, 50, randint(1, 5))
            enemies.add(enemy)

        if sprite.spritecollide(player, enemies, False) or missed >= 5:
            finish = True
            window.blit(lose_screen, (sc_width // 2 - 100, sc_height // 2))
        if score >= 10:
            finish = True
            window.blit(win_screen, (sc_width // 2 - 100, sc_height // 2))



    score_label = text.render(f'Score : {score}', 1, (255, 255, 255))
    window.blit(score_label, (10, 20))
    missed_label = text.render(f'Missed : {missed}', 1, (255, 255 ,255))
    window.blit(missed_label, (10, 50))
    for e in event.get():
        if e.type == QUIT:
            running = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                player.fire()
                fire_sound.play()

    display.update()
    clock.tick(FPS)