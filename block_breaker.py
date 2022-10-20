import pygame

def main():
    pygame.init()
    pygame.display.set_caption('ブロック崩し')
    screen = pygame.display.set_mode((400,400))
    screen.fill(0,0,0)


if __name__=="__main__":
    main()