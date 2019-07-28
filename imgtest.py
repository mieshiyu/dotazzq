import matplotlib.pyplot as plt
import cv2
import numpy as np
from io import BytesIO
from aip import AipOcr

img_path = r'0\rgb1.jpg'
img = cv2.imread(img_path)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# ret, gray2 = cv2.threshold(gray, 70, 180, cv2.THRESH_BINARY)
# ret, gray2 = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
# gray2 = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
# blurred = cv2.GaussianBlur(gray, (9, 9), 0)


edges = cv2.Canny(img, 180, 255)

#lower_blue = np.array([130, 100, 100])  # blue
#upper_blue = np.array([180, 255, 255])

#blue_mask = cv2.inRange(erosion, lower_blue, upper_blue)  # 蓝色

cv2.imshow('2', edges)




def get_word_by_img(img):
    """ 你的 APPID AK SK """
    APP_ID = '15861557'
    API_KEY = 'Kv13esNrPyNWnTnS1WQm0MUX'
    SECRET_KEY = 'wRPcYhXqHrAPi8Y4bh0aGe2A1CLZymw8'
    client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
    res = client.basicGeneral(img)
    return res


img_str = cv2.imencode('.jpg', edges)[1].tostring()
message = get_word_by_img(img_str)
for i in message.get('words_result'):
    print(i.get('words'))

cv2.waitKey(0)
