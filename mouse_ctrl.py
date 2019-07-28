import time
import autopy
import random


class Mouse_Ctrl:
    def __init__(self):
        pass

    def mouse_move(self, h, z):
        """z为纵坐标，h为横坐标"""
        h1, z1 = autopy.mouse.location()
        zong = z
        heng = h
        # 计算比例 使得轨迹成直线
        bili = abs((zong - z1)/(heng - h1))
        z2 = z1
        h2 = h1
        for i in range(50):
            jishu = abs((heng - h1)/50)
            if heng - h1 > 0:
                h2 += jishu
            else:
                h2 -= jishu
            if zong - z1 > 0:
                z2 += bili*jishu
            else:
                z2 -= bili*jishu
            autopy.mouse.move(h2, z2)
            time.sleep(0.0001)

    def mouse_click(self, sleep=0.1, L_or_R=1):
        """默认等待0.1s,默认点击左键,且不做按住操作"""
        time.sleep(sleep)
        if L_or_R == 1:
            autopy.mouse.click()
        else:
            autopy.mouse.click(autopy.mouse.Button.RIGHT)


if __name__ == '__main__':
    # m.click(39, 334, 1, 1)
    a = 320, 1600
    mouse_ctrl = Mouse_Ctrl()
    mouse_ctrl.mouse_move(a[0], a[1])
    mouse_ctrl.mouse_click()
    mouse_ctrl.mouse_move(200, 600)
    mouse_ctrl.mouse_click(5)

    # autopy.mouse.move(36, 614)
    # time.sleep(0.5)
    # autopy.mouse.click()
    # smooth是慢移动

    # autopy.mouse.click(autopy.mouse.Button.RIGHT)
    # autopy.mouse.toggle(autopy.mouse.Button.RIGHT, True)
    # autopy.mouse.toggle(autopy.mouse.Button.RIGHT, False)
    # autopy.mouse.click(RIGHT=True)
