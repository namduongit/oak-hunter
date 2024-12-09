import random
import pygame
from settings import *


class Enemy(pygame.sprite.Sprite):
    def __init__(self, type, x, y, scale):
        pygame.sprite.Sprite.__init__(self)
        # Cài đặt hình ảnh cho quái vật
        self.type = type
        animation_types = ['Idle', 'Walk', 'Attack', 'Die', 'Hurt']
        folder_path = f'Entity/{self.type}'
        self.update_time = pygame.time.get_ticks()
        self.action = 0
        self.frame_index = 0
        self.animation_list = []
        for animation in animation_types:
            temp_list = []
            number_frames = len(os.listdir(f'{folder_path}/{animation}'))
            for i in range(1, number_frames + 1):
                frames = pygame.image.load(f'{folder_path}/{animation}/{i}.png').convert_alpha()
                frames = pygame.transform.scale(frames, (int(frames.get_width() * scale), int(frames.get_height() * scale)))
                temp_list.append(frames)
            self.animation_list.append(temp_list)
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.width = self.rect.width
        self.height = self.rect.height
        # Các biến khởi tạo
        if self.type == 'Skeleton':
            self.health = 100
            self.dame = 10
            self.vision = pygame.Rect(0, 0, 100, self.height)
            self.vision_width = 100
        elif self.type == 'Bigger':
            self.health = 150
            self.dame = 20
            self.vision = pygame.Rect(0, 0, 200, self.height)
            self.vision_width = 200
        elif self.type == 'Demon':
            self.health = 500
            self.dame = 50
            self.vision_width = 200
            self.vision = pygame.Rect(0, 0, 300, self.height)
            self.vision_width = 300
        elif self.type == 'Boss':
            self.health = 1000
            self.dame = 100
            self.vision = pygame.Rect(0, 0, 400, self.height)
            self.vision_width = 400
        self.speed = 1
        self.direction = 1
        self.flip = False
        # Các biến dùng để di chuyển
        self.moving_left = False
        self.moving_right = False
        self.attack = False
        self.hurt = False
        self.vel_y = 0
        # Biến chờ đợi là hành phúc
        self.dame_cooldown = 0
        # Biến dành cho ai
        self.move_counter = 0
        self.idling = False
        self.idling_counter = 0
        # Biến kiểm tra va chạm
        self.collision_rect = pygame.Rect(self.rect.centerx - 5 * scale, self.rect.centery - 10 * scale, 10 * scale, 42 * scale)

    def update_action(self, new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0

    def update_animation(self):
        self.image = self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > ANIMATION:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 3: # Die
                self.frame_index = len(self.animation_list[self.action]) - 1
            elif self.action == 4: # Hurt
                self.update_action(0)
                self.hurt = False
            elif self.action == 2: # Attack
                self.update_action(0)
                self.attack = False
            else:
                self.frame_index = 0

    def move(self, world):
        dx = 0
        dy = 0

        # Điều chỉnh theo hướng di chuyển
        if self.moving_right:
            dx = self.speed
            self.direction = 1
            self.flip = False
        if self.moving_left:
            dx = -self.speed
            self.direction = -1
            self.flip = True
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
                self.direction *= -1
                self.move_counter += 1
            # Trục y
            if tile[1].colliderect(self.collision_rect.x, self.collision_rect.y + dy, self.collision_rect.width, self.collision_rect.height):
                if self.vel_y < 0:
                    self.vel_y = 0
                    dy = tile[1].bottom - self.collision_rect.top
                elif self.vel_y >= 0:
                    self.vel_y = 0
                    dy = tile[1].top - self.collision_rect.bottom

        if self.rect.top > SCREEN_HEIGHT:
            self.health = 0
            dy = 0
        # Cập nhật vị trí của collision_rect
        self.collision_rect.x += dx
        self.collision_rect.y += dy

        # Cập nhật vị trí của self.rect để đồng bộ hóa với collision_rect
        self.rect.centerx = self.collision_rect.centerx
        self.rect.bottom = self.collision_rect.bottom

    def ai(self, player, screen_scroll, world):
        # Cập nhật tầm nhìn
        if self.direction == -1:
            self.vision.x = self.rect.centerx + self.vision_width * self.direction
        else:
            self.vision.x = self.rect.centerx
        self.vision.y = self.rect.y
        if self.health > 0:
            if self.vision.colliderect(player.rect) and player.health > 0:
                self.idling = True
                self.idling_counter = 10
                self.speed = 2
                if abs(self.rect.centerx - player.rect.centerx) > 30:
                    if self.rect.centerx > player.rect.centerx:
                        self.moving_left = True
                        self.moving_right = False
                    else:
                        self.moving_left = False
                        self.moving_right = True
                    self.move(world)
                else:
                    if abs(self.rect.centery - player.rect.centery) <= 30:
                        self.moving_left = False
                        self.moving_right = False
                        self.attack = True
                        if self.attack == True:
                            if self.dame_cooldown == 0:
                                player.health -= self.dame
                                self.dame_cooldown = 100
                                if random.randint(1, 3) == 1:
                                    player.hurt = True
            else:
                self.speed = 1
            if not self.idling and random.randint(1, 200) == 1:
                self.idling = True
                self.idling_counter = random.randint(60, 300)
                self.moving_left = False
                self.moving_right = False
            else:
                if not self.idling:
                    if self.direction == 1:
                        self.moving_right = True
                        self.moving_left = False
                    else:
                        self.moving_right = False
                        self.moving_left = True
                    self.move(world)
                    self.move_counter += 1
                    if self.move_counter > 32:
                        self.direction *= -1
                        self.move_counter *= -1
                else:
                    self.idling_counter -= 1
                    if self.idling_counter <= 0:
                        self.idling = False

        self.rect.x += screen_scroll
        self.collision_rect.x += screen_scroll

    def update(self):
        # ['Idle', 'Walk', 'Attack', 'Die', 'Hurt']
        if self.health <= 0:
            self.health = 0
            self.update_action(3)
            self.hurt = False
            self.moving_left = False
            self.moving_right = False
            self.attack = False
        else:
            if self.moving_left or self.moving_right:
                self.update_action(1)
            elif self.attack:
                self.update_action(2)
            elif self.hurt:
                self.update_action(4)
            else:
                self.update_action(0)
        if self.dame_cooldown > 0:
            self.dame_cooldown -= 1

    def draw(self, player, screen, screen_scroll, world):
        self.update()
        self.update_animation()
        self.ai(player, screen_scroll, world)
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)

















        # pygame.draw.rect(screen, 'Red', self.collision_rect, 1)
        # pygame.draw.rect(screen, 'Black', self.rect, 1)
        # pygame.draw.rect(screen, 'Yellow', self.vision, 1)