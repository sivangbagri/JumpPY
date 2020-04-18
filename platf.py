"""
Author: Shivang
Created on: 14/3/20

"""

import pygame
import random
from PYsettings import *
from Sprites import *


class Game:
    def __init__(self):
        # intialise game window
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(icon)
        self.clock = pygame.time.Clock()
        self.running = True
        self.font_name = 'plat_assets/BRLNSR.ttf'
        self.data_load()

    def data_load(self):

        with open('scorefile.txt', 'r+') as file:
            try:
                self.highscore = int(file.readline())
            except:
                self.highscore = 0
        # load spritesheet image
        self.spritesheet = Spritesheet(SPRITESHEET)
        # loading clouding iamge
        self.cloud_im = []
        for i in range(1, 4):
            self.cloud_im.append(pygame.image.load(f'plat_assets/cloud{i}.png'))

        pygame.mixer.music.load("plat_assets/bgmu.mp3")

    def new(self):
        # start a new game
        self.score = 0
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.platforms = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        self.mobs = pygame.sprite.Group()
        self.clouds = pygame.sprite.Group()

        self.player = Player(self)
        # p1 = Platform(0, HEIGHT - 40)
        # self.all_sprites.add(self.player)
        for plat in PLATFORM_LIST:
            Platform(self, *plat)
            # self.all_sprites.add(p)
            # self.platforms.add(p)
        self.mob_timer = 0
        self.run()

    def run(self):
        # game loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        # game loop -update
        self.all_sprites.update()
        # spawn mob
        now = pygame.time.get_ticks()
        if now - self.mob_timer > 5000:
            self.mob_timer = now
            Mob(self)
        # mob and player colllision
        mob_coll = pygame.sprite.spritecollide(self.player, self.mobs, True, pygame.sprite.collide_mask)
        if mob_coll:
            self.playing = False
            # self.playing = False
        # check for hitting platform -only if falling
        if self.player.vel.y > 0:
            hits = pygame.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                lowest = hits[0]
                for hit in hits:
                    if hit.rect.bottom > lowest.rect.bottom:
                        lowest = hit
                if self.player.pos.x < lowest.rect.right + 10 and self.player.pos.x > lowest.rect.left - 10:
                    if self.player.pos.y < lowest.rect.bottom:
                        self.player.pos.y = lowest.rect.top
                        self.player.vel.y = 0
        # scrolling if player reaches above height/4
        if self.player.pos.y <= HEIGHT / 4:
            if random.randrange(100) > 90:
                Cloud(self)

            self.player.pos.y += max(abs(self.player.vel.y), 3)
            for mob in self.mobs:
                mob.rect.y += max(abs(self.player.vel.y), 3)
            for cloud in self.clouds:
                cloud.rect.y += max(abs(self.player.vel.y / 2), 3)

            for plat in self.platforms:
                plat.rect.y += max(abs(self.player.vel.y), 3)
                if plat.rect.top >= HEIGHT:
                    plat.kill()
                    self.score += 10
        # player hits powerups
        pow_collide = pygame.sprite.spritecollide(self.player, self.powerups, True)
        for hit in pow_collide:
            if hit.type == 'boost':
                self.player.vel.y = -BOOST_POWER
                self.jumping = False
            # die
        if self.player.rect.bottom > HEIGHT:
            for sprite in self.all_sprites:
                sprite.rect.y -= self.player.vel.y
                if sprite.rect.bottom < 0:
                    sprite.kill()
        if len(self.platforms) == 0:
            self.playing = False

        # spawning new platforms
        while len(self.platforms) < 6:
            width = random.randrange(50, 100)
            Platform(self, random.randrange(0, WIDTH - width),
                     random.randrange(-75, -30))
            # self.all_sprites.add(p)
            # self.platforms.add(p)

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # self.jump_sound.play()
                    self.player.jump()

    def draw(self):
        self.screen.fill((0, 155, 155))
        self.all_sprites.draw(self.screen)
        # self.screen.blit(self.player.image, self.player.rect) '''no need after layer command'''
        self.draw_text(str(self.score), 22, WHITE, WIDTH / 2, 5)
        # after drawing flip the display
        pygame.display.flip()

    def show_start_screen(self):
        # start screen
        # self.screen.fill((0,155,0))
        self.screen.blit(starter_scale, (0, 0))
        self.draw_text(TITLE, 65, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("BY SHIVANG", 18, RED, WIDTH / 2 + 3, HEIGHT / 2)
        self.draw_text("Press any key to continue...", 20, WHITE, WIDTH / 2, HEIGHT - 100)
        self.draw_text("HIGH SCORE " + str(self.highscore), 15, WHITE, WIDTH / 2, HEIGHT - 20)
        pygame.display.flip()
        self.wait_for_key()

    def show_go_screen(self):
        if self.running == False:
            return  # ends this function
        self.screen.fill((155, 200, 0))
        self.draw_text("GAME OVER", 65, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Score : " + str(self.score), 25, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Press any key to restart...", 20, WHITE, WIDTH / 2, HEIGHT - 100)
        if self.score > self.highscore:
            self.highscore = self.score
            self.draw_text("NEW HIGH SCORE", 20, WHITE, WIDTH / 2, HEIGHT - 150)
            with open("scorefile.txt", "w") as file:
                file.write(str(self.highscore))
        else:
            self.draw_text("HIGH SCORE " + str(self.highscore), 15, WHITE, WIDTH / 2, HEIGHT - 20)

        pygame.display.flip()
        self.wait_for_key()

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pygame.KEYUP:
                    waiting = False

    def draw_text(self, text, size, color, x, y):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)


g = Game()
g.show_start_screen()
while g.running:
    pygame.mixer.music.play(-1)
    g.new()
    g.show_go_screen()
pygame.quit()
