import pymouse,pykeyboard,os,sys
from pymouse import *
from pykeyboard import PyKeyboard
import datetime
import win32gui, win32ui, win32con, win32api
import cv2
import time
from io import BytesIO

#img_fb = BytesIO()
#img_fb.write()


def window_capture(filename):
        hwnd = 0 # 窗口的编号，0号表示当前活跃窗口
        # 根据窗口句柄获取窗口的设备上下文DC（Divice Context）
        hwndDC = win32gui.GetWindowDC(hwnd)
        # 根据窗口的DC获取mfcDC
        mfcDC = win32ui.CreateDCFromHandle(hwndDC)
        # mfcDC创建可兼容的DC
        saveDC = mfcDC.CreateCompatibleDC()
        # 创建bigmap准备保存图片
        saveBitMap = win32ui.CreateBitmap()
        # 获取监控器信息
        MoniterDev = win32api.EnumDisplayMonitors(None, None)
        w = MoniterDev[0][2][2]
        h = MoniterDev[0][2][3]
        # print(w, h)       # 图片大小
        # 为bitmap开辟空间
        saveBitMap.CreateCompatibleBitmap(mfcDC, 1600, 926)
        # 高度saveDC，将截图保存到saveBitmap中
        saveDC.SelectObject(saveBitMap)
        # 截取从左上角（0，0）长宽为（w，h）的图片 LOTA2 = 1600X900为以下坐标
        saveDC.BitBlt((0, 0), (1600, 990), mfcDC, (160, 65), win32con.SRCCOPY)
        saveBitMap.SaveBitmapFile(saveDC, filename)



m = PyMouse()
# m.move(39, 334)
m.click(39, 334, 1, 1)
# time.sleep(3)
m.click(1380, 507, 1, 1)
#time.sleep(1.5)
#k.tap_key(k.tab_key) # –点击tab键
# m.click(x,y,button,n)
# x,y –是坐标位置
# buttong –1表示左键，2表示点击右键

# n –点击次数，默认是1次，2表示双击
# for i in range(10):
for i in range(200):
    time.sleep(0.1)
    beg = time.time()
    time_now = datetime.datetime.now().strftime('%S.%f')
    if int(time_now[3]) >= 8:
        name = time_now[:2] + '_' + time_now[3:5] + '.jpg'
        window_capture(name)
        #img = cv2.imread(name)
        #cv2.imshow('img', img)
        #cv2.waitKey()

        print(time.time() - beg)
        print(time_now[:5], time.time())