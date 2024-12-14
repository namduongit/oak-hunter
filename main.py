import pygame
import random
import csv
import button
from settings import *
import Enemy

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
surface = pygame.Surface((WIDTH_MAP, HEIGHT_MAP))
logo_game = pygame.image.load('Map/Logo/logo_game.png').convert_alpha()
pygame.display.set_icon(logo_game)
pygame.display.set_caption("Oak Hunter")

# Bộ đếm thời gian cho màn hình
clock = pygame.time.Clock()

# Cài đặt phông chữ ThaleahFat
font = pygame.font.Font('Map/Font/ThaleahFat.ttf', 18)
# Biến dùng để người chơi có thể nâng cấp
speed_bullet = 0
dame_bullet = 0
health_bonus = 0
coin_player = 0
health_tile = 10
bullet_cooldown = 0
# Biến dùng để chơi game
home_game = True
play_game = False
option_game = False
exit_game = False
# Biến dùng khi win game
win_game = False
# Biến dùng trong map editor
current_tile = 0
scroll = 0
scroll_left = False
scroll_right = False
scroll_speed = 1
# Biến dùng để cuộn màn hình
screen_scroll = 0
bg_scroll = 0
level = 1

# Back ground trong game
img_1 = pygame.image.load('Map/Backgrounds/1.png').convert_alpha()
img_2 = pygame.image.load('Map/Backgrounds/2.png').convert_alpha()
img_3 = pygame.image.load('Map/Backgrounds/3.png').convert_alpha()
# Biến đổi background sao cho vừa màn hình (1024 x 512)
bg_1 = pygame.transform.scale(img_1, (SCREEN_WIDTH, SCREEN_HEIGHT))
bg_2 = pygame.transform.scale(img_2, (SCREEN_WIDTH, SCREEN_HEIGHT))
bg_3 = pygame.transform.scale(img_3, (SCREEN_WIDTH, SCREEN_HEIGHT))
# Bề mặt dùng trong map editor
layer_1 = pygame.image.load('Map/Backgrounds/1.png').convert_alpha()
layer_2 = pygame.image.load('Map/Backgrounds/2.png').convert_alpha()
layer_3 = pygame.image.load('Map/Backgrounds/3.png').convert_alpha()
layer_1 = pygame.transform.scale(layer_1, (WIDTH_MAP, HEIGHT_MAP))
layer_2 = pygame.transform.scale(layer_2, (WIDTH_MAP, HEIGHT_MAP))
layer_3 = pygame.transform.scale(layer_3, (WIDTH_MAP, HEIGHT_MAP))

empty_heath_bar = pygame.image.load('Entity/Player/assets/health_bar.png').convert_alpha()
chart_health = pygame.image.load('Entity/Player/assets/chart.png').convert_alpha()
board = pygame.image.load('Entity/Player/assets/board.png').convert_alpha()
bullet_image = pygame.image.load('Entity/Player/assets/bullet.png').convert_alpha()
bullet_image = pygame.transform.scale(bullet_image, (int(bullet_image.get_width() * 0.03), int(bullet_image.get_height() * 0.03)))
# board = pygame.transform.scale(board, (int(board.get_width() * 0.8), int(board.get_height() * 0.8)))
'''================================= Các ảnh ở cửa số chính ======================================='''
background = pygame.image.load('MainGame/main_game.png').convert_alpha()
background = pygame.transform.scale(background, (int(SCREEN_WIDTH), int(SCREEN_HEIGHT)))

