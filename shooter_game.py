from pygame import *
from random import *
WIN_W = 700
WIN_H = 500

lost = 0
score = 0 
class GameSprite(sprite.Sprite):
    def __init__(self, window, p_img, p_x, p_y, size_x, size_y, p_speed):
        sprite.Sprite.__init__(self)
        self.window = window

        self.image = transform.scale(image.load(p_img), (size_x, size_y))
        self.speed = p_speed

        self.rect = self.image.get_rect()
        self.rect.x = p_x
        self.rect.y = p_y

    def reset(self):
        self.window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < WIN_W - 80:
            self.rect.x += self.speed

    def fire(self, bullets):
        bullet = Bullet(self.window, "rocket.png", self.rect.centerx, self.rect.top, 15, 20, 15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += randint(1, self.speed)
        if self.rect.y > WIN_H:
            self.rect.x = randint(80, WIN_W-80)
            self.rect.y = 0
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += -1 * self.speed
        if self.rect.y < 0:
            self.kill()



def app():
    global score
    mixer.init()
    mixer.music.load('space.ogg')
    mixer.music.play()

    font.init()
    game_font = font.SysFont('Arial', 36)

    display.set_caption('Shooter')
    window = display.set_mode((WIN_W, WIN_H))
    background = transform.scale(image.load('galaxy.jpg'), (WIN_W, WIN_H))
    ship = Player(window, 'images.jpg', 5, WIN_H - 100, 80, 100, 5)



    bullets = sprite.Group()
    monsters = sprite.Group()
    for i in range (1, 6):
        monstr = Enemy(window, 'rocket.png', randint(80, WIN_W-80), -40, 80, 50, 5)
        monsters.add(monstr)

    run = True
    finish = False
    while run:
        window.blit(background, (0, 0))
        for e in event.get():
            if e.type == QUIT:
                run = False
            elif e.type == KEYDOWN:
                if e.key == K_SPACE:
                    ship.fire(bullets)
                    mixer.Sound('fire.ogg')


        if not finish:
            text = game_font.render(f'Пропущено: {lost}', 1, (255, 255, 255))
            window.blit(text, (10, 20))
            text_2 = game_font.render(f'Счёт: {score}', 1, (255, 255, 255))
            window.blit(text_2, (10, 50))

            ship.update()
            ship.reset()
            monsters.update()
            bullets.update()

            monsters.draw(window)
            bullets.draw(window)

            colliders = sprite.groupcollide(monsters, bullets, True, True)
            for c in colliders:
                score += 1
                monstr = Enemy(window, 'rocket.png', randint(80, WIN_W-80), -40, 80, 50, 5)
                monsters.add(monstr)

            if score >= 10:
                window.blit(font.SysFont('Arial', 80).render('WIN', 1, (255, 255, 255)), (200, 200))
                finish = True

            if lost >= 20:
                window.blit(font.SysFont('Arial', 80).render('LOSE', True, (200, 0, 0)), (200, 200))
                finish = True
                

            display.update()

            

if __name__ == "__main__":
    app()



