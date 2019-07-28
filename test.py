import pytesseract
import time
import cv2
"""自己开发的模块"""
from mouse_ctrl import Mouse_Ctrl
from jietu import JieTu
from shibie import ShiBie
from hero_dict import Hero_Dict


"""
mouse_ctrl = Mouse_Ctrl()
mouse_ctrl.mouse_move(1028, 859)
mouse_ctrl.mouse_click()
mouse_ctrl.mouse_move(200, 600)
mouse_ctrl.mouse_click(0.5)


beg = time.time()
jietu = JieTu()
img = jietu.grab_screen()
hhzt = jietu.get_hhzt(img)
cv2.imshow('img', hhzt)
print(time.time() - beg)
cv2.waitKey()
"""
"""
time.sleep(2)
mouse_ctrl = Mouse_Ctrl()
'''加载截图模块'''
jietu = JieTu()
beg = time.time()
img = jietu.grab_screen()
player = jietu.get_player(img)
cv2.imshow('img', player)
#cv2.imshow('img', player)
#qxzz = jietu.get_qzxx(img)
#cv2.imshow('img', qxzz)
'''加载百度识别模块'''
bdshibie = ShiBie()
'''加载英雄字典模块'''
hero = Hero_Dict()
hero_dict = hero.hero()
message = bdshibie.baiduaip_shibie(player)
#qzxx_list = []
no_player = 0
player_wz_dict = {
                    1: 214, 2: 306, 3: 389, 4: 476,
                    5: 556, 6: 653, 7: 750, 8: 826
                  }
for i in message.get('words_result'):
    no_player += 1
    print(i.get('words'))
    if i.get('words') == '★带哥':
        print('123', no_player)
        mouse_ctrl.mouse_move(1616, player_wz_dict[no_player])
        mouse_ctrl.mouse_click()

    '''
    qzxx_list.append(i.get('words'))
    for i in hero_dict:
        hero_xx = i + '★'
        if hero_xx in qzxx_list:
            print(hero_dict[i])
    '''

print(time.time() - beg)
cv2.waitKey()
"""
"""
a = True
while True:
    if a:
        print('123')

        break

    print('456')

"""

a = {'au': 1, 'ab': 2}

for i in a:
    print(i+'kk')

b = 'yungng'

if b[-1] == 'g':
    print(b[:-1])

for i in range(10):
    print(i+1)

lll = [1, 2, 3, 4, 5]

print(lll[:2])