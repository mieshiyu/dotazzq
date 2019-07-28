import numpy as np
import datetime
import win32gui, win32ui, win32con, win32api
import cv2
import time
from aip import AipOcr
import matplotlib.pyplot as plt
"""自己的模块"""
from shibie import ShiBie


class JieTu:
    def __init__(self):
        self.left = 160
        self.top = 65

    def grab_screen(self, region=None):
        hwin = win32gui.GetDesktopWindow()
        '''
        if region:
            left, top, x2, y2 = region
            width = x2 - left + 1
            height = y2 - top + 1
        else:
            width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
            height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
            left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
            top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)
        '''
        """已根据电脑屏幕1920*1080分辨率，和游戏设置1600*900分辨率设定region"""
        cv_width = 1600
        cv_height = 990
        cv_left = self.left
        cv_top = self.top

        hwindc = win32gui.GetWindowDC(hwin)
        srcdc = win32ui.CreateDCFromHandle(hwindc)
        memdc = srcdc.CreateCompatibleDC()
        bmp = win32ui.CreateBitmap()
        bmp.CreateCompatibleBitmap(srcdc, cv_width, cv_height)
        memdc.SelectObject(bmp)
        memdc.BitBlt((0, 0), (cv_width, cv_height), srcdc, (cv_left, cv_top), win32con.SRCCOPY)
        # memdc.BitBlt((0, 0), (1600, 990), srcdc, (160, 65), win32con.SRCCOPY)
        signedIntsArray = bmp.GetBitmapBits(True)
        img = np.fromstring(signedIntsArray, dtype='uint8')
        img.shape = (cv_height, cv_width, 4)
        srcdc.DeleteDC()
        memdc.DeleteDC()
        win32gui.ReleaseDC(hwin, hwindc)
        win32gui.DeleteObject(bmp.GetHandle())

        return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)    # RGB为彩图，GRAY是灰度图

    def get_hhzt(self, img):
        """回合状态，=准备或者！=准备"""
        hhzt = img[115 - self.top:150 - self.top, 900 - self.left:960 - self.left]
        # print('hhzt', time.time() - beg)
        return hhzt

    def get_hhtime(self, img):
        """确定在准备状态下，获得回合时间"""
        hhtime = img[150 - self.top:190 - self.top, 930 - self.left:990 - self.left]
        # print('hhtime', time.time() - beg)
        return hhtime

    def get_qzxx(self, img):
        """商店棋子信息"""
        # qzxx = img[370 - self.top:430 - self.top, 400 - self.left:1600 - self.left]  # 实际用
        # print('qzxx', time.time() - beg)
        qzxx1 = img[370 - self.top:430 - self.top, 470 - self.left:610 - self.left]
        qzxx2 = img[370 - self.top:430 - self.top, 685 - self.left:820 - self.left]
        qzxx3 = img[370 - self.top:430 - self.top, 890 - self.left:1030 - self.left]
        qzxx4 = img[370 - self.top:430 - self.top, 1100 - self.left:1235 - self.left]
        qzxx5 = img[370 - self.top:430 - self.top, 1300 - self.left:1445 - self.left]

        qzxx = np.ones((400, 200, 3), dtype=np.uint8)
        qzxx[5: 65, 5:145] = qzxx1
        qzxx[85:145, 5:140] = qzxx2
        qzxx[165: 225, 5:145] = qzxx3
        qzxx[245: 305, 5:140] = qzxx4
        qzxx[325: 385, 5:150] = qzxx5

        return qzxx

    def get_gold(self, img):
        """金币信息"""
        gold = img[115 - self.top:145 - self.top, 1260 - self.left:1300 - self.left]
        # print('gold', time.time() - beg)
        return gold

    def get_player(self, img):
        """玩家位置信息，确定在自己棋盘操作"""
        player1 = img[183 - self.top:211 - self.top, 1639 - self.left:1675 - self.left]
        player2 = img[274 - self.top:300 - self.top, 1639 - self.left:1675 - self.left]
        player3 = img[359 - self.top:384 - self.top, 1639 - self.left:1675 - self.left]
        player4 = img[446 - self.top:472 - self.top, 1639 - self.left:1675 - self.left]
        player5 = img[533 - self.top:562 - self.top, 1639 - self.left:1675 - self.left]
        player6 = img[623 - self.top:650 - self.top, 1639 - self.left:1675 - self.left]
        player7 = img[711 - self.top:740 - self.top, 1639 - self.left:1675 - self.left]
        player8 = img[799 - self.top:825 - self.top, 1639 - self.left:1675 - self.left]

        xx = cv2.imread('x.jpg', 1)
        player = np.ones((300, 60, 3), dtype=np.uint8)
        player[1:29, 22:58] = player1
        player[5:25, 1:21] = xx
        player[35:61, 22:58] = player2
        player[38:58, 1:21] = xx
        player[70:95, 22:58] = player3
        player[73:93, 1:21] = xx
        player[100:126, 22:58] = player4
        player[103:123, 1:21] = xx
        player[136:165, 22:58] = player5
        player[140:160, 1:21] = xx
        player[170:197, 22:58] = player6
        player[173:193, 1:21] = xx
        player[205:234, 22:58] = player7
        player[209:229, 1:21] = xx
        player[240:266, 22:58] = player8
        player[243:263, 1:21] = xx

        # print('player', time.time() - beg)
        return player

    def get_level(self, img):
        level = img[115 - self.top:145 - self.top, 1105 - self.left:1150 - self.left]
        # print('level', time.time() - beg)
        return level

    def get_round(self, img):
        q_round = img[96 - self.top:113 - self.top, 770 - self.left:835 - self.left]
        # print('round', time.time() - beg)
        return q_round


if __name__ == '__main__':

    def get_word_by_img(img):
        """ 你的 APPID AK SK """
        APP_ID = '15861557'
        API_KEY = 'Kv13esNrPyNWnTnS1WQm0MUX'
        SECRET_KEY = 'wRPcYhXqHrAPi8Y4bh0aGe2A1CLZymw8'
        client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
        res = client.basicGeneral(img)
        return res

    time.sleep(1)
    beg = time.time()
    shibie = ShiBie()
    jietu = JieTu()
    img = jietu.grab_screen()
    hhzt = jietu.get_hhzt(img)
    hhtime = jietu.get_hhtime(img)
    qzxx = jietu.get_qzxx(img)
    gold = jietu.get_gold(img)
    player = jietu.get_player(img)
    level = jietu.get_level(img)
    # q_round = jietu.get_round(img)

    # cv2.waitKey()

    # titles = ['img', 'hhzt', 'hhtime', 'qzxx', 'gold', 'player', 'level', 'round']
    # images = [img, hhzt, hhtime, qzxx, gold, player, level, q_round]    round 识别不完整 暂时不要
    images = [img, hhzt, hhtime, qzxx, gold, player, level]

    for i in range(7):
        """
        '显示全部截图'
        plt.subplot(2, 4, i + 1), plt.imshow(images[i], 'gray')
        plt.title(titles[i])
        plt.xticks([]), plt.yticks([])
        """
        if i == 0:
            pass
        else:
            print(i, time.time() - beg)
            shibie.output_word(images[i])

    # plt.show()

    print(time.time() - beg)
