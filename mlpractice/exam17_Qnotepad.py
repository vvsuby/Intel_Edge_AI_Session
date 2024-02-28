import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic

form_window = uic.loadUiType('./Qnotepad.ui')[0]

class Exam(QMainWindow, form_window):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.path = ('제목 없음', '')
        self.edited_flag = False
        self.setWindowTitle(self.path[0] + ' - QT Note Pad')
        self.plain_te.textChanged.connect(self.text_changed_slot)

        # file menu 구현
        self.actionSave_as.triggered.connect(self.action_save_as_slot)
        self.actionSave.triggered.connect(self.action_save_slot)
        self.actionExit.triggered.connect(self.action_exit_slot)
        self.actionOpen.triggered.connect(self.action_open_slot)
        self.actionNew.triggered.connect(self.action_new_slot)

        # edit menu 구현
        self.actionUn_do.triggered.connect(self.plain_te.undo)
        self.actionCut.triggered.connect(self.plain_te.cut)
        self.actionCopy.triggered.connect(self.plain_te.copy)
        self.actionPaste.triggered.connect(self.plain_te.paste)
        self.actionDelete.triggered.connect(self.plain_te.cut)
        self.actionSelect_all.triggered.connect(self.plain_te.selectAll)

        self.actionFont_2.triggered.connect(self.action_font_slot)

        self.actionAbout.triggered.connect(self.action_about_slot)

    def action_about_slot(self):
        QMessageBox.about(self, 'Qt Note Pad',
                          '''만든이 : ABC lab\n\r버전 정보 : 1.0.0''')

    def action_font_slot(self):
        font = QFontDialog.getFont()
        print(font)
        if font[1]:
            self.plain_te.setFont(font[0])

    def save_edited(self):
        if self.edited_flag:
            ans = QMessageBox.question(self, '저장하기', '저장할까요?',
                                       QMessageBox.No | QMessageBox.Cancel | QMessageBox.Yes,
                                       QMessageBox.Yes)
            if ans == QMessageBox.Yes:
                if self.action_save_slot():
                    return
            elif ans == QMessageBox.No: self.edited_flag = False
            elif ans == QMessageBox.Cancel:
                return 1

    def action_new_slot(self):
        if self.save_edited():
            return
        if self.edited_flag:
            return
        self.plain_te.setPlainText('')
        self.edited_flag = False
        self.plain_te.textChanged.connect(self.text_changed_slot)
        self.path = ('제목 없음', '')
        self.setWindowTitle(self.path[0].split('/')[-1] + ' - QT Note Pad')

    def action_open_slot(self):
        if self.save_edited():
            return
        if self.edited_flag:
            return
        old_path = self.path
        self.path = QFileDialog.getOpenFileName(self, 'Open File', '',
                    'Text Files(*.txt);;Python Files(*.py);;All Files(*.*)')
        if self.path[0]:
            with open(self.path[0], 'r') as f:
                str_read = f.read()
            self.plain_te.setPlainText(str_read)
            self.edited_flag = False
            self.plain_te.textChanged.connect(self.text_changed_slot)
            self.setWindowTitle(self.path[0].split('/')[-1] + ' - QT Note Pad')
        else :
            self.path = old_path

    def text_changed_slot(self):
        self.edited_flag = True
        self.setWindowTitle('*' + self.path[0].split('/')[-1] + ' - QT Note Pad')
        self.plain_te.textChanged.disconnect(self.text_changed_slot)

    def action_exit_slot(self):
        if self.save_edited():
            return
        if self.edited_flag:
            return
        self.close()

    def action_save_slot(self):
        if self.path[0] != '제목 없음':
            with open(self.path[0], 'w') as f:
                f.write(self.plain_te.toPlainText())
                self.edited_flag = False
                self.plain_te.textChanged.connect(self.text_changed_slot)
                self.setWindowTitle(self.path[0].split('/')[-1] + ' - QT Note Pad')
        else :  return self.action_save_as_slot()


    def action_save_as_slot(self):
        old_path = self.path
        self.path = QFileDialog.getSaveFileName(self,
                    'Save file', '', 'Text Files(*.txt);;Python Files(*.py);;All Files(*.*)')
        print(self.path)
        if self.path[0]:
            with open(self.path[0], 'w') as f:
                f.write(self.plain_te.toPlainText())
                self.edited_flag = False
                self.plain_te.textChanged.connect(self.text_changed_slot)
                self.setWindowTitle(self.path[0].split('/')[-1] + ' - QT Note Pad')
            return 0
        else :
            self.path = old_path
            return 1

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = Exam()
    mainWindow.show()
    sys.exit(app.exec_())
