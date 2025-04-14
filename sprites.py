# Sprite classes for platform game
from settings import *
import random
vec = pg.math.Vector2

class Player(pg.sprite.Sprite):
    def __init__(self, game):
        self._layer = PLAYER_LAYER
        pg.sprite.Sprite.__init__(self)
        self.running = False
        self.jumping = False
        self.game = game
        self.idle = []
        self.run_img_r = []
        self.run_img_l = []
        self.width= 40
        self.height=80


        self.load_img()



        self.image = self.idle[0]


        # self.image = pg.Surface((30, 40))
        # self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.pos = vec(WIDTH / 2, HEIGHT / 2)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

        self.count=0
        self.track=0
        self.far=0
        self.stop=False 

        self.last_update = 0

        self.current_frame = 0

    def animate(self):
        now = pg.time.get_ticks()
        if int(self.vel.x) != 0: self.running = True
        else: self.running = False
        if not self.running and not self.jumping:
            if now - self.last_update > 500:
                self.last_update = now
                self.current_frame = (self.current_frame + 1)%len(self.idle)
                self.image = self.idle[self.current_frame]
                self.rect = self.image.get_rect()
        if self.jumping:
            self.image = pg.image.load("jump-up.png")
            self.image = pg.transform.scale(self.image, (self.width, self.height))
            self.rect = self.image.get_rect()
        if self.running:
            if now - self.last_update > 150:
                self.last_update = now
                self.current_frame = (self.current_frame + 1)%len(self.idle)
                self.image = self.run_img_r[self.current_frame]
                if self.vel.x < 0:
                    self.image = self.run_img_l[self.current_frame]

                self.rect = self.image.get_rect()
    def load_img(self):
        for i in range(1,3):
            filename = f"stand{i}.png"
            img = pg.image.load(filename)
            img = pg.transform.scale(img, (self.width,self.height))
            self.idle.append(img)

        for i in range(1,6):
            filename = f"runy{i}.png"
            img_r = pg.image.load(filename)
            img_r = pg.transform.scale(img_r, (self.width,self.height))
            self.run_img_r.append(img_r)

        for frame in self.run_img_r:
            self.run_img_l.append(pg.transform.flip(frame, True, False))

    def jump(self):
        # jump only if standing on a platform
        self.rect.x += 1
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        self.rect.x -= 1
        if hits:
            self.jumping = True
            self.vel.y = -20

    def update(self):
        self.animate()
        self.acc = vec(0, PLAYER_GRAV)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.acc.x = -PLAYER_ACC

        if keys[pg.K_RIGHT]:
            self.acc.x = PLAYER_ACC

        # apply friction
        self.acc.x += self.vel.x * PLAYER_FRICTION
        # equations of motion
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        # wrap around the sides of the screen
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH

        self.rect.midbottom = self.pos

class Platform(pg.sprite.Sprite):
    def __init__(self,game, x, y, w, h):
        self._layer = PLATFORM_LAYER
        self.groups= game.all_sprites,game.platforms
        pg.sprite.Sprite.__init__(self,self.groups)
        self.game=game
        self.width= random.randrange(30,80)
        self.height = 50
        self.plat_img=[]
        self.load_img()
        self.image = random.choice(self.plat_img)
        # self.image = pg.Surface((w, h))
        # self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        if random.randrange(100)<POW_SPAWN_PCT:
            Pow(self.game,self)
    def load_img(self):
        for i in range(1,6):
            filename = f"plat{i}.PNG"
            img = pg.image.load(filename)
            img = pg.transform.scale(img, (self.width,self.height))
            self.plat_img.append(img)


class Cloud(pg.sprite.Sprite):
    def __init__(self, game):
        self._layer = CLOUD_LAYER
        self.groups = game.all_sprites, game.clouds
        pg.sprite.Sprite.__init__(self,self.groups)
        self.game=game
        self.image = random.choice(self.game.cloud_images)
        self.image.set_colorkey(BLACK)
        # self.image = pg.Surface((w, h))
        # self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        scale = random.randrange(50,101) / 100
        self.image= pg.transform.scale(self.image,(int(self.rect.width*scale),int(self.rect.height*scale)))
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-500,-50)
    def update(self):
      if self.rect.top> HEIGHT*2:
        self.kill()

class Pow(pg.sprite.Sprite):
    def __init__(self, game, plat):
        self.groups = game.all_sprites, game.powerups
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.plat = plat
        self.type = random.choice(['boost'])
        self.image = pg.image.load("power.PNG")
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = self.plat.rect.centerx
        self.rect.bottom = self.plat.rect.top - 5

    def update(self):
        self.rect.bottom = self.plat.rect.top - 5
        if not self.game.platforms.has(self.plat):
            self.kill()