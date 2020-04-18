import pygame

TITLE = "JumpPy"
FPS = 60
WIDTH = 480
HEIGHT = 600

icon = pygame.image.load("plat_assets/bunny2_jump.png")
# player properties
PLAYER_ACC = 0.5
PLAYER_FRICTION = -0.12  # ideal =0.12 or 0.02
PLAYER_GRAV = 0.5
PLAYER_JUMP = 15

starter = pygame.image.load("plat_assets/somebgs (2).jpg")
starter_scale = pygame.transform.scale(starter, (WIDTH, HEIGHT))

# layers
PLAYER_LAYER = 2
PLAT_LAYER = 1
POW_LAYER = 1
MOB_LAYER = 2
CLOUD_LAYER = -1

# powerups properties
BOOST_POWER = 45
SPAWN_PCT = 7
MOB_FREQ = 500  # millisecond

# all platforms
PLATFORM_LIST = [(0, HEIGHT - 40),
                 (50, HEIGHT * 3 / 4),  # (x,y,w,h)
                 (150, HEIGHT * 3 / 4 - 100),
                 (200, HEIGHT * 3 / 4 - 200),
                 (300, HEIGHT * 3 / 4 - 400),
                 (200, HEIGHT * 3 / 4 - 600),
                 (100, HEIGHT * 3 / 4 - 500)]

SPRITESHEET = "plat_assets/spr_jum.png"
IM = pygame.image.load("plat_assets/ground_cake.png")
PLATFORM_IM = pygame.transform.scale(IM, (20, 20))
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
