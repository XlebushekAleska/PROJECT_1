from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QFormLayout, QPushButton, QHBoxLayout, QMessageBox
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from database_class import Database


class Ui_Add_Window(QWidget):
    def __init__(self, table_name):
        super().__init__()
        
        self.widgets = {}
        self.finish_dict = []

        self.db = Database("Database1.db")
        self.table_name = table_name
        self.columns = self.db.get_column_names(table_name)
        
        form_layout = QFormLayout()
        
        for label in self.columns:
            lbl = QLabel(label)
            if label == 'id':
                widget = QLabel("autofill")
                widget.setStyleSheet("color: gray;")
            else:
                widget = QLineEdit('')
                widget.setFixedWidth(90)
            self.widgets[lbl.text()] = widget
            form_layout.addRow(lbl, widget)
        
        btn_cancel = QPushButton('Очистить')
        self.btn_add = QPushButton('Добавить')

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(btn_cancel)
        btn_layout.addWidget(self.btn_add)

        self.btn_add.clicked.connect(self.showConfirmationDialog)
        btn_cancel.clicked.connect(self.cancel_button)
        
        main_layout = QVBoxLayout()
        main_layout.addLayout(form_layout)
        main_layout.addLayout(btn_layout)
        
        self.setLayout(main_layout)
        self.setWindowTitle('Добавление объекта')
        self.show()

    def cancel_button(self):
        reversed_dict = {v: k for k, v in self.widgets.items()}
        for value, key in reversed_dict.items():
                if key != 'id':
                    widg = self.widgets.get(key)
                    widg.setText("")

    
    def add_object(self):
        reversed_dict = {v: k for k, v in self.widgets.items()}
        for value, key in reversed_dict.items():
                widg = self.widgets.get(key)
                if key != "id":
                    if value != "":
                        self.finish_dict.append(widg.text())
                    else:
                         self.finish_dict.append("None")
        if len(self.finish_dict) > 0:
            send_dict = self.finish_dict
            self.db.set_data(table_name=self.table_name, data=send_dict)

    def showConfirmationDialog(self):
        reply = QMessageBox.question(self, 'Confirmation', 'Уверены, что хотите добавить этот объект?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            self.add_object()
            self.close()


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    form = Ui_Add_Window("Goods")
    sys.exit(app.exec_())
