import time
import cv2
import datetime
import copy
"""自己开发的模块"""
from mouse_ctrl import Mouse_Ctrl
from jietu import JieTu
from shibie import ShiBie
from hero_dict import Hero_Dict


class zzq_demo:
    def __init__(self):
        self.ctrl_start = False
        self.ctrl_stop = False

        '''加载截图模块'''
        self.jietu = JieTu()  # grab_screen()获得截图,get_qzxx棋子信息，get_gold金币信息,get_hhzt回合状态,get_hhtime时间
                                # get_player获得玩家排位好定位
        '''加载鼠标控制模块'''
        self.mouse_ctrl = Mouse_Ctrl()  # mouse_move(h,z)移动到hz,mouse_click(n,m)n为移动后等待时间,m默认左键,填2为右键
        '''加载百度识别模块'''
        self.bdshibie = ShiBie()    # output_word()返回识别的列表
        '''加载英雄字典模块'''
        self.hero = Hero_Dict()  # hero是全英雄信息,race是种族羁绊,career是职业羁绊
        '''玩家位置字典'''
        self.player_wz_dict = {
            1: 214, 2: 306, 3: 389, 4: 476, 5: 556, 6: 653, 7: 750, 8: 826, 'heng': 1616
        }
        '''棋盘等待区位置字典'''
        self.want_qpan_dict = {
            'zong': 760, 1: 640, 2: 738, 3: 828, 4: 909, 5: 1000, 6: 1085, 7: 1194, 8: 1268
        }
        '''等候区内容字典'''
        self.want_wz_dict = {
            1: None, 2: None, 3: None, 4: None, 5: None, 6: None, 7: None, 8: None
        }
        '''已拥有棋子字典'''
        self.qz_have_dict = {}
        '''棋子位置字典'''
        self.qz_dict = {
            'zong': 300, 1: 541, 2: 750, 3: 970, 4: 1170, 5: 1390
        }
        # ————————————————————————————————————————
        '''棋盘倒数第二排位置字典'''
        self.two_qpan_dict = {
            'zong': 545, 1: 711, 2: 768, 3: 862, 4: 924, 5: 998, 6: 1078, 7: 1150, 8: 1220
        }
        '''棋盘倒数第一排位置字典'''
        self.one_qpan_dict = {
            'zong': 620, 1: 702, 2: 770, 3: 852, 4: 933, 5: 1004, 6: 1083, 7: 1160, 8: 1240
        }
        '''棋盘倒数第一排战场站位字典'''
        self.one_war_dict = {
            1: None, 2: None, 3: None, 4: None, 5: None, 6: None, 7: None, 8: None
        }

        """按键坐标"""
        self.Q_move = 880, 900   # Q是移动棋子，W是放回棋子，E是售出棋子，D是换棋子菜单，F是提升等级/人口
        self.W_move = 925, 900   # 由于是鼠标操作，所以D选的就近的   X是关闭棋子菜单
        self.E_move = 970, 900
        self.D_move = 423, 380
        self.F_move = 1067, 900
        self.X_move = 1500, 377

        self.zzq_gold = 1
        self.qz_order = []

    def run(self):
        while True:
            time.sleep(1.5)
            """判断游戏状态"""
            img = self.jietu.grab_screen()
            hhzt = self.jietu.get_hhzt(img)
            hhtime = self.jietu.get_hhtime(img)
            qzxx = self.jietu.get_qzxx(img)
            gold = self.jietu.get_gold(img)
            player = self.jietu.get_player(img)
            level = self.jietu.get_level(img)

            """若符合可操作状态,回合状态为准备,回合时间不为0"""
            try:
                if self.bdshibie.output_word(hhtime) == []:
                    """因时间识别有时候会出错，所以只能反向识别"""
                    pass
                else:
                    if self.bdshibie.output_word(hhtime)[0][0] != '0':
                        if self.bdshibie.output_word(hhzt)[0] == '准备':
                            """1.定位英雄位置，确保在自己棋盘操作"""
                            no_player = 0
                            for i in self.bdshibie.output_word(player):
                                no_player += 1
                                """ID前两位"""
                                if i == '★带哥':
                                    # print('123', no_player)
                                    self.mouse_ctrl.mouse_move(1616, self.player_wz_dict[no_player])
                                    self.mouse_ctrl.mouse_click()

                            """观察棋子，确定阵容"""
                            qzxx_dict = {}   # 棋子空字典，方便计算棋子位置
                            qzxx_list = []   # 棋子空列表
                            hero_dict = self.hero.hero()
                            m = 0
                            for i in self.bdshibie.output_word(qzxx):
                                print(i)
                                m += 1
                                """去掉★，创建棋子字典内容列表"""
                                if i[-1] == '★':
                                    i = i[:-1]
                                if i in qzxx_dict:
                                    pass
                                else:
                                    qzxx_dict[i] = []
                                """插入位置"""
                                qzxx_dict[i].append(m)
                                qzxx_list.append(i)

                            if qzxx_dict != {}:
                                '棋子信息列表为空，返回重新识别'
                                pass
                            else:
                                time.sleep(2)
                                continue
                            print('qzxx_dict', qzxx_dict, 'qzxx_list', qzxx_list)

                            """金币，等级获取"""
                            try:
                                self.zzq_gold = int(self.bdshibie.output_word(gold)[0])
                            except:
                                self.zzq_gold = 1
                            try:
                                zzq_level_have = int(self.bdshibie.output_word(level)[0][2])
                            except:
                                zzq_level_have = 1
                            zzq_level_kong = int(self.bdshibie.output_word(level)[0][2]) - int(self.bdshibie.output_word(level)[0][0])
                            print('self.zzq_gold, zzq_level_kong, zzq_level_have', self.zzq_gold, zzq_level_kong, zzq_level_have)
                            self.qz_order = []  # 架子位置下单列表
                            """前3回合通用打野组合"""
                            for hero_xx in qzxx_dict:
                                """判断是否是地精"""
                                if hero_dict[hero_xx][0] == '地精':
                                    """判断有几个,计算所需金币"""
                                    self.shaixuan_qz(hero_xx, qzxx_dict, hero_dict)
                            for hero_xx in qzxx_dict:
                                """判断是否是战士"""
                                if hero_dict[hero_xx][1] == '战士':
                                    self.shaixuan_qz(hero_xx, qzxx_dict, hero_dict)
                            for hero_xx in qzxx_dict:
                                """都不是就选金币对应的"""
                                if hero_dict[hero_xx][0] != '地精' and hero_dict[hero_xx][1] != '战士':
                                    self.shaixuan_qz(hero_xx, qzxx_dict, hero_dict)

                            print('self.qz_order', self.qz_order)

                            """购买棋子，记录，移动"""
                            buy_zongshu = len(self.qz_order)
                            """获得空位置列表"""
                            want_wz_list = []
                            for wz in self.want_wz_dict:  # 只重复第一个要插入的棋子
                                if self.want_wz_dict[wz] is None:
                                    want_wz_list.append(wz)
                            """截取所需区域"""
                            want_wz_list = want_wz_list[:buy_zongshu]
                            print('want_wz_list', want_wz_list)
                            for i in self.qz_order:
                                self.mouse_ctrl.mouse_move(self.qz_dict[i], self.qz_dict['zong'])
                                self.mouse_ctrl.mouse_click(0.5)
                                """记录此棋子,拥有就加1,没有就创建"""
                                try:
                                    if self.qz_have_dict[qzxx_list[i-1]] >= 1:
                                        self.qz_have_dict[qzxx_list[i-1]] = self.qz_have_dict[qzxx_list[i]] + 1
                                except:
                                    self.qz_have_dict[qzxx_list[i-1]] = 1
                                """棋子会到的等候区的位置"""
                                for wz in want_wz_list:
                                    self.want_wz_dict[wz] = qzxx_list[i-1]
                                del want_wz_list[0]
                                print('qzxx_list在qz_order中', qzxx_list)


                            """关闭商店,移动棋子后不需要，自动会关闭"""
                            #if  # 购买完了才关闭
                            #self.mouse_ctrl.mouse_move(self.X_move[0], self.X_move[1])
                            #self.mouse_ctrl.mouse_click(0.5)

                            print('wz', self.want_wz_dict, 'have', self.qz_have_dict)

                            """把棋子放置于战场上"""
                            """检查战场站位"""
                            for i in self.one_war_dict:
                                for k in self.want_wz_dict:
                                    if self.one_war_dict[i] is None and self.want_wz_dict[k] is not None \
                                            and zzq_level_kong > 0:
                                        self.mouse_ctrl.mouse_move(self.Q_move[0], self.Q_move[1])
                                        self.mouse_ctrl.mouse_click(0.5)
                                        self.mouse_ctrl.mouse_move(self.want_qpan_dict[k], self.want_qpan_dict['zong'])
                                        self.mouse_ctrl.mouse_click(0.5)
                                        self.mouse_ctrl.mouse_move(self.one_qpan_dict[i], self.one_qpan_dict['zong'])
                                        self.mouse_ctrl.mouse_click(0.5)
                                        self.one_war_dict[i] = self.want_wz_dict[k]
                                        self.want_wz_dict[k] = None
                                        zzq_level_kong -= 1

                            """清空"""

            except EnvironmentError as e:
                print(e)

    def shaixuan_qz(self, hero_xx, qzxx_dict, hero_dict):
        if self.zzq_gold / hero_dict[hero_xx][-1] >= 1:
            """如果1个棋子都买不起 就pass了"""
            if self.zzq_gold / hero_dict[hero_xx][-1] >= len(qzxx_dict[hero_xx]) >= 2:
                """全部都买的起就把位置插入下单列表"""
                self.zzq_gold = self.zzq_gold - (hero_dict[hero_xx][-1] * len(qzxx_dict[hero_xx]))
                for i in qzxx_dict[hero_xx]:
                    self.qz_order.append(i)
            else:
                """只能买一颗"""
                print('只买一颗')
                self.zzq_gold = self.zzq_gold - hero_dict[hero_xx][-1]
                self.qz_order.append(qzxx_dict[hero_xx][0])


if __name__ == '__main__':
    play = zzq_demo()
    play.run()

