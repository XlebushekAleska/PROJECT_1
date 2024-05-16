from PyQt5 import QtCore, QtGui, QtWidgets
from database_class import Database
from actsWindow import Ui_Dialog_Acts

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(918, 626)
        self.tabWidget = QtWidgets.QTabWidget(Dialog)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 921, 611))
        self.tabWidget.setObjectName("tabWidget")

        db = Database("Database1.db")
        goods_data = db.table_filling("Goods")
        houses_data = db.table_filling("Warehouses")
        orders_data = db.table_filling("Orders")
        clients_data = db.table_filling("Clients")
        acts_data = db.operations()
        table_tabs = []
        table_tabs.append(goods_data[1])
        table_tabs.append(houses_data[1])
        table_tabs.append(orders_data[1])
        table_tabs.append(clients_data[1])
        # table_tabs.append(acts_data[1])

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

            for j in range(6):
                if i != 4:
                    if j == 0:
                        button_name = "фильтр"
                    elif j == 1:
                        button_name = "удалить"
                    elif j == 2:
                        button_name = "добавить"
                    elif j == 3:
                        button_name = "изменить"
                    elif j == 4:
                        button_name = "перезагрузить"
                    else:
                        button_name = "сохранить"
                else:
                    if j == 0:
                        button_name = "фильтр"
                    elif j == 1:
                        button_name = "продажа"
                    elif j == 2:
                        button_name = "приемка"
                    elif j == 3:
                        button_name = "списание"
                    elif j == 4:
                        button_name = "перемещение"
                    else:
                        button_name = "перезагрузить"
                pushButton = QtWidgets.QPushButton(button_name, horizontalLayoutWidget)
                pushButton.setObjectName(f"pushButton_{i*5+j+1}")
                horizontalLayout.addWidget(pushButton)
                pushButton.setFocusPolicy(QtCore.Qt.NoFocus)

            tableWidget = QtWidgets.QTableWidget(tab)
            tableWidget.setGeometry(QtCore.QRect(0, 50, 911, 531))
            tableWidget.setObjectName(f"tableWidget_{i+1}")

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

        for i in [3, 8, 13, 18]:
            button_name = f"pushButton_{i}"
            button = self.tabWidget.findChild(QtWidgets.QPushButton, button_name) 
            if button:
                button.clicked.connect(self.add_row)
        
        for i in [2, 7, 12, 17]:
            button_name = f"pushButton_{i}"
            button = self.tabWidget.findChild(QtWidgets.QPushButton, button_name) 
            if button:
                button.clicked.connect(self.delete_row)

        for i in range(5):
            current_tb_widget = self.tabWidget.findChild(QtWidgets.QTableWidget, f"tableWidget_{i+1}")
            current_tb_widget.itemClicked.connect(self.on_item_clicked)

        for i in [22, 23, 24, 25]:
            button_name = f"pushButton_{i}"
            button = self.tabWidget.findChild(QtWidgets.QPushButton, button_name) 
            if button:
                button.clicked.connect(lambda _, index=(i-22): self.actsWindowShow(index))
        
        
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

    def actsWindowShow(self, index):
        dialog = QtWidgets.QDialog()
        ui_dialog = Ui_Dialog_Acts()
        ui_dialog.setupUi(dialog)
        ui_dialog.comboBox.setCurrentIndex(index)
        dialog.exec_()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
