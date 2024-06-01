import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QFormLayout, QPushButton, QHBoxLayout, QShortcut, QMessageBox, QFileDialog
from PyQt5 import QtCore
from PyQt5.QtGui import QKeySequence, QPixmap
from PyQt5.QtCore import Qt
from database_class import Database


class Ui_Details(QWidget):
    def __init__(self, content, table_name):
        super().__init__()
        
        data, labels = content
        self.widgets = {}

        self.start_dict = {}
        self.finish_dict = {}

        self.db = Database("Database1.db")
        self.table_name = table_name
        
        form_layout = QFormLayout()
        
        for label, value in zip(labels, data):
            lbl = QLabel(label)
            if label == 'id':
                widget = QLabel(str(value))
            elif label == 'picture':
                self.picture_label = QLabel(self)
                self.load_image(value)
                self.im_path = value
                widget = QPushButton('Выбрать картинку', self)
                widget.setEnabled(False)
                widget.clicked.connect(self.change_picture)
                self.change_picture_button = widget
                form_layout.addRow(self.picture_label)
            else:
                widget = QLineEdit(str(value) if value is not None else '')
                text_width = widget.fontMetrics().boundingRect(widget.text()).width()
                if text_width > 90:
                    widget.setFixedWidth(text_width + 10)
                else:
                    widget.setFixedWidth(90)
                widget.setFocusPolicy(QtCore.Qt.NoFocus)
            self.widgets[lbl.text()] = widget
            form_layout.addRow(lbl, widget)
        
        self.btn_delete = QPushButton('Удалить')
        self.btn_change = QPushButton('Изменить')
        self.btn_save = QPushButton('Сохранить')

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.btn_delete)
        btn_layout.addWidget(self.btn_change)
        btn_layout.addWidget(self.btn_save)

        delete_shortcut = QShortcut(QKeySequence(Qt.Key_Backspace), self)
        delete_shortcut.activated.connect(self.showConfirmationDialog)

        self.btn_change.clicked.connect(self.change_cancel_button)
        self.btn_delete.clicked.connect(self.showConfirmationDialog)
        self.btn_save.clicked.connect(self.return_changes)
        
        main_layout = QVBoxLayout()
        main_layout.addLayout(btn_layout)
        main_layout.addLayout(form_layout)
        
        self.setLayout(main_layout)
        self.setWindowTitle('Подробности объекта')
        self.show()

    def load_image(self, image_path):
        if image_path:
            pixmap = QPixmap(image_path)
            self.picture_label.setPixmap(pixmap.scaled(200, 200, Qt.KeepAspectRatio))
            self.finish_dict['picture'] = image_path

    def change_picture(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Images (*.png *.xpm *.jpg *.jpeg *.bmp)", options=options)
        if file_name:
            self.load_image(file_name)
            self.finish_dict['picture'] = file_name

    def change_cancel_button(self):
        current_text = self.btn_change.text()
        reversed_dict = {v: k for k, v in self.widgets.items()}
        
        if current_text == 'Отменить изменения':
            self.btn_change.setText('Изменить')
            self.btn_change.setStyleSheet("")
            self.change_picture_button.setEnabled(False)
            for value, key in reversed_dict.items():
                if key != "id" and key != "picture":
                    widg = self.widgets.get(key)
                    widg.setFocusPolicy(QtCore.Qt.NoFocus)
                    widg.clearFocus()
                    widg.setText(self.start_dict[key])
                elif key == "picture":
                    self.load_image(self.start_dict[key])
            self.finish_dict = {}
        else:
            self.btn_change.setText('Отменить изменения')
            self.btn_change.setStyleSheet("background-color: #AFB5B9; color: white;")
            self.change_picture_button.setEnabled(True)
            for value, key in reversed_dict.items():
                if key != "id":
                    widg = self.widgets.get(key)
                    widg.setFocusPolicy(QtCore.Qt.StrongFocus)
                    self.start_dict[key] = widg.text()
                    self.finish_dict[key] = widg.text()
                    if key != "picture":
                        widg.textChanged.connect(self.changed_object)
                    else:
                        self.start_dict[key] = self.im_path

    def delete_item(self):
        id_wgt = self.widgets.get("id")
        id = id_wgt.text()
        self.db.delete_data(self.table_name, id)
    
    def changed_object(self):
        reversed_dict = {v: k for k, v in self.widgets.items()}
        for value, key in reversed_dict.items():
            if key != "id" and key != "picture":
                widg = self.widgets.get(key)
                self.finish_dict[key] = widg.text()
    
    def return_changes(self):
        id_wgt = self.widgets.get("id")
        id = id_wgt.text()
        if self.finish_dict != {}:
            self.finish_dict['picture'] = self.im_path
            send_dict = self.finish_dict
            self.db.change_data(table_name=self.table_name, row_id=int(id), data=send_dict)
            self.change_cancel_button()
            self.close()

    def showConfirmationDialog(self):
        reply = QMessageBox.question(self, 'Confirmation', 'Уверены, что хотите удалить этот объект?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            self.delete_item()
            self.close()


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    content = ((3, 'kdrfq', 'werfc', 's', 'sfdv', None, '22'), ['id', 'name', 'article', 'category', 'charasteristic', 'picture', 'price'])
    form = Ui_Details(content, "Goods")
    sys.exit(app.exec_())
