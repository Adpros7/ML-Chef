import keyboard
import random
import pygame
from math import floor
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

pygame.init()
screen = pygame.display.set_mode((1200, 900))
clock = pygame.time.Clock()
font = pygame.font.Font('freesansbold.ttf', 32)


score = 0
health = 3


class Basketball(pygame.sprite.Sprite):
    def __init__(self, y: int):
        super().__init__()
        self.image = pygame.image.load("basketball.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect()
        self.speed = 5
        self.rect.y = y
        self.rect.x = random.randint(0, 1100)

    def reset(self, x: int, y: int):
        self.rect.x = x
        self.speed = min(5 + floor(score/5), 11)
        self.rect.y = y
        print(self.speed)

    def fall(self):
        self.rect.y += self.speed


class Hoop(Basketball, pygame.sprite.Sprite):
    def __init__(self):
        self.image = pygame.image.load("hoop.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (150, 150))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, 1050)
        self.rect.y = 800
        self.speed = basketball.speed

    def movement(self):
        if keyboard.is_pressed("right") and hoop.rect.x < 1063:
            hoop.rect.x += self.speed*2
        if keyboard.is_pressed("left") and hoop.rect.x > 10:
            hoop.rect.x -= self.speed*2

    def get_rectx(self):
        return self.rect.x


basketballList = []
num_balls = 2
max_diff = 300
for i in range(num_balls):
    basketball = Basketball(i*250)
    basketballList.append(basketball)
hoop = Hoop()

running = True
while running:
    screen.fill((255, 255, 255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    Hoop.movement(hoop)

    for i in range(num_balls):

        basketballList[i].fall()

        if basketballList[i].rect.colliderect(hoop.rect):
            score += 1
            hoopx = hoop.get_rectx()
            basketballList[i].reset(random.randint(
                max(hoopx-max_diff, 0), min(hoopx+max_diff, 1063)), random.randint(0, 300))

        if basketballList[i].rect.y > 900:
            hoopx = hoop.get_rectx()
            basketballList[i].reset(random.randint(
                max(hoopx-max_diff, 0), min(hoopx+max_diff, 1063)), random.randint(0, 300))
            health -= 1

        screen.blit(basketballList[i].image, basketballList[i].rect)
    screen.blit(hoop.image, hoop.rect)
    score_text = font.render(f'Score: {score}', True, (0, 0, 0))
    health_text = font.render(f'Health: {health}', True, (0, 0, 0))
    screen.blit(score_text, (600, 50))
    screen.blit(health_text, (600, 100))

    pygame.display.update()
    if health <= 0:
        endscreen = pygame.image.load("Losing.png").convert_alpha()
        endscreen = pygame.transform.scale(endscreen, (1200, 900))
        screen.blit(endscreen, (0, 0))
        pygame.display.update()
        while True:
            if keyboard.is_pressed("space"):
                score = 0
                health = 3
                for i in range(num_balls):
                    basketballList[i].reset(random.randint(0, 1100), i*250)
                hoop.rect.x = random.randint(0, 1050)
                screen.fill((255, 255, 255))
                break

            elif keyboard.is_pressed("escape"):
                pygame.quit()
                running = False
    clock.tick(100)
