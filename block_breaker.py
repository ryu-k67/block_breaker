import pygame
from pygame.locals import *
import sys



SCREEN=Rect(0,0,400,600)

class Block(pygame.sprite.Sprite):
    def __init__(self,file,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load(file).convert_alpha()
        self.image=pygame.transform.scale(self.image,(SCREEN.width/8,SCREEN.height*0.4/4))
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
        self.dx=0
        self.dy=-10

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def start(self):
        self.rect.centerx=self.paddle.rect.centerx
        self.rect.bottom=self.paddle.rect.top

        
    def change(self):
        self.update=self.move

    def move(self):
        self.rect.centerx+=self.dx
        self.rect.centery+=self.dy

        if self.rect.left<SCREEN.left:
            self.rect.left=SCREEN.left
            self.dx=-self.dx
            self.dy=-self.dy
        if self.rect.top<SCREEN.top:
            self.rect.top=SCREEN.top
            self.dx=-self.dx
            self.dy=-self.dy
        if self.rect.right>SCREEN.right:
            self.rect.right=SCREEN.right
            self.dx=-self.dx
            self.dy=-self.dy
        if self.rect.bottom>SCREEN.bottom:
            self.update=self.start

        

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
    for ball_x in range(8):
        for ball_y in range(4):
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