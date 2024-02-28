import sys
from PIL import Image
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import *
from PyQt5 import uic
import numpy as np
from tensorflow.keras.models import load_model
import cv2
import time

form_window = uic.loadUiType('./cat_and_dog.ui')[0]

class Exam(QWidget, form_window):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.model = load_model('.\cat_and_dog_0.834.h5')

        self.btn_open.clicked.connect(self.btn_clicked_slot)

    def btn_clicked_slot(self):
        capture = cv2.VideoCapture(0)
        capture.set(cv2.CAP_PROP_FRAME_WIDTH, 64)
        capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 64)
        flag = True
        while flag:
            v, frame = capture.read()
            print(type(frame))

            if (v):
                cv2.imshow('VideoFrame', frame)
                cv2.imwrite('./capture.png', frame)
            # time.sleep(0.01)
            key = cv2.waitKey(50)
            if key == 27:
                flag = False

            pixmap = QPixmap('./capture.png')
            self.lbl_image.setPixmap(pixmap)

            try:
                img = Image.open('./capture.png')
                img = img.convert('RGB')
                img = img.resize((64, 64))
                data = np.asarray(img)
                data = data / 255
                data = data.reshape(1, 64, 64, 3)

                pred = self.model.predict(data)
                print(pred)
                if pred < 0.5:
                    self.lbl_result.setText('고양이입니다.')
                else:
                    self.lbl_result.setText('강아지입니다.')
            except:
                print('error ')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = Exam()
    mainWindow.show()
    sys.exit(app.exec_())
