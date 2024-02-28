import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic

form_window = uic.loadUiType('D:\work\python\intel_AI\calculator.ui')[0]

class Exam(QWidget, form_window):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.calculator_init()

        btns = [self.btn_0, self.btn_1, self.btn_2, self.btn_3, self.btn_4,
                self.btn_5, self.btn_6, self.btn_7, self.btn_8, self.btn_9]
        btn_ops = [self.btn_add, self.btn_sub, self.btn_div, self.btn_mul, self.btn_eql]

        for idx, btn in enumerate(btns):
            btn.clicked.connect(self.btn_number_clicked_slot)

        for idx, btn in enumerate(btn_ops):
            btn.clicked.connect(self.btn_op_clicked_slot)
        self.btn_clr.clicked.connect(self.calculator_init)

    def calculator_init(self):
        self.first_input_flag = True
        self.opcode = ''
        self.number1 = 0
        self.lbl_result.setText('0')

    def btn_number_clicked_slot(self):
        btn = self.sender()
        value = self.lbl_result.text()
        if self.first_input_flag or value == '0':
            self.first_input_flag = False
            self.lbl_result.setText('')
        self.lbl_result.setText(self.lbl_result.text() + btn.objectName()[-1])

    def btn_op_clicked_slot(self):
        btn = self.sender()
        if self.first_input_flag == False:
            self.calculate()
            self.number1 = float(self.lbl_result.text())
        self.opcode = btn.objectName()[-3:]
        self.first_input_flag = True
        print(self.number1)
        print(self.opcode)

    def calculate(self):
        number2 = float(self.lbl_result.text())
        if self.opcode == 'add':
            self.lbl_result.setText(str(self.number1 + number2))
        elif self.opcode == 'sub':
            self.lbl_result.setText(str(self.number1 - number2))
        elif self.opcode == 'div':
            if number2:
                self.lbl_result.setText(str(self.number1 / number2))
            else :
                self.lbl_result.setText('infinity')
        elif self.opcode == 'mul':
            self.lbl_result.setText(str(self.number1 * number2))



if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = Exam()
    mainWindow.show()
    sys.exit(app.exec_())
