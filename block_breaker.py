import pygame
from pygame.locals import *
import sys


class Block(pygame.sprite.Sprite):
    def __init__(self,file):
        self.image=pygame.image.load(file).convert_alpha()
        self.image=pygame.transform.scale(self.image,(100,50))
        self.rect=self.image.get_rect()
        self.rect.left=0
        self.rect.top=0

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Ball(pygame.sprite.Sprite):
    def __init__(self,file):
        self.image=pygame.image.load(file).convert_alpha()
        self.image=pygame.transform.scale(self.image,(25,25))
        self.rect=self.image.get_rect()
        self.rect.left=0
        self.rect.top=300

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Paddle(pygame.sprite.Sprite):
    def __init__(self,file):
        self.image=pygame.image.load(file).convert_alpha()
        self.image=pygame.transform.scale(self.image,(100,20))
        self.rect=self.image.get_rect()
        self.rect.left=0
        self.rect.top=350

    def draw(self, screen):
        screen.blit(self.image, self.rect)


def main():
    pygame.init()
    pygame.display.set_caption('ブロック崩し')
    screen = pygame.display.set_mode((400,400))
    screen.fill((0,0,0))
    block=Block('block.png')
    ball=Ball('ball.png')
    paddle=Paddle('paddle.png')

    while True:
        block.draw(screen)
        ball.draw(screen)
        paddle.draw(screen)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type==QUIT:
                exit()
            elif event.type==KEYDOWN:
                exit()

def exit():
    pygame.quit()
    sys.exit()

if __name__=="__main__":
    main()