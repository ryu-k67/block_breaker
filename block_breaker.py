import random
import pygame
from pygame.locals import *
import sys



SCREEN=Rect(0,0,400,600)

class Block(pygame.sprite.Sprite):
    def __init__(self,file,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load(file).convert_alpha()
        self.image=pygame.transform.scale(self.image,(SCREEN.width/6,SCREEN.height*0.4/8))
        self.rect=self.image.get_rect()
        self.rect.left=x*self.rect.width
        self.rect.top=y*self.rect.height

    def draw(self, screen):
        screen.blit(self.image, self.rect)



class Ball(pygame.sprite.Sprite):
    def __init__(self,file,blocks,paddle):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load(file).convert_alpha()
        self.image=pygame.transform.scale(self.image,(25,25))
        self.rect=self.image.get_rect()
        self.blocks=blocks
        self.paddle=paddle
        self.update=self.start

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def start(self):
        self.rect.centerx=self.paddle.rect.centerx
        self.rect.bottom=self.paddle.rect.top
        # self.dx=random.uniform(-10,10)
        self.dx=0
        self.dy=-10
        
    def change(self):
        self.update=self.move

    def move(self):
        self.rect.centerx+=self.dx
        self.rect.centery+=self.dy

        if self.rect.left<SCREEN.left:
            self.rect.left=SCREEN.left
            self.dx=-self.dx
        if self.rect.top<SCREEN.top:
            self.rect.top=SCREEN.top
            self.dy=-self.dy
        if self.rect.right>SCREEN.right:
            self.rect.right=SCREEN.right
            self.dx=-self.dx
        
        if self.rect.colliderect(self.paddle.rect):
            self.dy=-self.dy
            self.dx=self.dx+(self.rect.centerx-self.paddle.rect.centerx)/10
            if self.dx>15:
                self.dx=15
            elif self.dx<-15:
                self.dx=-15
            self.rect.bottom=self.paddle.rect.top-1
        
        if self.rect.bottom>SCREEN.bottom:
            self.update=self.start

        vanish_blocks=pygame.sprite.spritecollide(self,self.blocks,True)

        if vanish_blocks:
            for block in vanish_blocks:
                if self.rect.top<block.rect.bottom and self.rect.bottom>block.rect.bottom:#下から
                    self.rect.top=block.rect.bottom
                    self.dy=-self.dy
                if self.rect.top>block.rect.top and self.rect.bottom<block.rect.top:#上から
                    self.rect.bottom=block.rect.top
                    self.dy=-self.dy
                if self.rect.left>block.rect.left and self.rect.right<block.rect.left:#左から
                    self.rect.right=block.rect.left
                    self.dx=-self.dx
                if self.rect.right<block.rect.right and self.rect.left>block.rect.right:#右から
                    self.rect.left=block.rect.right
                    self.dx=-self.dx

        self.rect.clamp_ip(SCREEN)



class Paddle(pygame.sprite.Sprite):
    def __init__(self,file):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load(file).convert_alpha()
        self.image=pygame.transform.scale(self.image,(100,20))
        self.rect=self.image.get_rect()
        self.rect.bottom=SCREEN.bottom
        self.rect.centerx=int(SCREEN.width/2)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def move(self):
        self.rect.centerx=pygame.mouse.get_pos()[0]
        self.rect.clamp_ip(SCREEN)




def main():
    pygame.init()
    pygame.display.set_caption('ブロック崩し')
    screen = pygame.display.set_mode(SCREEN.size)
    screen.fill((0,0,0))

    clock = pygame.time.Clock()

    blocks=pygame.sprite.Group()
    for ball_x in range(6):
        for ball_y in range(8):
            block=Block('block.png',ball_x,ball_y)
            blocks.add(block)
    paddle=Paddle('paddle.png')
    ball=Ball('ball.png',blocks,paddle)

    while True:

        clock.tick(60)

        screen.fill((0,0,0))
        paddle.move()
        ball.update()

        blocks.draw(screen)
        ball.draw(screen)
        paddle.draw(screen)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type==QUIT:
                exit()
            elif event.type==KEYDOWN:
                if event.key==K_RETURN:
                    ball.change()
                else:
                    exit()



def exit():
    pygame.quit()
    sys.exit()


if __name__=="__main__":
    main()