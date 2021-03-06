import os

import pygame

towers_sprites = pygame.sprite.Group()


# function collide rect and circle
def intersects(rect, r, center):
    circle_distance_x = abs(center[0] - rect.centerx)
    circle_distance_y = abs(center[1] - rect.centery)
    if circle_distance_x > rect.w / 2.0 + r or circle_distance_y > rect.h / 2.0 + r:
        return False
    if circle_distance_x <= rect.w / 2.0 or circle_distance_y <= rect.h / 2.0:
        return True
    corner_x = circle_distance_x - rect.w / 2.0
    corner_y = circle_distance_y - rect.h / 2.0
    corner_distance_sq = corner_x ** 2.0 + corner_y ** 2.0
    return corner_distance_sq <= r ** 2.0


class Tower(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(towers_sprites)
        # property rect
        self.x = x
        self.y = y
        self.width = 0
        self.height = 0
        # prices
        self.sell_price = [0, 0, 0]
        self.price = [0, 0, 0]
        self.level = 0
        # base attributes
        self.selected = True
        self.main_img = None
        self.damage = 1
        self.range = 0
        self.archer_count = 0
        self.attack_imgs = []
        self.is_attack = False
        self.splash = False

    def attack(self, enemies):
        # try to attack enemies
        add_money = 0
        if self.is_attack:
            enemy_closest = []
            for enemy in enemies:
                if intersects(enemy.hit_box, self.range, (self.x, self.y)):
                    if self.archer_count == len(self.attack_imgs) - 1:
                        enemy_closest.append(enemy)
                        if not self.splash:
                            if enemy.hit(self.damage):
                                add_money += enemy.money_for_kill
                                enemies.remove(enemy)
                            self.archer_count = 0
            if not enemy_closest:
                self.is_attack = False
            if self.splash:
                for enemy in enemy_closest:
                    if enemy.hit(self.damage):
                        add_money += enemy.money_for_kill
                        enemies.remove(enemy)
                    self.archer_count = 0
        return add_money

    def update(self, enemies):
        # draw animation
        for enemy in enemies:
            if intersects(enemy.hit_box, self.range, (self.x, self.y)):
                self.is_attack = True
        if self.is_attack:
            self.image = self.attack_imgs[self.archer_count]
            self.archer_count = (self.archer_count + 1) % len(self.attack_imgs)
        else:
            self.image = self.main_img

    def draw_radius(self, win):
        # draw attack radius
        surface = pygame.Surface((self.range * 2, self.range * 2), pygame.SRCALPHA)
        pygame.draw.circle(surface, (128, 128, 128, 120), (self.range, self.range), self.range, 0)
        win.blit(surface, (self.x - self.range, self.y - self.range))

    def collide(self, wind, x, y):
        # pygame.draw.rect(wind, (255, 255, 255), (self.rect), 10)
        return self.rect.collidepoint(x, y)


# base func
def load_image(name, colorkey=None):
    pygame.init()
    fullname = os.path.join(name)
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image
