import os
import random
import sys
import pygame as pg


WIDTH, HEIGHT = 1200, 700
DELTA = {  # 移動量辞書
    pg.K_UP : (0, -5),
    pg.K_DOWN : (0, +5),
    pg.K_LEFT : (-5, 0),
    pg.K_RIGHT : (+5, 0),
}
ROTATE = {  # 回転辞書
    ( 0, -5):270,
    (-5, -5):315,
    (-5,  0):0,
    (-5, +5):45,
    ( 0, +5):90,
    (+5, +5):135,
    (+5,  0):180,
    (+5, -5):225,
    ( 0,  0):0,
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(rct:pg.Rect) -> tuple[bool, bool]:
    """
    引数:こうかとんRectか爆弾Rect
    戻り値:タプル(横方向判定結果,縦方向判定結果)
    画面内ならTrue,画面外ならFalse
    """
    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right:
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:
        tate = False
    return yoko, tate



def push_rotate(): 
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 2.0)
    kk_img01 = pg.transform.flip(kk_img, True, False) 
    return {  # 回転辞書
        ( 0, -5):pg.transform.rotozoom(kk_img01, 90, 1.0),
        (-5, -5):pg.transform.rotozoom(kk_img, -45, 1.0),
        (-5,  0):kk_img,
        (-5, +5):pg.transform.rotozoom(kk_img, 45, 1.0),
        ( 0, +5):pg.transform.rotozoom(kk_img01, -90, 1.0),
        (+5, +5):pg.transform.rotozoom(kk_img01, -45, 1.0),
        (+5,  0):kk_img01,
        (+5, -5):pg.transform.rotozoom(kk_img01, 45, 1.0),
        ( 0,  0):kk_img,
}


def bb_big(): #拡大爆弾Surface
    a = []
    b = []
    for r in range(1, 11):
        bomb_img = pg.Surface((20*r, 20*r))
        pg.draw.circle(bomb_img, (255, 0, 0), (10*r, 10*r), 10*r)
        bomb_img.set_colorkey((0, 0, 0))
        a.append(r)
        b.append(bomb_img)
    return a,b
        

def gameover(screen:pg.display, kk_rct:pg.rect):  # GameOver画面
    """
    引数
    """
    font = pg.font.Font(None, 100)  #font
    text = font.render("Game Over", True, (255, 255, 255))  # テキストサイズ
    text_rct = text.get_rect(center=(WIDTH/2,HEIGHT/2))  # テキスト位置
    black = pg.Surface((WIDTH,HEIGHT))
    black.set_alpha(128)
    black.fill((0, 0, 0))
    cry_img = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 2.0)
    cry_rct = cry_img.get_rect(center=kk_rct.center)
    cry_img2 = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 2.0)
    cry_rct2 = cry_img.get_rect(center=(WIDTH-kk_rct[0],HEIGHT-kk_rct[1]))

    screen.blit(black,(0,0))
    screen.blit(cry_img,cry_rct)
    screen.blit(cry_img2,cry_rct2)
    screen.blit(text,text_rct)
    pg.display.update()
    pg.time.wait(5000)


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg") 
    kk_imgs = push_rotate() # 回転率,大きさ倍率
    kk_img = kk_imgs[(0,0)]   
    kk_rct = kk_img.get_rect()
    kk_rct.center = 900, 400
    bomb_img = pg.Surface((20, 20))  # 爆弾
    pg.draw.circle(bomb_img, (255, 0, 0), (10, 10), 10)
    bomb_accs, bomb_imgs = bb_big()
    bomb_img.set_colorkey((0, 0, 0))
    bomb_rct = bomb_img.get_rect()
    bomb_rct.center = random.randint(0, 1200), random.randint(0, 700)
    vx, vy = +5, +5  # 横、縦の速さ

    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        if kk_rct.colliderect(bomb_rct):  # 衝突判定
            return gameover(screen, kk_rct)
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for k, v in DELTA.items():  # k=キー,v=変化量
            if key_lst[k]:
                sum_mv[0] += v[0]
                sum_mv[1] += v[1]

        kk_img = kk_imgs[tuple(sum_mv)] #こうかとんの動きによって向きが変わる。

        kk_rct.move_ip(sum_mv)  # こうかとん画面内
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])

        screen.blit(kk_img, kk_rct)

        avx = vx*bomb_accs[min(tmr//500, 9)]
        avy = vy*bomb_accs[min(tmr//500, 9)]
        bomb_img = bomb_imgs[min(tmr//500, 9)]

        vx,vy = avx, avy

        bomb_rct.move_ip(vx, vy)  # 爆弾画面内
        yoko, tate = check_bound(bomb_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        
        screen.blit(bomb_img, bomb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)
        


if __name__ == "__main__":
    pg.init()
    main()
    print(bb_big())
    pg.quit()
    sys.exit()
