from aip import AipOcr
import cv2
import time


class ShiBie:
    def __init__(self):
        pass

    def cv_to_jpg(self, cv2_read_img):
        img_str = cv2.imencode('.jpg', cv2_read_img)[1].tostring()
        return img_str

    def baiduaip_shibie(self, cv2_read_img):
        """先把cv转化成百度api识别的jpg格式"""
        img = self.cv_to_jpg(cv2_read_img)
        """ 你的 APPID AK SK """
        APP_ID = '15861557'
        API_KEY = 'Kv13esNrPyNWnTnS1WQm0MUX'
        SECRET_KEY = 'wRPcYhXqHrAPi8Y4bh0aGe2A1CLZymw8'
        client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
        res = client.basicGeneral(img)
        return res

    def output_word(self, img_str):
        str_list = []
        message = self.baiduaip_shibie(img_str)
        for i in message.get('words_result'):
            # print(i.get('words'))
            str_list.append(i.get('words'))
        # 返回 str_list
        return str_list


if __name__ == '__main__':
    beg = time.time()
    bdshibie = ShiBie()
    img = cv2.imread('xz.jpg', 1)
    qzxx = []
    for i in bdshibie.output_word(img):
        print(i)
        qzxx.append(i)
    if qzxx[0] == '圣堂刺客' + '★':
        print(qzxx[0], 'ta来了')
    print(time.time() - beg)

