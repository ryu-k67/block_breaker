import random
import pygame
from pygame.locals import *
import sys



# 表示ウィンドウのサイズ
SCREEN=Rect(0,0,400,600)


# ブロッククラス
class Block(pygame.sprite.Sprite):

    #初期化
    def __init__(self,file,x,y):
        pygame.sprite.Sprite.__init__(self)
        # 画像の読み込み
        self.image=pygame.image.load(file).convert_alpha()
        # 画像サイズを決める
        self.image=pygame.transform.scale(self.image,(SCREEN.width/6,SCREEN.height*0.4/8))
        # 画像の描写情報(Rect)を取得
        self.rect=self.image.get_rect()
        # 画像の位置決め
        self.rect.left=x*self.rect.width
        self.rect.top=y*self.rect.height

    # 画像の描写
    def draw(self, screen):
        screen.blit(self.image, self.rect)


# ボールクラス
class Ball(pygame.sprite.Sprite):

    #初期化
    def __init__(self,file,blocks,paddle):
        pygame.sprite.Sprite.__init__(self)
        # 画像の読み込み
        self.image=pygame.image.load(file).convert_alpha()
        # 画像サイズを決める
        self.image=pygame.transform.scale(self.image,(25,25))
        # 画像の描写情報(Rect)を取得
        self.rect=self.image.get_rect()
        self.blocks=blocks
        self.paddle=paddle
        # self.updateにstartを登録
        self.update=self.start

    # 画像の描写
    def draw(self, screen):
        screen.blit(self.image, self.rect)

    # ボールの初期状態（位置、変化量）
    def start(self):
        # 画像の位置決め
        self.rect.centerx=self.paddle.rect.centerx
        self.rect.bottom=self.paddle.rect.top
        # x軸変化量はランダム
        self.dx=random.uniform(-10,10)
        # y軸変化量
        self.dy=-10
        
    # updateに登録する関数をmoveに変更する
    def change(self):
        self.update=self.move

    # ボールの動き
    def move(self):
        # ボールの位置に変化量を加えて移動
        self.rect.centerx+=self.dx
        self.rect.centery+=self.dy
        
        # 左壁に反射
        if self.rect.left<SCREEN.left:
            # 位置を壁面に接触した位置に設定
            self.rect.left=SCREEN.left
            # x軸変化量を逆向きに
            self.dx=-self.dx
        # 上壁に反射
        if self.rect.top<SCREEN.top:
            self.rect.top=SCREEN.top
            # y軸変化量を逆向きに
            self.dy=-self.dy
        # 右壁に反射
        if self.rect.right>SCREEN.right:
            self.rect.right=SCREEN.right
            # x軸変化量を逆向きに
            self.dx=-self.dx
        
        # パドルに反射
        if self.rect.colliderect(self.paddle.rect):
            # y軸変化量を逆向きに
            self.dy=-self.dy
            # x軸変化量を、パドルとの接触位置によって変化させる
            self.dx=self.dx+(self.rect.centerx-self.paddle.rect.centerx)/10
            # 変化量の上限を 15 とする
            if self.dx>15:
                self.dx=15
            elif self.dx<-15:
                self.dx=-15
            # 位置をパドルを接触する1px手前に
            self.rect.bottom=self.paddle.rect.top-1
        
        # 下に落ちた場合
        if self.rect.bottom>SCREEN.bottom:
            # updateに登録する関数をstartに変更（やり直し）
            self.update=self.start

        # ボールとぶつかったブロックを消去し、そのブロックをリストで取得
        vanish_blocks=pygame.sprite.spritecollide(self,self.blocks,True)

        # ぶつかったブロックがあれば
        if vanish_blocks:
            # ブロックリストを全探索
            for block in vanish_blocks:
                # 下からブロックに接触
                if self.rect.top<block.rect.bottom and self.rect.bottom>block.rect.bottom:
                    self.rect.top=block.rect.bottom
                    self.dy=-self.dy
                # 上からブロックに接触
                if self.rect.top>block.rect.top and self.rect.bottom<block.rect.top:
                    self.rect.bottom=block.rect.top
                    self.dy=-self.dy
                # 左からブロックに接触
                if self.rect.left>block.rect.left and self.rect.right<block.rect.left:
                    self.rect.right=block.rect.left
                    self.dx=-self.dx
                # 右からブロックに接触
                if self.rect.right<block.rect.right and self.rect.left>block.rect.right:
                    self.rect.left=block.rect.right
                    self.dx=-self.dx

        # 画面からボールがはみ出さないようにする
        self.rect.clamp_ip(SCREEN)


# パドルクラス
class Paddle(pygame.sprite.Sprite):

    # 初期化
    def __init__(self,file):
        pygame.sprite.Sprite.__init__(self)
        # 画像の読み込み
        self.image=pygame.image.load(file).convert_alpha()
        # 画像サイズの設定
        self.image=pygame.transform.scale(self.image,(100,20))
        # 画像の描写情報を取得
        self.rect=self.image.get_rect()
        # 位置決め
        self.rect.bottom=SCREEN.bottom
        self.rect.centerx=int(SCREEN.width/2)

    # 描写
    def draw(self, screen):
        screen.blit(self.image, self.rect)

    # パドルの動き
    def move(self):
        # マウスカーソルの位置にしたがってパドル位置も変動
        self.rect.centerx=pygame.mouse.get_pos()[0]
        # パドルが画面からはみ出さないようにする
        self.rect.clamp_ip(SCREEN)




def main():
    pygame.init()
    pygame.display.set_caption('ブロック崩し')
    screen = pygame.display.set_mode(SCREEN.size)
    # 黒画面
    screen.fill((0,0,0))

    clock = pygame.time.Clock()

    # グループの作成
    blocks=pygame.sprite.Group()
    for block_x in range(6):
        for block_y in range(8):
            # ブロックの生成
            block=Block('block.png',block_x,block_y)
            # ブロックをグループに追加
            blocks.add(block)
    # パドルの生成
    paddle=Paddle('paddle.png')
    # ボールの生成
    ball=Ball('ball.png',blocks,paddle)

    # exit()が呼ばれるまで終わらない
    while True:

        clock.tick(60)
        screen.fill((0,0,0))

        # 位置を変化
        paddle.move()
        ball.update()

        # 画面に描写
        blocks.draw(screen)
        ball.draw(screen)
        paddle.draw(screen)
        pygame.display.update()

        for event in pygame.event.get():
            # 閉じるボタン
            if event.type==QUIT:
                exit()
            # キーボードのなんらかのキーが押された場合
            elif event.type==KEYDOWN:
                # エンターキーが押された場合
                if event.key==K_RETURN:
                    ball.change()
                # エンターキー以外が押された場合
                else:
                    exit()


# 終了
def exit():
    pygame.quit()
    sys.exit()


if __name__=="__main__":
    main()