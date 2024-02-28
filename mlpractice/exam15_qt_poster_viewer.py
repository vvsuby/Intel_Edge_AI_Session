import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic

form_window = uic.loadUiType('./poster.ui')[0]

class Exam(QWidget, form_window):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.btn_ml.clicked.connect(self.btn_click_slot)
        self.btn_nl.clicked.connect(self.btn_click_slot)
        self.btn_hs.clicked.connect(self.btn_click_slot)
        self.btn_seoul.clicked.connect(self.btn_click_slot)

    def btn_click_slot(self):
        btn = self.sender()
        self.lbl_ml.hide()
        self.lbl_hs.hide()
        self.lbl_nl.hide()
        self.lbl_seoul.hide()
        if btn.objectName() == 'btn_ml': self.lbl_ml.show()
        elif btn.objectName() == 'btn_hs': self.lbl_hs.show()
        elif btn.objectName() == 'btn_nl': self.lbl_nl.show()
        elif btn.objectName() == 'btn_seoul': self.lbl_seoul.show()

    def btn_nl_slot(self):
        self.lbl_ml.hide()
        self.lbl_hs.hide()
        self.lbl_nl.hide()
        self.lbl_seoul.hide()
        self.lbl_nl.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = Exam()
    mainWindow.show()
    sys.exit(app.exec_())