# Cái ảnh settings của game dành cho player
setting_game_image = pygame.image.load('MainGame/settings_game.png').convert_alpha()
setting_game_image = pygame.transform.scale(setting_game_image, (350, 370))
victory_image = pygame.image.load('MainGame/wingame.png').convert_alpha()
victory_image = pygame.transform.scale(victory_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
'''================================================================================================'''

'''==================================== Các nút ở cửa sổ chính ===================================='''
play_btn = pygame.image.load('MainGame/button_action/PlayBtn.png').convert_alpha()
play_btn_hover = pygame.image.load('MainGame/button_action/PlayClick.png').convert_alpha()
play_btn = pygame.transform.scale(play_btn, (MAINBTN_WIDTH, MAINBTN_HEIGHT))
play_btn_hover = pygame.transform.scale(play_btn_hover, (MAINBTN_WIDTH, MAINBTN_HEIGHT))

exit_btn = pygame.image.load('MainGame/button_action/ExitBtn.png').convert_alpha()
exit_btn_hover = pygame.image.load('MainGame/button_action/ExitClick.png').convert_alpha()
exit_btn = pygame.transform.scale(exit_btn, (int(MAINBTN_WIDTH), int(MAINBTN_HEIGHT)))
exit_btn_hover = pygame.transform.scale(exit_btn_hover, (int(MAINBTN_WIDTH), int(MAINBTN_HEIGHT)))

option_btn = pygame.image.load('MainGame/button_action/OptBtn.png').convert_alpha()
option_btn_hover = pygame.image.load('MainGame/button_action/OptClick.png').convert_alpha()
option_btn = pygame.transform.scale(option_btn, (int(MAINBTN_WIDTH), int(MAINBTN_HEIGHT)))
option_btn_hover = pygame.transform.scale(option_btn_hover, (int(MAINBTN_WIDTH), int(MAINBTN_HEIGHT)))

play = button.Button(100, 120, play_btn, play_btn_hover, 1)
exit = button.Button(100, 120 + 10 + MAINBTN_HEIGHT, exit_btn, exit_btn_hover, 1)
option = button.Button(100, 120 + 10 * 2 + MAINBTN_HEIGHT * 2, option_btn, option_btn_hover, 1)
'''=================================================================================================='''

'''==================================== Các nút ở trong map editor ===================================='''
save_img = pygame.image.load('MainGame/button_action/save_btn.png').convert_alpha()
load_img = pygame.image.load('MainGame/button_action/load_btn.png').convert_alpha()

save_btn = button.Button(714, 416 - save_img.get_height() * 0.8, save_img, save_img, 0.8)
load_btn = button.Button(714 + save_img.get_width(),  416 - save_img.get_height() * 0.8, load_img, load_img, 0.8)
'''=================================================================================================='''

'''==================================== Các nút ở trong game ===================================='''
upgarde_dame = pygame.image.load('MainGame/button_action/dameBullet.png').convert_alpha()
upgrade_dame_hover = pygame.image.load('MainGame/button_action/dameHover.png').convert_alpha()
upgrade_health = pygame.image.load('MainGame/button_action/healthUpgrade.png').convert_alpha()
upgrade_health_hover = pygame.image.load('MainGame/button_action/healthHover.png').convert_alpha()
upgrade_speed_bullet = pygame.image.load('MainGame/button_action/speedBullet.png').convert_alpha()
upgrade_speed_bullet_hover = pygame.image.load('MainGame/button_action/speedHover.png').convert_alpha()
recover_health = pygame.image.load('MainGame/button_action/recoverHealth.png').convert_alpha()
recover_health_hover = pygame.image.load('MainGame/button_action/recoverHover.png').convert_alpha()
upgrade_cooldown = pygame.image.load('MainGame/button_action/cooldown.png').convert_alpha()
upgrade_cooldown_hover = pygame.image.load('MainGame/button_action/cooldownHover.png').convert_alpha()
dame_upgrade = button.Button(SCREEN_WIDTH - 50, 200, upgarde_dame, upgrade_dame_hover, 1)
health_upgrade = button.Button(SCREEN_WIDTH - 50, 250, upgrade_health, upgrade_health_hover, 1)
speed_bullet_upgrade = button.Button(SCREEN_WIDTH - 50, 300, upgrade_speed_bullet, upgrade_speed_bullet_hover, 1)
recover_health_upgrade = button.Button(SCREEN_WIDTH - 50, 350, recover_health, recover_health_hover, 1)
cooldown_upgrade = button.Button(SCREEN_WIDTH - 50, 400, upgrade_cooldown, upgrade_cooldown_hover, 1)

home = pygame.image.load('MainGame/button_action/home.png').convert_alpha()
home_hover = pygame.image.load('MainGame/button_action/homeHover.png').convert_alpha()
home_btn = button.Button(SCREEN_WIDTH - 40, SCREEN_HEIGHT - 40, home, home_hover, 1)

restartClick = pygame.image.load('MainGame/button_action/restartClick.png').convert_alpha()
restartHover = pygame.image.load('MainGame/button_action/restartHover.png').convert_alpha()
menuClick = pygame.image.load('MainGame/button_action/menuClick.png').convert_alpha()
menuHover = pygame.image.load('MainGame/button_action/menuHover.png').convert_alpha()

menu_btn = button.Button(SCREEN_WIDTH // 2 - 20 - restartClick.get_width(), SCREEN_HEIGHT // 2 - 100, menuClick, menuHover, 1)
restart_btn = button.Button(SCREEN_WIDTH // 2 + 20, SCREEN_HEIGHT // 2 - 100, restartClick, restartHover, 1)
'''=================================================================================================='''


'''================================== Các loại âm thanh trong game =================================='''
# Tiếng nhận tiền
coin_recieved = pygame.mixer.Sound('Audio/coin.wav')
coin_recieved.set_volume(0.3)
# Tiếng nhảy
jump_up = pygame.mixer.Sound('Audio/jump.wav')
jump_up.set_volume(0.3)
# Tiếng bắn súng
shooted = pygame.mixer.Sound('Audio/shot.wav')
shooted.set_volume(0.3)
# Tiếng đấm
punch_audio = pygame.mixer.Sound('Audio/punch.wav')
punch_audio.set_volume(0.3)
# Tiếng dao
slash_audio = pygame.mixer.Sound('Audio/slash.wav')
slash_audio.set_volume(0.3)
# Tiếng skeleton die
skeleton_hurt_audio = pygame.mixer.Sound('Audio/skeletondie.wav')
skeleton_hurt_audio.set_volume(0.3)
# Tiếng demon die
demon_hurt_audio = pygame.mixer.Sound('Audio/demondie.wav')
demon_hurt_audio.set_volume(0.3)
# Tiếng boss die
boss_hurt_audio = pygame.mixer.Sound('Audio/bossdie.wav')
boss_hurt_audio.set_volume(0.3)
# Tiếng thua game
lose_game_audio = pygame.mixer.Sound('Audio/game_over.wav')
lose_game_audio.set_volume(0.3)
# Tiếng thắng game
win_game_audio = pygame.mixer.Sound('Audio/win.wav')
win_game_audio.set_volume(0.3)

lose_game_audio_played = False # Dùng để check khi thua
win_game_audio_played = False # Dùng để check khi thắng
'''=================================================================================================='''
# Nhóm sprite
shop_group = pygame.sprite.Group()

trap_group = pygame.sprite.Group()

decoration_group = pygame.sprite.Group()

coin_group = pygame.sprite.Group()
level_complete_group = pygame.sprite.Group()

enemy_group = pygame.sprite.Group()

'''================================== Các class trong game ===================================='''
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, scale):
        pygame.sprite.Sprite.__init__(self)
        animation_types = ['Idle', 'Run', 'Jump', 'Hurt', 'Shot', 'Dead', 'Recharge', 'Walk']
        self.update_time = pygame.time.get_ticks()
        self.action = 0
        self.scale = scale
        self.frame_index = 0
        self.animation_list = []
        for animation in animation_types:
            sprite_sheet = pygame.image.load(f'Entity/Player/image/{animation}.png').convert_alpha()
            number_frames = sprite_sheet.get_width() // PLAYER_WIDTH
            temp_list = []
            for i in range(number_frames):
                frames = sprite_sheet.subsurface(i * PLAYER_WIDTH, 0, PLAYER_WIDTH, PLAYER_HEIGHT)
                frames = pygame.transform.scale(frames, (int(PLAYER_WIDTH * self.scale), int(PLAYER_HEIGHT * self.scale)))
                temp_list.append(frames)
            self.animation_list.append(temp_list)
        # Các biến giới hạn tối đa
        self.max_health = 150 + health_bonus
        self.max_bullet = 30
        self.dame = 20
        self.speed = 5
        self.direction = 1
        self.flip = False
        # Các biến khởi tạo
        self.health = self.max_health
        self.bullet = self.max_bullet
        # Biến dùng để di chuyển
        self.moving_left = False
        self.moving_right = False
        self.move_jump = False
        self.run = False
        self.in_air = False
        self.hurt = False
        self.shoot = False
        self.rechange = False
        self.vel_y = 0
        # Ảnh và vị trí của player
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        # Biến đợi chờ là hạnh phúc
        self.shoot_cooldown = 0
        # Biến kiếm tra va chạm
        self.width = self.rect.width
        self.height = self.rect.height
        self.collision_rect = pygame.Rect(self.rect.centerx - 10 * self.scale, self.rect.bottom - 20 * self.scale, 20 * self.scale, 20 * self.scale)
        self.coin_collision = pygame.Rect(self.rect.centerx - 10 * self.scale, self.rect.centery, 20 * self.scale, self.rect.height  // 2)
        # Nhóm đạn dược của người chơi
        self.bullets = pygame.sprite.Group()

    def update_action(self, new_action):
        if self.action != new_action:
            self.action = new_action
            self.frame_index = 0

    def update_animation(self):
        self.image = self.animation_list[self.action][self.frame_index]
        # ['Idle', 'Run', 'Jump', 'Hurt', 'Shot', 'Dead', 'Recharge', 'Walk', 'Punch']
        if pygame.time.get_ticks() - self.update_time > ANIMATION:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 5: # Dead
                self.frame_index = len(self.animation_list[self.action]) - 1
            elif self.action == 2: # Jump
                self.update_action(0)
            elif self.action == 3: # Hurt
                self.update_action(0)
                self.hurt = False
            elif self.action == 4: # Shot
                self.update_action(0)
                self.shoot = False
            elif self.action == 6: # Recharge
                self.bullet = self.max_bullet
                self.rechange = False
                self.update_action(0)
            else:
                self.frame_index = 0

    def move(self):
        screen_scroll = 0
        dx = 0
        dy = 0

        # Điều chỉnh theo hướng di chuyển
        if self.run:
            dx = (self.speed * self.direction) * 2
        if self.moving_right:
            dx = self.speed
            self.direction = 1
            self.flip = False
        if self.moving_left:
            dx = -self.speed
            self.direction = -1
            self.flip = True
        if self.move_jump and not self.in_air:
            self.vel_y = -12
            self.move_jump = False
            self.in_air = True

        # Thêm trọng lực
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y

        # Kiểm tra va chạm
        for tile in world.obstacle_list:
            # Trục x
            if tile[1].colliderect(self.collision_rect.x + dx, self.collision_rect.y, self.collision_rect.width, self.collision_rect.height):
                dx = 0
            # Trục y
            if tile[1].colliderect(self.collision_rect.x, self.collision_rect.y + dy, self.collision_rect.width, self.collision_rect.height):
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile[1].bottom - self.collision_rect.top
                elif self.vel_y >= 0:
                    self.vel_y = 0
                    self.in_air = False
                    dy = tile[1].top - self.collision_rect.bottom

        # Ngăn chặn đập đầu dô tường
        if self.collision_rect.left + dx < 0 or self.collision_rect.right + dx > SCREEN_WIDTH:
            dx = 0
        # Kiểm tra coi có bị rớt xuống vực không
        if self.coin_collision.top > SCREEN_HEIGHT:
            self.health = 0
            dy = 0

        # Cập nhật vị trí của collision_rect
        self.collision_rect.x += dx
        self.collision_rect.y += dy

        # Cập nhật vị trí của self.rect để đồng bộ hóa với collision_rect
        self.rect.centerx = self.collision_rect.centerx
        self.rect.bottom = self.collision_rect.bottom
        # Cập nhật ví trí của coin_collision
        self.coin_collision.x = self.rect.centerx - 10 * self.scale
        self.coin_collision.y = self.rect.centery

        # Cập nhật cuộn màn hình
        if (self.collision_rect.right > SCREEN_WIDTH - SCROLL_THRESH and bg_scroll < (world.level_length * TILE_SIZE) - SCREEN_WIDTH) or \
        (self.collision_rect.left < SCROLL_THRESH and bg_scroll > abs(dx)):
            self.collision_rect.x -= dx
            screen_scroll = -dx

        return screen_scroll

    def gun(self):
        if self.shoot_cooldown == 0 and self.bullet > 0:
            self.shoot_cooldown = 45 - bullet_cooldown
            bullet = Bullet(self.rect.centerx, self.rect.centery + 20 * self.scale, self.direction, self.flip)
            self.bullets.add(bullet)
            self.bullet -= 1

    def update(self):
        # ['Idle', 'Run', 'Jump', 'Hurt', 'Shot', 'Dead', 'Recharge', 'Walk', 'Punch']
        if self.health <= 0:
            self.health = 0
            self.update_action(5)
            self.hurt = False
            self.moving_left = False
            self.moving_right = False
            self.shoot = False
            self.move_jump = False
            self.in_air = False
            self.run = False
        else:
            if self.run:
                self.update_action(1)
            elif self.in_air:
                self.update_action(2)
            elif self.hurt:
                self.update_action(3)
            elif self.shoot:
                self.update_action(4)
                self.gun()
            elif self.rechange:
                self.update_action(6)
                # Tất cả hành động khác dừng lại
                self.moving_left = False
                self.moving_right = False
                self.move_jump = False
                self.run = False
                self.hurt = False
            elif self.moving_left or self.moving_right:
                self.update_action(7)
            else:
                self.update_action(0)
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

    def draw(self):
        self.update_animation()
        self.update()
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)
        for bullet in self.bullets:
            bullet.draw()
            bullet.update()

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, flip):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10 + speed_bullet
        self.image = pygame.image.load('Entity/Player/assets/1.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * 0.2), int(self.image.get_height() * 0.2)))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction
        if flip:
            self.image = pygame.transform.flip(self.image, True, False)

    def draw(self):
        self.rect.x += (self.direction * self.speed + speed_bullet) + screen_scroll
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()
        screen.blit(self.image, self.rect)
        # pygame.draw.rect(screen, 'Black', self.rect, 1)

class CoinBar(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.update_time = pygame.time.get_ticks()
        self.frame_index = 0
        self.animation_list = []
        sprite_sheet = pygame.image.load('Entity/Decoration/coin.png').convert_alpha()
        number_frames = sprite_sheet.get_width() // COIN_WIDTH
        for i in range(number_frames):
            frames = sprite_sheet.subsurface(i * COIN_WIDTH, 0, COIN_WIDTH, COIN_HEIGHT)
            frames = pygame.transform.scale(frames, (int(COIN_WIDTH * 1.5), int(COIN_HEIGHT * 1.5)))
            self.animation_list.append(frames)
        self.image = self.animation_list[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self):
        self.image = self.animation_list[self.frame_index]
        if pygame.time.get_ticks() - self.update_time > ANIMATION:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        if self.frame_index >= len(self.animation_list):
            self.frame_index = 0
        screen.blit(self.image, self.rect)


class Shop(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        sprite_sheet = pygame.image.load('Entity/Decoration/shop.png').convert_alpha()
        number_frames = sprite_sheet.get_width() // SHOP_WIDTH
        self.animation_list = []
        self.frame_index = 0
        for i in range(number_frames):
            frames = sprite_sheet.subsurface(i * SHOP_WIDTH, 0, SHOP_WIDTH, SHOP_HEIGHT)
            self.animation_list.append(frames)
        self.image = self.animation_list[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))
        self.update_time = pygame.time.get_ticks()

    def draw(self):
        self.image = self.animation_list[self.frame_index]
        if pygame.time.get_ticks() - self.update_time > ANIMATION:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
            if self.frame_index >= len(self.animation_list):
                self.frame_index = 0
        self.rect.x += screen_scroll
        screen.blit(self.image, self.rect)


class Decoration(pygame.sprite.Sprite):
    def __init__(self, type, img,  x, y):
        pygame.sprite.Sprite.__init__(self)
        if type != 1:
            self.image = pygame.image.load(f'Entity/Decoration/{type}.png').convert_alpha()
        else:
            self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))

    def draw(self):
        self.rect.x += screen_scroll
        screen.blit(self.image, self.rect)


class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        sprite_sheet = pygame.image.load('Entity/Decoration/coin.png').convert_alpha()
        self.animation_list = []
        number_frames = sprite_sheet.get_width() // COIN_WIDTH
        for i in range(number_frames):
            frames = sprite_sheet.subsurface(i * COIN_WIDTH, 0, COIN_WIDTH, COIN_HEIGHT)
            self.animation_list.append(frames)
        self.frame_index = 0
        self.image = self.animation_list[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))
        self.update_time = pygame.time.get_ticks()

    def draw(self):
        self.image = self.animation_list[self.frame_index]
        if pygame.time.get_ticks() - self.update_time > ANIMATION:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
            if self.frame_index >= len(self.animation_list):
                self.frame_index = 0
        self.rect.x += screen_scroll
        screen.blit(self.image, self.rect)

