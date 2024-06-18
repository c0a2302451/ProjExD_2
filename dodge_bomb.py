import os
import random
import sys
import pygame as pg


WIDTH, HEIGHT = 1200, 700
DELTA = {  # 移動量辞書
    pg.K_UP : (0, -5),
    pg.K_DOWN : (0, +5),
    pg.K_LEFT : (-5, 0),
    pg.K_RIGHT : (+5, 0)
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


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 2.0) # 回転率,大きさ倍率
    kk_rct = kk_img.get_rect()
    kk_rct.center = 900, 400
    bomb_img = pg.Surface((20, 20))  # 爆弾
    bomb_img.set_colorkey((0, 0, 0))
    pg.draw.circle(bomb_img, (255, 0, 0), (10, 10), 10)
    bomb_rct = bomb_img.get_rect()
    bomb_rct.center = random.randint(0, 1200), random.randint(0, 700)
    vx, vy = +5, +5  # 横、縦の速さ

    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for k, v in DELTA.items():  # k=キー,v=変化量
            if key_lst[k]:
                sum_mv[0] += v[0]
                sum_mv[1] += v[1]
        kk_rct.move_ip(sum_mv)  # こうかとん
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)

        bomb_rct.move_ip(vx, vy)  # 爆弾
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
    pg.quit()
    sys.exit()
