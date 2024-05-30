import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QListWidget, QFileDialog, QDialog,QMenu
from PyQt5.QtCore import Qt

from PyQt5.QtGui import QIcon, QPixmap


# 우클릭 삭제 
class EditDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('연락처 수정')
        self.name_label = QLabel('새 이름:')
        self.name_input = QLineEdit()
        self.phone_label = QLabel('새 전화번호:')
        self.phone_input = QLineEdit()
        
        # QLabel을 사용하여 이미지를 표시할 준비
        self.image_label = QLabel()
        self.image_label.setFixedSize(100, 100)  # 이미지 크기 지정
        
        self.load_image_button = QPushButton('이미지 불러오기')
        self.load_image_button.clicked.connect(self.load_image)
        
        self.ok_button = QPushButton('확인')
        self.ok_button.clicked.connect(self.accept)
        
        self.cancel_button = QPushButton('취소')
        self.cancel_button.clicked.connect(self.reject)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(self.cancel_button)

        layout = QVBoxLayout()
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_input)
        layout.addWidget(self.phone_label)
        layout.addWidget(self.phone_input)
        layout.addWidget(self.image_label)  # 이미지 표시 QLabel 추가
        layout.addWidget(self.load_image_button)
        layout.addLayout(button_layout)
        self.setLayout(layout)

    def load_image(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "이미지 불러오기", "", "이미지 파일 (*.png *.jpg *.jpeg *.bmp *.gif)", options=options)
        if file_name:
            # 이미지 파일이 선택되었을 때의 처리
            pixmap = QPixmap(file_name)
            pixmap = pixmap.scaledToWidth(100)  # 이미지 크기 조정
            self.image_label.setPixmap(pixmap)

class AddressBook(QWidget):
    def __init__(self):
        super().__init__()
        self.contacts = {}  # 주소록을 딕셔너리로 관리합니다.
        self.init_ui()
        self.load_from_file()

    def init_ui(self):
        self.setWindowTitle('주소록 프로그램')

        # 수정 버튼에 아이콘 추가
        self.edit_button = QPushButton()
        self.edit_button.setIcon(QIcon('D:/Jiwon/myPj01/res/edit.png'))  # 아이콘 경로 지정

        # 삭제 버튼에 아이콘 추가
        self.delete_button = QPushButton()
        self.delete_button.setIcon(QIcon('D:/Jiwon/myPj01/res/delete.png'))  # 아이콘 경로 지정

        self.name_label = QLabel('이름:')
        self.name_input = QLineEdit()
        self.phone_label = QLabel('전화번호:')
        self.phone_input = QLineEdit()

        self.add_button = QPushButton('추가')
        self.add_button.clicked.connect(self.add_contact)

        self.search_label = QLabel('찾기:')
        self.search_input = QLineEdit()
        # 검색버튼을 만들고 눌렀을때 검색
        # self.search_button = QPushButton('검색')
        # self.search_button.clicked.connect(self.search_contact)

        # self.search_input = QLineEdit() 앤터치면 검색
        self.search_input.returnPressed.connect(self.search_contact)

        self.contact_list_label = QLabel('주소록 목록:')
        self.contact_list = QListWidget()
        self.contact_list.itemDoubleClicked.connect(self.edit_contact)
        # 삭제 
        self.contact_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.contact_list.customContextMenuRequested.connect(self.show_context_menu)


        self.save_button = QPushButton('저장')
        self.save_button.clicked.connect(self.save_to_file)
        self.load_button = QPushButton('불러오기')
        self.load_button.clicked.connect(self.load_from_file)

        layout = QVBoxLayout()
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_input)
        layout.addWidget(self.phone_label)
        layout.addWidget(self.phone_input)
        layout.addWidget(self.add_button)
        layout.addWidget(self.search_label)
        layout.addWidget(self.search_input)
        # layout.addWidget(self.search_button)
        layout.addWidget(self.contact_list_label)
        layout.addWidget(self.contact_list)
        layout.addWidget(self.save_button)
        layout.addWidget(self.load_button)

        self.setLayout(layout)

    def edit_contact(self, item):
        # 항목을 더블 클릭했을 때 수정 모드로 진입
        current_text = item.text()
        name, phone = current_text.split(':')
        dialog = EditDialog(self) # 다른 클래스를 호출 합니다. 
        dialog.name_input.setText(name.strip())
        dialog.phone_input.setText(phone.strip())
        if dialog.exec_():
            new_name = dialog.name_input.text()
            new_phone = dialog.phone_input.text()
            self.contacts.pop(name)
            self.contacts[new_name] = new_phone
            self.update_contact_list()

    def delete_contact(self, item):
        # 항목 삭제
        current_text = item.text()
        name, phone = current_text.split(':')
        del self.contacts[name]
        self.update_contact_list()

    def show_context_menu(self, pos):
        # 우클릭 메뉴 표시
        menu = QMenu()
        
        edit_action = menu.addAction(QIcon('D:/Jiwon/myPj01/res/edit.png'),"수  정")
        delete_action = menu.addAction(QIcon('D:/Jiwon/myPj01/res/delete.png'),"삭  제")
        action = menu.exec_(self.contact_list.mapToGlobal(pos))
        if action == delete_action:
            item = self.contact_list.itemAt(pos)
            self.delete_contact(item)
        elif action == edit_action:
            item = self.contact_list.itemAt(pos)
            self.edit_contact(item)
    def add_contact(self):
        name = self.name_input.text()
        phone = self.phone_input.text()

        if name and phone:
            self.contacts[name] = phone  # 주소록에 이름과 전화번호 추가
            self.update_contact_list()
            # QMessageBox.information(self, '추가 성공', f'{name}님의 전화번호 {phone}이(가) 주소록에 추가되었습니다.', QMessageBox.Ok)
        else:
            QMessageBox.warning(self, '입력 오류', '이름과 전화번호를 모두 입력해주세요.', QMessageBox.Ok)

    
    # 리스트박스를 반전             
    def search_contact(self):
        search_text = self.search_input.text().lower()
        for row in range(self.contact_list.count()):
            item = self.contact_list.item(row)
            name, phone = item.text().split(':')
            if search_text in name.strip().lower() or search_text in phone.strip().lower():
                item.setSelected(True)
                 # 아이템이 보이도록 스크롤 조정
                self.contact_list.scrollToItem(item)
            else:
                item.setSelected(False)


    def update_contact_list(self):
        self.contact_list.clear()
        for name, phone in self.contacts.items():
            self.contact_list.addItem(f'{name}: {phone}')

    def save_to_file(self):
        # filename, _ = QFileDialog.getSaveFileName(self, '주소록 저장', '', '텍스트 파일 (*.txt)')
        filename = 'addbook.txt'
        if filename:
            with open(filename, 'w') as file:
                for name, phone in self.contacts.items():
                    file.write(f'{name},{phone}\n')
                QMessageBox.information(self, '저장 성공', f'주소록 파일이 {filename}에 안전하게 저장되었습니다. ', QMessageBox.Ok)

    def load_from_file(self):
        # filename, _ = QFileDialog.getOpenFileName(self, '주소록 불러오기', '', '텍스트 파일 (*.txt)')
        filename = 'addbook.txt'
        if filename:
            self.contacts.clear()
            with open(filename, 'r') as file:
                for line in file:
                    name, phone = line.strip().split(',')
                    self.contacts[name] = phone
            self.update_contact_list()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AddressBook()
    window.show()
    sys.exit(app.exec_())
