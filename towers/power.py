import pygame

from towers.tower import Tower, load_image

pygame.init()


class PowerTower(Tower):
    main_img = pygame.transform.scale(
        load_image('data/towers/power/frame_00_delay-0.04s-removebg-preview.png', -1),
        (100, 170))
    attack_imgs = []
    for x in range(23):
        add_str = str(x)
        if x < 10:
            add_str = "0" + add_str
        attack_imgs.append(pygame.transform.scale(load_image(
            f"data/towers/power/attack/frame_" + add_str + "_delay-0.04s-removebg-preview.png", -1),
            (100, 170)))

    def __init__(self, x, y):
        super().__init__(x, y)
        self.main_img = PowerTower.main_img
        self.attack_imgs = PowerTower.attack_imgs[:]
        self.image = self.main_img
        self.rect = pygame.Rect(0, 0, self.image.get_width(), self.image.get_height())
        self.rect = self.rect.move(self.x - self.image.get_width() // 2,
                                   self.y - self.image.get_width() // 2 - 90)
        self.range = 250
        self.splash = False

        self.sell_price = [200, 500, 700]
        self.price = [200, 500, 700]