class NextLevel(pygame.sprite.Sprite):
    def __init__(self, x, y, img):
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self):
        self.rect.x += screen_scroll
        screen.blit(self.image, self.rect)

class Trap(pygame.sprite.Sprite):
    def __init__(self, type, x, y):
        # Có 4 loại theo 4 folder
        pygame.sprite.Sprite.__init__(self)
        folder = type
        number_frames = len(os.listdir(f'Entity/Trap/{folder}'))
        self.animation_list = []
        self.frame_index = 0
        for i in range(1, number_frames + 1):
            frames = pygame.image.load(f'Entity/Trap/{folder}/{i}.png')
            width = frames.get_width()
            height = frames.get_height()
            frames = pygame.transform.scale(frames, (int(width * 0.2), int(height * 0.2)))
            self.animation_list.append(frames)
        self.image = self.animation_list[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + TILE_SIZE // 2, y + (TILE_SIZE - self.image.get_height()))
        self.update_time = pygame.time.get_ticks()
        self.dame_cooldown = 0

    def draw(self):
        self.image = self.animation_list[self.frame_index]
        if pygame.time.get_ticks() - self.update_time > ANIMATION:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
            if self.frame_index >= len(self.animation_list):
                self.frame_index = 0
        if self.dame_cooldown > 0:
            self.dame_cooldown -= 1
        self.rect.x += screen_scroll
        screen.blit(self.image, self.rect)


''' ----------------------- Dữ liệu thế giới ----------------------- '''
class World:
    def __init__(self):
        self.obstacle_list = []

    def process_data(self, world_data):
        self.level_length = len(world_data[0])
        player = None
        for y, row in enumerate(world_data):
            for x, tile in enumerate(row):
                if tile >= 0:
                    img = img_list[tile]
                    img_rect = img.get_rect()
                    img_rect.x = x * TILE_SIZE
                    img_rect.y = y * TILE_SIZE
                    tile_data = (img, img_rect)  # Tuple
                    if (tile >= 0 and tile <= 4) or (tile >= 9 and tile <= 17) or (tile >= 19 and tile <= 20):
                        self.obstacle_list.append(tile_data)
                    elif tile == 22:
                        rock = Decoration('rock_1', img, img_rect.x, img_rect.y)
                        decoration_group.add(rock)
                    elif tile == 23:
                        rock = Decoration('rock_2', img, img_rect.x, img_rect.y)
                        decoration_group.add(rock)
                    elif tile == 24:
                        rock = Decoration('rock_3', img, img_rect.x, img_rect.y)
                        decoration_group.add(rock)
                    # Grass
                    elif tile == 25:
                        grass = Decoration('grass_1', img, img_rect.x, img_rect.y)
                        decoration_group.add(grass)
                    elif tile == 26:
                        grass = Decoration('grass_2', img, img_rect.x, img_rect.y)
                        decoration_group.add(grass)
                    elif tile == 27:
                        grass = Decoration('grass_3', img, img_rect.x, img_rect.y)
                        decoration_group.add(grass)
                    # Lamp
                    elif tile == 28:
                        lamp = Decoration('lamp', img, img_rect.x, img_rect.y)
                        decoration_group.add(lamp)
                    # Fence
                    elif tile == 29:
                        fence = Decoration('fence_1', img, img_rect.x, img_rect.y)
                        decoration_group.add(fence)
                    elif tile == 30:
                        fence = Decoration('fence_2', img, img_rect.x, img_rect.y)
                        decoration_group.add(fence)
                    elif tile == 31: # Shop
                        shop = Shop(img_rect.x, img_rect.y)
                        shop_group.add(shop)
                    # Next Level
                    elif tile == 32:
                        next_level = NextLevel(img_rect.x, img_rect.y, img)
                        level_complete_group.add(next_level)
                    elif tile == 33: # Skeleton
                        enemy = Enemy.Enemy('Skeleton', img_rect.x, img_rect.y, 1)
                        enemy_group.add(enemy)
                    elif tile == 34: # Player
                        player = Player(img_rect.x, img_rect.y, 0.75)
                    # Coin
                    elif tile == 35:
                        coin = Coin(img_rect.x, img_rect.y)
                        coin_group.add(coin)
                    elif tile == 36:
                        enemy = Enemy.Enemy('Bigger', img_rect.x, img_rect.y, 1)
                        enemy_group.add(enemy)
                    elif tile == 37:
                        enemy = Enemy.Enemy('Demon', img_rect.x, img_rect.y, 1)
                        enemy_group.add(enemy)
                    elif tile == 38:
                        enemy = Enemy.Enemy('Boss', img_rect.x, img_rect.y, 1)
                        enemy_group.add(enemy)
                    elif tile == 39:
                        traps = Trap('long_metal', img_rect.x, img_rect.y)
                        trap_group.add(traps)
                    elif tile == 40:
                        traps = Trap('long_wood', img_rect.x, img_rect.y)
                        trap_group.add(traps)
                    elif tile == 41:
                        traps = Trap('small_metal', img_rect.x, img_rect.y)
                        trap_group.add(traps)
                    elif tile == 42:
                        traps = Trap('small_wood', img_rect.x, img_rect.y)
                        trap_group.add(traps)
                    else:
                        decoration = Decoration(1, img, img_rect.x, img_rect.y)
                        decoration_group.add(decoration)

        return player

    def draw(self):
        for tile in self.obstacle_list:
            tile[1].x += screen_scroll
            screen.blit(tile[0], tile[1])

''' ----------------------- Chuẩn bị thành phần cho main game -----------------------'''
# Tạo mảng lưu các tile trong map
img_list = []
for i in range(TILE_TYPES):
    img = pygame.image.load(f'Map/Tile/{i}.png').convert_alpha()
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    img_list.append(img)

# Lưu trữ các nút trong map editor
button_list = []
button_col = 0
button_row = 0
for i in range(len(img_list)):
	tile_button = button.Button(WIDTH_MAP + 10 + button_col * TILE_SIZE + button_col * 10, 10 + button_row * TILE_SIZE + button_row * 10, img_list[i], img_list[i], 1)
	button_list.append(tile_button)
	button_col += 1
	if button_col == 7:
		button_row += 1
		button_col = 0

# Tạo mảng data rỗng dùng để chứa dữ liệu thế giới
world_data = []
for row in range(ROWS):
    r = [-1] * COLS
    world_data.append(r)
# Đọc dữ liệu lên mảng vừa tạo
with open(f'Level/level{level}_data.csv', newline = '') as csvfile:
    reader = csv.reader(csvfile, delimiter = ',')
    for x, row in enumerate(reader):
        for y, tile in enumerate(row):
            world_data[x][y] = int(tile)




# Hàm vẽ chữ
def draw_text(text, font, color, x, y):
    # Transform string to img
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

# Hàm vẽ background để tạo hiệu ứng 3D dựa trên các layer
def draw_bg():
    width = bg_1.get_width()
    for i in range(20):
        screen.blit(bg_1, ((i * width) - bg_scroll * 0.5, 0))
        screen.blit(bg_2, ((i * width) - bg_scroll * 0.6, 0))
        screen.blit(bg_3, ((i * width) - bg_scroll * 0.7, 0))

# Dùng để reset level khi chơi lại hoặc qua màn mới
def reset_level():
    # Tạo lại mảng rỗng
    data = []
    for row in range(ROWS):
        r = [-1] * COLS
        data.append(r)
    return data

def reset_data():
    global coin_player
    decoration_group.empty()
    shop_group.empty()
    coin_group.empty()
    enemy_group.empty()
    level_complete_group.empty()
    trap_group.empty()
    coin_player = 0

def draw_enemy(player):
    for enemy in enemy_group:
        enemy.draw(player, screen, screen_scroll, world)
        if enemy.attack == True and enemy.dame_cooldown == 90:
            if enemy.type == 'Skeleton' or enemy.type == 'Demon':
                slash_audio.play()
            else:
                punch_audio.play()

def draw_group(player):
    for decoration in decoration_group:
        decoration.draw()
    for next_level in level_complete_group:
        next_level.draw()
    for shop in shop_group:
        shop.draw()
    for coin in coin_group:
        coin.draw()
    for trap in trap_group:
        trap.draw()
        if trap.rect.colliderect(player.coin_collision):
            if trap.dame_cooldown == 0:
                player.health -= 10
                trap.dame_cooldown = 20

def draw_chart(player):
    screen.blit(empty_heath_bar, (10, 10))
    draw_text(f'x {coin_player}', font, WHITE, 15 + CoinBarPlayer.image.get_width(), 79)
    number_tiles = player.health // health_tile
    step = 0
    for i in range(number_tiles):
        if i  == 5:
            step = 10
        if i == 10:
            step = 21
        screen.blit(chart_health, (76 + i * 16 + step, 33))
    for i in range(player.bullet):
        screen.blit(bullet_image, (10 + i * 10, 100))



def bullet_enemy(player):
    for bullet in player.bullets:
        for enemy in enemy_group:
            if bullet.rect.colliderect(enemy.collision_rect):
                if enemy.health > 0:
                    enemy.health -= player.dame + dame_bullet
                    if enemy.health <= 0:
                            if enemy.type == 'Skeleton' or enemy.type == 'Bigger':
                                skeleton_hurt_audio.play()
                            elif enemy.type == 'Demon':
                                demon_hurt_audio.play()
                            else:
                                boss_hurt_audio.play()
                    if random.randint(1, 3) == 1:
                        enemy.hurt = True
                    player.bullets.remove(bullet)

def check_enmy_alive():
    number_of_enemy = 0
    for enemy in enemy_group:
        if enemy.health == 0:
            number_of_enemy += 1
    return number_of_enemy == len(enemy_group)

def coin_collision(player):
    global coin_player
    for coin in coin_group:
        if coin.rect.colliderect(player.coin_collision):
            coin_group.remove(coin)
            coin_player += 1
            coin_recieved.play()

def shop_collision(player):
    for shop in shop_group:
        if shop.rect.colliderect(player.coin_collision):
            # Hiển thị bảng cửa hàng
            screen.blit(board, (870, 10))
            draw_text('Info Player', font, 'White', 900, 20)
            draw_text(f'Health: {player.health}', font, 'White', 880, 50)
            draw_text(f'Max Health: {player.max_health}', font, 'White', 880, 75)
            draw_text(f'Bullet Speed: {speed_bullet}', font, 'White', 880, 105)
            draw_text(f'Damage Bonus: {dame_bullet}', font, 'White', 880, 135)
            draw_text(f'Cooldown: {bullet_cooldown}', font, 'White', 880, 165)

            # Thêm thông tin trên mỗi nút
            pygame.draw.rect(screen, "Black", (SCREEN_WIDTH - 255, 200, 200, 30))
            draw_text("+ 1 Damage Bullet: 2 xu", font, "White", SCREEN_WIDTH - 250, 205)
            if dame_upgrade.draw(screen):
                handle_upgrade("dame", player)
            pygame.draw.rect(screen, "Black", (SCREEN_WIDTH - 255, 250, 200, 30))
            draw_text("+ 15 Health: 2 xu", font, "White", SCREEN_WIDTH - 250, 255)
            if health_upgrade.draw(screen):
                handle_upgrade("health", player)
            pygame.draw.rect(screen, "Black", (SCREEN_WIDTH - 255, 300, 200, 30))
            draw_text("+ Bullet Speed: 1 xu", font, "White", SCREEN_WIDTH - 250, 305)
            if speed_bullet_upgrade.draw(screen):
                handle_upgrade("speed_bullet", player)
            pygame.draw.rect(screen, "Black", (SCREEN_WIDTH - 255, 350, 200, 30))
            draw_text("Recover Health: 1 xu", font, "White", SCREEN_WIDTH - 250, 355)
            if recover_health_upgrade.draw(screen):
                handle_upgrade("recover_health", player)
            pygame.draw.rect(screen, "Black", (SCREEN_WIDTH - 255, 400, 200, 30))
            draw_text("- Cooldown Bullet: 1 xu", font, "White", SCREEN_WIDTH - 250, 405)
            if cooldown_upgrade.draw(screen):
                handle_upgrade("cooldown", player)

def handle_upgrade(upgrade_type, player):
    """
    Xử lý logic nâng cấp dựa trên loại nâng cấp.
    """
    global coin_player, dame_bullet, speed_bullet, bullet_cooldown, max_health_current, health_tile
    if upgrade_type == "dame" and coin_player >= 2:
        dame_bullet += 1
        coin_player -= 2
    elif upgrade_type == "health" and coin_player >= 2:
        player.max_health += 15
        health_tile += 1
        coin_player -= 2
    elif upgrade_type == "speed_bullet" and coin_player >= 1 and speed_bullet < 5:
        speed_bullet += 1
        coin_player -= 1
    elif upgrade_type == "recover_health" and coin_player >= 1:
        player.health = player.max_health
        coin_player -= 1
    elif upgrade_type == "cooldown" and coin_player >= 1 and bullet_cooldown < 35:
        bullet_cooldown += 1
        coin_player -= 1


world = World()
player = world.process_data(world_data)

'''Map editor'''

'''Map editor'''
def map_editor():
    action_edit = True
    global current_tile
    global scroll
    global scroll_left
    global scroll_right
    global scroll_speed
    global home_game
    global level
    global MAX_LEVELS
    global player
    screen.fill(GRAY)
    # Chỗ này dùng để vẽ chữ nè
    draw_text(f'Current Level: {level}', font, WHITE, 10, HEIGHT_MAP + 5)
    draw_text(f'Curent Tile: {current_tile}', font, WHITE, 10, HEIGHT_MAP + 20)
    draw_text('Press UP/DOWN to change level', font, WHITE, 10, HEIGHT_MAP + 35)
    draw_text('Press LEFT/RIGHT to scroll map', font, WHITE, 10, HEIGHT_MAP + 50)
    draw_text('Press ESC to return to main menu', font, BLACK, 10, HEIGHT_MAP + 65)
    # Vẽ cái nền chỗ cso thể thêm tile vào map
    num_tiles = (COLS * TILE_SIZE) // WIDTH_MAP + 1
    for i in range(num_tiles):
        surface.blit(layer_1, ((i * WIDTH_MAP) - scroll * 0.5, 0))
        surface.blit(layer_2, ((i * WIDTH_MAP) - scroll * 0.6, 0))
        surface.blit(layer_3, ((i * WIDTH_MAP) - scroll * 0.7, 0))
    # Vẽ cái lưới chỗ map
    for i in range(ROWS + 1):
        pygame.draw.line(surface, (255, 255, 255), (0, i * TILE_SIZE_MAP ), (WIDTH_MAP, i * TILE_SIZE_MAP))
    for j in range(COLS + 1):
        pygame.draw.line(surface, (255, 255, 255), (j * TILE_SIZE_MAP - scroll, 0), (j * TILE_SIZE_MAP - scroll, HEIGHT_MAP))
    # Vẽ thế giới vào trong chỗ map
    for y, row in enumerate(world_data):
        for x, tile in enumerate(row):
            if tile >= 0:
                surface.blit(img_list[tile], (x * TILE_SIZE_MAP - scroll, y * TILE_SIZE_MAP))

    # Nút load mop
    if load_btn.draw(screen):
        scroll = 0
        with open(f'Level/level{level}_data.csv', newline = '') as csvfile:
            reader = csv.reader(csvfile, delimiter = ',')
            for x, row in enumerate(reader):
                for y, tile in enumerate(row):
                    world_data[x][y] = int(tile)
    # Nút lưu map
    if save_btn.draw(screen):
        with open(f'Level/level{level}_data.csv', 'w', newline = '') as csvfile:
            writer = csv.writer(csvfile, delimiter = ',')
            for row in world_data:
                writer.writerow(row)
    # Vẽ mấy cái nút bên trái màn hình
    button_count = 0
    for button_count, i in enumerate(button_list):
        if i.draw(screen):
            current_tile = button_count
    # Tô đậm nút ấn hiện tại
    pygame.draw.rect(screen, RED, button_list[current_tile].rect, 3)

    # Di chuyển bản đồ
    if scroll_left == True and scroll > 0:
        scroll -= 5 * scroll_speed
    if scroll_right == True and scroll < (COLS * TILE_SIZE_MAP) - WIDTH_MAP:
        scroll += 5 * scroll_speed

    pos = pygame.mouse.get_pos()
    x = (pos[0] + scroll) // TILE_SIZE_MAP
    y = pos[1] // TILE_SIZE_MAP
    # Kiểm tra xem chuột có nằm trong vùng vẽ không
    if pos[0] < (704) and pos[1] < (416):
        # Cập nhật tile vào world data
        if pygame.mouse.get_pressed()[0] == 1:
            if world_data[y][x] != current_tile:
                world_data[y][x] = current_tile
        if pygame.mouse.get_pressed()[2] == 1:
            world_data[y][x] = -1

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                scroll_left = True
            if event.key == pygame.K_RIGHT:
                scroll_right = True
            if event.key == pygame.K_UP and level < MAX_LEVELS:
                level += 1
            if event.key == pygame.K_DOWN and level > 1:
                level -= 1
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                scroll_left = False
            if event.key == pygame.K_RIGHT:
                scroll_right = False
        # Exit map editor
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                action_edit = False
                # Cập nhật lại dữ liệu thế giới
                world = reset_level()
                reset_data()
                world = World()
                player = world.process_data(world_data)
                home_game = True
        # Exit pygame
        if event.type == pygame.QUIT:
            pygame.quit()
    # Update to screen
    screen.blit(surface, (0, 0))

    return action_edit, home_game

'''Gangster ở cửa sổ chính'''
GangsterMain = Player(835, 325, 1.5)
CoinBarPlayer = CoinBar(10, 74)
# Vòng lặp chính
running = True
while running:
    # Cài đặt FPS
    clock.tick(FPS)
    if home_game:
        screen.blit(background, (0, 0))
        pygame.draw.rect(screen, 'Black', (510, 48, 354, 374))
        screen.blit(setting_game_image, (512, 50))
        GangsterMain.draw()
        if play.draw(screen):
            home_game = False
            play_game = True
        if option.draw(screen):
            home_game = False
            option_game = True
        if exit.draw(screen):
            home_game = False
            exit_game = True

    else:
        if option_game:
            option_game, main_game = map_editor()
        if exit_game:
            running = False
        if play_game:
            if win_game:
                screen.blit(victory_image, (0, 0))
                if win_game_audio_played == False:
                    win_game_audio.play()
                    win_game_audio_played = True
                if menu_btn.draw(screen):
                    level = 1
                    bg_scroll = 0
                    home_game = True
                    win_game_audio_played = False
                    lose_game_audio_played = False
                    win_game = False
                    world_data = reset_level()
                    reset_data()
                    # Tải level mới khi ra khỏi màn hình chính
                    with open(f'Level/level{level}_data.csv', newline = '') as csvfile:
                        reader = csv.reader(csvfile, delimiter = ',')
                        for x, row in enumerate(reader):
                            for y, tile in enumerate(row):
                                world_data[x][y] = int(tile)
                    world = World()
                    player = world.process_data(world_data)
                if restart_btn.draw(screen):
                    level = 1
                    bg_scroll = 0
                    win_game_audio_played = False
                    lose_game_audio_played = False
                    win_game = False
                    world_data = reset_level()
                    reset_data()
                    # Tải level mới và chơi lại luôn
                    with open(f'Level/level{level}_data.csv', newline = '') as csvfile:
                        reader = csv.reader(csvfile, delimiter = ',')
                        for x, row in enumerate(reader):
                            for y, tile in enumerate(row):
                                world_data[x][y] = int(tile)
                    world = World()
                    player = world.process_data(world_data)
            else:
                # Nếu người chơi tồn tại thì mới vẽ
                if player:
                    draw_bg()
                    world.draw()
                    draw_group(player)
                    # coin_group.update(screen_scroll)
                    CoinBarPlayer.draw()
                    draw_enemy(player)
                    draw_chart(player)
                    bullet_enemy(player)
                    player.draw()
                    screen_scroll = player.move()
                    bg_scroll -= screen_scroll

                    # Collision_coin
                    coin_collision(player)
                    # Collision_shop
                    shop_collision(player)

                # Lấy sự kiện từ người chơi
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            running = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_a:
                            player.moving_left = True
                        if event.key == pygame.K_d:
                            player.moving_right = True
                        if event.key == pygame.K_w and player.in_air == False:
                            player.move_jump = True
                            jump_up.play()
                        if event.key == pygame.K_r:
                            player.rechange = True
                        if event.key == pygame.K_SPACE:
                            if player.shoot_cooldown == 0 and player.bullet > 0:
                                player.shoot = True
                                shooted.play()
                        if event.key == pygame.K_LCTRL:
                            player.run = True
                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_a:
                            player.moving_left = False
                        if event.key == pygame.K_d:
                            player.moving_right = False
                        if event.key == pygame.K_w:
                            player.move_jump = False
                        if event.key == pygame.K_r:
                            player.rechange = False
                        if event.key == pygame.K_LCTRL:
                            player.run = False
                # Vẽ cái nút quay về home nếu người chơi muốn ra ngoài nhưng vẫn giữ level hiện tại
                if home_btn.draw(screen):
                    bg_scroll = 0
                    home_game = True
                    play_game = False
                    # Reset lại dữ liệu thế giới
                    world_data = reset_level()
                    reset_data() # Để tránh khi vô lại bị x2 quái
                    with open(f'Level/level{level}_data.csv', newline = '') as csvfile:
                        reader = csv.reader(csvfile, delimiter = ',')
                        for x, row in enumerate(reader):
                            for y, tile in enumerate(row):
                                world_data[x][y] = int(tile)
                    world = World()
                    player = world.process_data(world_data)
                # Kiểm tra khi va chạm với cục chuyển tới level tiếp theo
                for pos in level_complete_group:
                    if player.coin_collision.colliderect(pos.rect) and check_enmy_alive():
                        level += 1
                        if level <= MAX_LEVELS:
                            bg_scroll = 0
                            world_data = reset_level()
                            reset_data()
                            # Tải level mới vào world data
                            with open(f'Level/level{level}_data.csv', newline = '') as csvfile:
                                reader = csv.reader(csvfile, delimiter = ',')
                                for x, row in enumerate(reader):
                                    for y, tile in enumerate(row):
                                        world_data[x][y] = int(tile)
                            world = World()
                            player = world.process_data(world_data)
                        elif level == MAX_LEVELS + 1:
                            win_game = True
                # Kiểm tra sự sống chết của người chơi
                if player.health <= 0:
                    if lose_game_audio_played == False:
                        lose_game_audio.play()
                        lose_game_audio_played = True
                    if menu_btn.draw(screen):
                        level = 1
                        bg_scroll = 0
                        home_game = True
                        win_game_audio_played = False
                        lose_game_audio_played = False
                        win_game = False
                        world_data = reset_level()
                        reset_data()
                        # Tải level mới khi ra khỏi màn hình chính
                        with open(f'Level/level{level}_data.csv', newline = '') as csvfile:
                            reader = csv.reader(csvfile, delimiter = ',')
                            for x, row in enumerate(reader):
                                for y, tile in enumerate(row):
                                    world_data[x][y] = int(tile)
                        world = World()
                        player = world.process_data(world_data)
                    if restart_btn.draw(screen):
                        # Không reset level để được chơi lại màn đó
                        bg_scroll = 0
                        win_game_audio_played = False
                        lose_game_audio_played = False
                        win_game = False
                        world_data = reset_level()
                        reset_data()
                        # Tải level mới và chơi lại luôn
                        with open(f'Level/level{level}_data.csv', newline = '') as csvfile:
                            reader = csv.reader(csvfile, delimiter = ',')
                            for x, row in enumerate(reader):
                                for y, tile in enumerate(row):
                                    world_data[x][y] = int(tile)
                        world = World()
                        player = world.process_data(world_data)


    # Vòng lặp lấy sự kiện bên ngoài
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    # Cập nhật lại màn hình
    pygame.display.update()

pygame.quit()