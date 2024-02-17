#Створи власний Шутер!

from random import randint
from pygame import *

font.init()
window = display.set_mode((700,500))
display.set_caption("Шутер")
background = transform.scale(image.load("galaxy.jpg"), (700, 500))
clock = time.Clock()
FPS = 60

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, plater_x,plater_y, player_speed, width, height):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (width,height))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = plater_x
        self.rect.y = plater_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        key_pressed = key.get_pressed()
        if key_pressed[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if key_pressed[K_d] and self.rect.x < 615:
            self.rect.x += self.speed
    def fire(self): 
        bullet = Bullet('bullet.png', self.rect.centerx,self.rect.y, -15, 10, 30)
        bullets.add(bullet)


class Enemy(GameSprite):
    def update(self):
        global lost, score
        self.rect.y += self.speed
        if self.rect.y > 500:
            self.rect.y = 0
            self.rect.x = randint(80, 620)
            lost += 1
        if sprite.spritecollide(self, bullets,True):
            score += 1
            self.rect.y = 0
            self.rect.x = randint(80, 620)

            
class Label():
    def set_text(self, text, fsize = 12, text_color =(0, 0, 0)):
        self.image = font.SysFont('verdana', fsize).render(text, True, text_color)

    def draw(self, shift_x = 0, shift_y = 0):
        window.blit(self.image, (shift_x,shift_y))

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
sound_fire = mixer.Sound('fire.ogg')

lost_text = Label()


# score = Label(430,55,50,40,(90, 167, 255))
# score.set_text('0', 45)
# score.draw(0,0)

score = 0
lost = 0
player = Player('rocket.png', 300, 400, 4, 80, 100)

enemies = sprite.Group()
for i in range (1, 6):
    enemy = Enemy('ufo.png', randint(80, 620), 0, randint(1, 3), 80, 50)
    enemies.add(enemy)
bullets = sprite.Group()

#win = font.render('YOU THE FIRST!', True, (255, 215, 0))

game = True
finish = False
while game:
    window.blit(background,(0,0))
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                player.fire()
                sound_fire.play()
    if finish != True:
        player.update()
        enemies.update()
        enemies.draw(window)
        player.reset()
        bullets.update()
        bullets.draw(window)
        lost_text.set_text('Пропущено: '+str(lost), 30, (90, 167, 255))
        lost_text.draw(5,20)
        lost_text.set_text('Збитих: '+str(score), 30, (90, 167, 255))
        lost_text.draw(5,60)

            #sprite.groupcollide(enemies, bullets, False, True)

    if sprite.spritecollide(player, enemies, False) or lost >= 10:
        loss = Label()
        loss.set_text('YOU LOST!', 60, (255, 0, 0))
        window.blit(background,(0,0))
        loss.draw(170, 250)
        finish = True
    if score >= 10:
        win = Label()
        win.set_text('YOU THE FIRST!', 60, (255, 215, 0))
        window.blit(background,(0,0))
        win.draw(150, 250)
        finish = True

                
    
    display.update()
    clock.tick(FPS)