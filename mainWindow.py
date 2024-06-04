from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QShortcut, QApplication, QMessageBox
from database_class import Database
from actsWindow import Ui_Dialog_Acts
from detailsWindow import Ui_Details
from filterWindow import Ui_Dialog_filter
from addWindow import Ui_Add_Window

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(918, 626)
        self.tabWidget = QtWidgets.QTabWidget(Dialog)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 921, 611))
        self.tabWidget.setObjectName("tabWidget")

        self.db = Database("Database1.db")
        self.goods_data = self.db.table_filling("Goods")
        self.houses_data = self.db.table_filling("Warehouses")
        self.orders_data = self.db.table_filling("Orders")
        self.clients_data = self.db.table_filling("Clients")
        self.acts_data = self.db.operations()
        table_tabs = []
        table_tabs.append(self.goods_data[1])
        table_tabs.append(self.houses_data[1])
        table_tabs.append(self.orders_data[1])
        table_tabs.append(self.clients_data[1])
        table_tabs.append(self.acts_data[1])

        self.del_buf = {}

        main_window = QApplication.instance().activeWindow()
        if main_window:
            main_window.close()

        delete_shortcut = QShortcut(QKeySequence(Qt.Key_Backspace), Dialog)
        delete_shortcut.activated.connect(self.delete_object)

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
                if 0 < len(self.goods_data[0]):
                    content = self.goods_data[0]
            elif i == 1:
                if 0 < len(self.houses_data[0]):
                    content = self.houses_data[0]
            elif i == 2:
                if 0 < len(self.orders_data[0]):
                    content = self.orders_data[0]
            elif i == 3:
                if 0 < len(self.clients_data[0]):
                    content = self.clients_data[0]
            else:
                if 0 < len(self.acts_data[0]):
                    content = self.acts_data[0]

            if len(content) > 0:
                tableWidget.setRowCount(len(content))
                for index_row, row in enumerate(content):
                    for index_value, value in enumerate(row):
                        item = QtWidgets.QTableWidgetItem(str(value))
                        tableWidget.setItem(index_row, index_value, item)
                        item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEditable)
            else:
                tableWidget.setRowCount(0)

        self.popup = PopupWidget(Dialog)

        for i in [2, 12, 22, 32]:
            button_name = f"pushButton_{i}"
            button = self.tabWidget.findChild(QtWidgets.QPushButton, button_name) 
            if button:
                button.clicked.connect(self.add_object)
        
        for i in [1, 11, 21, 31, 41]:
            button_name = f"pushButton_{i}"
            button = self.tabWidget.findChild(QtWidgets.QPushButton, button_name) 
            if button:
                button.clicked.connect(self.filterWindowShow)
        
        for i in [3, 13, 23, 33, 44]:
            button_name = f"pushButton_{i}"
            button = self.tabWidget.findChild(QtWidgets.QPushButton, button_name) 
            if button:
                button.clicked.connect(self.reload_table)
        
        for i in [43]:
            button_name = f"pushButton_{i}"
            button = self.tabWidget.findChild(QtWidgets.QPushButton, button_name) 
            if button:
                button.clicked.connect(lambda _, index=(i): self.show_popup(index))

        self.popup.button1.clicked.connect(lambda _, table_name=("Receipt"): self.add_act_object(table_name))
        self.popup.button2.clicked.connect(lambda _, table_name=("Write_off"): self.add_act_object(table_name))
        self.popup.button3.clicked.connect(lambda _, table_name=("Transfer"): self.add_act_object(table_name))

        for i in range(5):
            current_tb_widget = self.tabWidget.findChild(QtWidgets.QTableWidget, f"tableWidget_{i+1}")
            current_tb_widget.itemClicked.connect(self.on_item_clicked)
            current_tb_widget.cellDoubleClicked.connect(self.cell_double_clicked)

        for i in [42]:
            button_name = f"pushButton_{i}"
            button = self.tabWidget.findChild(QtWidgets.QPushButton, button_name) 
            if button:
                button.clicked.connect(lambda _, table_name=("Sale"): self.add_act_object(table_name))
        
        
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

    def add_act_object(self, table_name):
        self.add_window = Ui_Add_Window(table_name)

    def get_current_table_name(self):
        table_index = self.tabWidget.currentIndex()
        current_table = self.tabWidget.findChild(QtWidgets.QTableWidget, f"tableWidget_{table_index+1}")
        if table_index == 0:
            table_name = "Goods"
        elif table_index == 1:
            table_name = "Warehouses"
        elif table_index == 2:
            table_name = "Orders"
        elif table_index == 3:
            table_name = "Clients"
        elif table_index == 4:
            table_name = None
        
        return current_table, table_name


    def add_object(self):
        current_table, table_name = self.get_current_table_name()
        if table_name == None:
            return
        
        current_table.insertRow(0)

        item = QtWidgets.QTableWidgetItem("autofill")
        current_table.setItem(0, 0, item)
        item.setForeground(QtCore.Qt.gray)
        item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEditable)
        
        self.add_window = Ui_Add_Window(table_name)
        self.add_window.btn_add.clicked.connect(self.fill_add_row)

    def fill_add_row(self):
        current_table, _ = self.get_current_table_name()

        insert_data = self.add_window.finish_dict
        self.add_window.close()
        for col, value in enumerate(insert_data):
            if col > 0:
                item = QtWidgets.QTableWidgetItem(str(value))
                current_table.setItem(0, col, item)

    def delete_object(self):
        current_table, table_name = self.get_current_table_name()
        if table_name == None:
            return
        
        row_number = current_table.currentRow()
        item = current_table.item(row_number, 0)
        id_object = item.text()
        
        red = QtGui.QColor(255, 143, 135)
        default_color = QtGui.QColor(QtCore.Qt.white)
        reply2 = None
        reply1 = None
        
        if item:
            background_color = item.background().color()
            target_color = red
            if background_color == target_color:
                reply2 = QMessageBox.question(Dialog, 'Confirmation', 'Уверены, что хотите отменить удаление этого объекта?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            else:
                reply1 = QMessageBox.question(Dialog, 'Confirmation', 'Уверены, что хотите удалить этот объект?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if reply1 == QMessageBox.Yes:
            self.show_color_row(red)
            if table_name in self.del_buf:
                self.del_buf[table_name].append(id_object)
            else:
                self.del_buf[table_name] = [id_object]
        
        if reply2 is not None and reply2 == QMessageBox.Yes:
            if table_name in self.del_buf:
                if id_object in self.del_buf[table_name]:
                    self.del_buf[table_name].remove(id_object)
                    if not self.del_buf[table_name]:
                        del self.del_buf[table_name]
            self.show_color_row(default_color)

        

    def show_color_row(self, color):
        current_tabel, _ = self.get_current_table_name()
        current_tabel.clearSelection()
        row_number = current_tabel.currentRow()

        for col in range(current_tabel.columnCount()):
            current_tabel.item(row_number, col).setBackground(color)

    def cell_double_clicked(self, row, column):
        current_table, table_name = self.get_current_table_name()
        if table_name == None:
            return
        
        item = current_table.item(row, 0)

        if item:
            item_id = item.text()
        else:
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
        table_index = self.tabWidget.currentIndex()

        self.filter_window = Ui_Dialog_filter(table_index)
        self.filter_window.apply_button.clicked.connect(self.reload_with_filter)

        self.filter_window.exec_()

    def reload_with_filter(self):
        current_table, _ = self.get_current_table_name()

        config = self.filter_window.config
        filter = self.filter_window.finish_filter

        if config == 0:
            try:
                data = self.db.filter_goods(**filter)
            except Exception as e:
                QMessageBox.warning(None,"Ошибка запроса", "Ошибка при выполнении запроса:\n "+str(e))
                return
        elif config == 1:
            try:
                data = self.db.filter_wharehouses(**filter)
            except Exception as e:
                QMessageBox.warning(None,"Ошибка запроса", "Ошибка при выполнении запроса:\n "+str(e))
                return
        elif config == 2:
            try:
                data = self.db.filter_orders(**filter)
            except Exception as e:
                QMessageBox.warning(None,"Ошибка запроса", "Ошибка при выполнении запроса:\n "+str(e))
                return
        elif config == 3:
            try:
                data = self.db.filter_clients(**filter)
            except Exception as e:
                QMessageBox.warning(None,"Ошибка запроса", "Ошибка при выполнении запроса:\n "+str(e))
                return
        elif config == 4:
            inter = filter['операция']
            if inter != "последние":
                if inter == "продажа":
                    tb_name = "Sale"
                elif inter == "приемка":
                    tb_name = "Receipt"
                elif inter == "списание":
                    tb_name = "Write_off"
                elif inter == "перемещение":
                    tb_name = "Transfer"
                data = self.db.table_filling(tb_name)
            else:
                data = self.db.operations()
            table_tabs = data[1]

            current_table.setColumnCount(len(table_tabs))
            for index, value in enumerate(table_tabs):
                item = QtWidgets.QTableWidgetItem()
                current_table.setHorizontalHeaderItem(index, item)
                item.setText(value)

        
        content = data[0]
        
        if len(content) > 0:
            current_table.setRowCount(len(content))
            for index_row, row in enumerate(content):
                for index_value, value in enumerate(row):
                    item = QtWidgets.QTableWidgetItem(str(value))
                    current_table.setItem(index_row, index_value, item)
                    item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEditable)
        else:
            current_table.setRowCount(0)


    def show_popup(self, index):
        button = self.tabWidget.findChild(QtWidgets.QPushButton, f"pushButton_{index}")
        button_width = button.width()
        button_height = button.height()

        button_pos = button.mapToGlobal(button.rect().bottomLeft())
        self.popup.move(button_pos)

        self.popup.setFixedSize(button_width, button_height * 3)
        self.popup.set_button_size(button_width, button_height)

        self.popup.show()

    def reload_table(self):
        table_index = self.tabWidget.currentIndex()
        current_table, _ = self.get_current_table_name()

        if self.del_buf:
            for key, values in self.del_buf.items():
                for value in values:
                    self.db.delete_data(key, value)
            self.del_buf = {}

        content = []

        if table_index == 0:
            self.goods_data = self.db.table_filling("Goods")
            if 0 < len(self.goods_data[0]):
                content = self.goods_data[0]
        elif table_index == 1:
            self.houses_data = self.db.table_filling("Warehouses")
            if 0 < len(self.houses_data[0]):
                content = self.houses_data[0]
        elif table_index == 2:
            self.orders_data = self.db.table_filling("Orders")
            if 0 < len(self.orders_data[0]):
                content = self.orders_data[0]
        elif table_index == 3:
            self.clients_data = self.db.table_filling("Clients")
            if 0 < len(self.clients_data[0]):
                content = self.clients_data[0]
        else:
            self.acts_data = self.db.operations()
            if 0 < len(self.acts_data[0]):
                content = self.acts_data[0]
        if len(content) > 0:
            current_table.setRowCount(len(content))
            for index_row, row in enumerate(content):
                for index_value, value in enumerate(row):
                    item = QtWidgets.QTableWidgetItem(str(value))
                    current_table.setItem(index_row, index_value, item)
                    item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEditable)
        else:
            current_table.setRowCount(0)



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
