import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidgetItem, QFileDialog, QMenu, QAction, QDialog, QVBoxLayout, QTextEdit, QDialogButtonBox, QWidget
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt  # Qt 모듈 추가

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        # UI 파일 로드
        loadUi('./res/myWin01.ui', self)
        # 윈도우 제목 설정
        self.setWindowTitle('Main Window')

        self.btnPicture.clicked.connect(self.getImage)
        self.btnAdd.clicked.connect(self.add_contact)
        self.btnSave.clicked.connect(self.save_contacts)
        self.btnRead.clicked.connect(self.read_contacts)

        # 리스트 위젯 우클릭 메뉴 연결
        self.listWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.listWidget.customContextMenuRequested.connect(self.show_context_menu)

    def show_context_menu(self, pos):
        context_menu = QMenu()
        edit_action = QAction("수정", self)
        delete_action = QAction("삭제", self)
        context_menu.addAction(edit_action)
        context_menu.addAction(delete_action)
        edit_action.triggered.connect(self.edit_item)
        delete_action.triggered.connect(self.delete_item)
        context_menu.exec_(self.listWidget.mapToGlobal(pos))

    def add_contact(self):
        name = self.lineEditName.text()
        phone = self.lineEditPhone.text()
        photo_path = self.lblPicturePath.text()

        if name and phone:
            text = f'이름 : {name}, 전화번호 : {phone}, 이미지 경로 : {photo_path}'
            item = QListWidgetItem(text)

            if os.path.exists(photo_path):
                icon = QIcon(photo_path)
            else:
                icon = QIcon('./res/unknown.jpg')
            item.setIcon(icon)

            self.listWidget.addItem(item)
        else:
            print("이름과 전화번호를 입력하세요.")

    def edit_item(self):
        selected_item = self.listWidget.currentItem()
        if selected_item:
            dialog = EditDialog(selected_item.text(), self)
            if dialog.exec_():
                edited_text = dialog.get_text()
                selected_item.setText(edited_text)

    def delete_item(self):
        selected_items = self.listWidget.selectedItems()
        for item in selected_items:
            self.listWidget.takeItem(self.listWidget.row(item))

    def getImage(self): 
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filename, _ = QFileDialog.getOpenFileName(self,  '이미지 파일', '' , '이미지 파일 (*.png *.jpg *.jpeg *.bmp *.gif)', options=options)

        if filename:
            pixmap = QPixmap(filename)
            self.lblPicture.setPixmap(pixmap)
            self.lblPicture.setScaledContents(True)
            self.lblPicturePath.setText(filename)
        else:
            self.lblPicturePath.setText('None')

    def save_contacts(self):
        filename, _ = QFileDialog.getSaveFileName(self, '저장할 파일 선택', '', '텍스트 파일 (*.txt)')
        if filename:
            with open(filename, 'w') as file:
                for index in range(self.listWidget.count()):
                    item = self.listWidget.item(index)
                    file.write(item.text() + '\n')

    def read_contacts(self):
        filename, _ = QFileDialog.getOpenFileName(self, '불러올 파일 선택', '', '텍스트 파일 (*.txt)')
        if filename:
            with open(filename, 'r') as file:
                for line in file:
                    data = line.strip().split(', ')
                    name, phone, photo_path = data[0].split(' : ')[1], data[1].split(' : ')[1], data[2].split(' : ')[1]
                    item = QListWidgetItem(f'이름 : {name}, 전화번호 : {phone}, 이미지 경로 : {photo_path}')
                    if os.path.exists(photo_path):
                        icon = QIcon(photo_path)
                    else:
                        icon = QIcon('./res/unknown.jpg')
                    item.setIcon(icon)
                    self.listWidget.addItem(item)

class EditDialog(QDialog):
    def __init__(self, text, parent=None):
        super(EditDialog, self).__init__(parent)
        self.setWindowTitle('수정')
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.text_edit = QTextEdit()
        self.text_edit.setPlainText(text)
        layout.addWidget(self.text_edit)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        layout.addWidget(button_box)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

    def get_text(self):
        return self.text_edit.toPlainText()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
