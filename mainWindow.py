from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QShortcut
from database_class import Database
from actsWindow import Ui_Dialog_Acts
from detailsWindow import Ui_Details
from filterWindow import Ui_Dialog_filter

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(918, 626)
        self.tabWidget = QtWidgets.QTabWidget(Dialog)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 921, 611))
        self.tabWidget.setObjectName("tabWidget")

        self.db = Database("Database1.db")
        goods_data = self.db.table_filling("Goods")
        houses_data = self.db.table_filling("Warehouses")
        orders_data = self.db.table_filling("Orders")
        clients_data = self.db.table_filling("Clients")
        acts_data = self.db.operations()
        table_tabs = []
        table_tabs.append(goods_data[1])
        table_tabs.append(houses_data[1])
        table_tabs.append(orders_data[1])
        table_tabs.append(clients_data[1])
        table_tabs.append(acts_data[1])

        delete_shortcut = QShortcut(QKeySequence(Qt.Key_Backspace), Dialog)
        delete_shortcut.activated.connect(self.delete_row)

        for i in range(5):
            tab = QtWidgets.QWidget()
            tab.setObjectName(f"tab_{i+1}")
            self.tabWidget.addTab(tab, f"Tab {i+1}")

            horizontalLayoutWidget = QtWidgets.QWidget(tab)
            horizontalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 911, 51))
            horizontalLayoutWidget.setObjectName(f"horizontalLayoutWidget_{i+1}")
            horizontalLayout = QtWidgets.QHBoxLayout(horizontalLayoutWidget)
            horizontalLayout.setContentsMargins(0, 0, 0, 0)
            horizontalLayout.setObjectName(f"horizontalLayout_{i+1}")

            for j in range(4):
                if i != 4:
                    if j == 0:
                        button_name = "фильтр"
                    elif j == 1:
                        button_name = "добавить"
                    elif j == 2:
                        button_name = "перезагрузить"
                    elif j == 3:
                        button_name = "сохранить"
                    else:
                        continue
                else:
                    if j == 0:
                        button_name = "фильтр"
                    elif j == 1:
                        button_name = "продажа"
                    elif j == 2:
                        button_name = "приемка"
                    elif j == 3:
                        button_name = "перезагрузить"
                    else:
                        continue
                pushButton = QtWidgets.QPushButton(button_name, horizontalLayoutWidget)
                pushButton.setObjectName(f"pushButton_{i*10+j+1}")
                horizontalLayout.addWidget(pushButton)
                pushButton.setFocusPolicy(QtCore.Qt.NoFocus)

            tableWidget = QtWidgets.QTableWidget(tab)
            tableWidget.setGeometry(QtCore.QRect(0, 50, 911, 531))
            tableWidget.setObjectName(f"tableWidget_{i+1}")
            tableWidget.setSortingEnabled(True)

            if i < len(table_tabs):
                tableWidget.setColumnCount(len(table_tabs[i]))
                for index, value in enumerate(table_tabs[i]):
                    item = QtWidgets.QTableWidgetItem()
                    tableWidget.setHorizontalHeaderItem(index, item)
                    item.setText(value)
                
            else:
                tableWidget.setColumnCount(1)

            content = []
            if i == 0:
                if 0 < len(goods_data[0]):
                    content = goods_data[0]
            elif i == 1:
                if 0 < len(houses_data[0]):
                    content = houses_data[0]
            elif i == 2:
                if 0 < len(orders_data[0]):
                    content = orders_data[0]
            elif i == 3:
                if 0 < len(clients_data[0]):
                    content = clients_data[0]
            else:
                if 0 < len(acts_data[0]):
                    content = acts_data[0]

            if len(content) > 0:
                tableWidget.setRowCount(len(content))
                for index_row, row in enumerate(content):
                    for index_value, value in enumerate(row):
                        item = QtWidgets.QTableWidgetItem(str(value))
                        tableWidget.setItem(index_row, index_value, item)
                        item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEditable)
            else:
                tableWidget.setRowCount(1)

        self.popup = PopupWidget(Dialog)

        for i in [2, 12, 22, 32]:
            button_name = f"pushButton_{i}"
            button = self.tabWidget.findChild(QtWidgets.QPushButton, button_name) 
            if button:
                button.clicked.connect(self.add_row)
        
        for i in [1, 11, 21, 31, 41]:
            button_name = f"pushButton_{i}"
            button = self.tabWidget.findChild(QtWidgets.QPushButton, button_name) 
            if button:
                button.clicked.connect(self.filterWindowShow)
        
        for i in [43]:
            button_name = f"pushButton_{i}"
            button = self.tabWidget.findChild(QtWidgets.QPushButton, button_name) 
            if button:
                button.clicked.connect(lambda _, index=(i): self.show_popup(index))

        self.popup.button1.clicked.connect(lambda _, index=(1): self.actsWindowShow(index))
        self.popup.button2.clicked.connect(lambda _, index=(2): self.actsWindowShow(index))
        self.popup.button3.clicked.connect(lambda _, index=(3): self.actsWindowShow(index))

        for i in range(5):
            current_tb_widget = self.tabWidget.findChild(QtWidgets.QTableWidget, f"tableWidget_{i+1}")
            current_tb_widget.itemClicked.connect(self.on_item_clicked)
            current_tb_widget.cellDoubleClicked.connect(self.cell_double_clicked)

        for i in [42]:
            button_name = f"pushButton_{i}"
            button = self.tabWidget.findChild(QtWidgets.QPushButton, button_name) 
            if button:
                button.clicked.connect(lambda _, index=(i-42): self.actsWindowShow(index))
        
        
        self.retranslateUi(Dialog)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Главное окно"))
        for i in range(5):
            if i == 0:
                tab_name = "Товары"
            elif i == 1:
                tab_name = "Склады"
            elif i == 2:
                tab_name = "Заказы"
            elif i == 3:
                tab_name = "Клиенты"
            else:
                tab_name = "Акты"
            self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabWidget.findChild(QtWidgets.QWidget, f"tab_{i+1}")), _translate("Dialog", tab_name))


    def on_item_clicked(self, item):
            row = item.row()
            table_index = self.tabWidget.currentIndex()
            current_tabel = self.tabWidget.findChild(QtWidgets.QTableWidget, f"tableWidget_{table_index+1}")
            current_tabel.selectRow(row)

    def add_row(self):
        table_index = self.tabWidget.currentIndex()
        current_tabel = self.tabWidget.findChild(QtWidgets.QTableWidget, f"tableWidget_{table_index+1}")
        current_tabel.insertRow(0)

        item = QtWidgets.QTableWidgetItem("autofill")
        current_tabel.setItem(0, 0, item)
        item.setForeground(QtCore.Qt.gray)
        item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEditable)

        for col in range(current_tabel.columnCount()):
            if col > 0:
                item = QtWidgets.QTableWidgetItem()
                current_tabel.setItem(0, col, item)

    def delete_row(self):
        table_index = self.tabWidget.currentIndex()
        current_tabel = self.tabWidget.findChild(QtWidgets.QTableWidget, f"tableWidget_{table_index+1}")
        current_tabel.clearSelection()
        row_number = current_tabel.currentRow()
        # item = self.current_tabel.item(row_number, 0)
        red = QtGui.QColor(255, 143, 135)

        for col in range(current_tabel.columnCount()):
            current_tabel.item(row_number, col).setBackground(red)

    def cell_double_clicked(self, row, column):
        table_index = self.tabWidget.currentIndex()
        current_table = self.tabWidget.findChild(QtWidgets.QTableWidget, f"tableWidget_{table_index+1}")
        item = current_table.item(row, 0)
        item_id = item.text()

        if table_index == 0:
            table_name = "Goods"
        elif table_index == 1:
            table_name = "Warehouses"
        elif table_index == 2:
            table_name = "Orders"
        elif table_index == 3:
            table_name = "Clients"
        elif table_index == 4:
            return
        
        content = self.db.get_data(table_name, item_id)

        self.details_window = Ui_Details(content, table_name=table_name)



    def actsWindowShow(self, index):
        dialog = QtWidgets.QDialog()
        ui_dialog = Ui_Dialog_Acts()
        ui_dialog.setupUi(dialog)
        ui_dialog.comboBox.setCurrentIndex(index)
        dialog.exec_()

    def filterWindowShow(self):
        dialog = QtWidgets.QDialog()
        ui_dialog = Ui_Dialog_filter()
        ui_dialog.setupUi(dialog)
        dialog.exec_()

    def show_popup(self, index):
        button = self.tabWidget.findChild(QtWidgets.QPushButton, f"pushButton_{index}")
        button_width = button.width()
        button_height = button.height()

        button_pos = button.mapToGlobal(button.rect().bottomLeft())
        self.popup.move(button_pos)

        self.popup.setFixedSize(button_width, button_height * 3)
        self.popup.set_button_size(button_width, button_height)

        self.popup.show()

class PopupWidget(QtWidgets.QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Popup)

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.button1 = QtWidgets.QPushButton("приемка", self)
        self.button2 = QtWidgets.QPushButton("списание", self)
        self.button3 = QtWidgets.QPushButton("перемещение", self)

        self.layout.addWidget(self.button1)
        self.layout.addWidget(self.button2)
        self.layout.addWidget(self.button3)
        self.setLayout(self.layout)

    def set_button_size(self, width, height):
        self.button1.setFixedSize(width, height)
        self.button2.setFixedSize(width, height)
        self.button3.setFixedSize(width, height)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
