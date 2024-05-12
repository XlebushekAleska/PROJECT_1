from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(918, 626)
        self.tabWidget = QtWidgets.QTabWidget(Dialog)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 921, 611))
        self.tabWidget.setObjectName("tabWidget")

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

            for j in range(5):
                if i != 4:
                    if j == 0:
                        button_name = "фильтр"
                    elif j == 1:
                        button_name = "удалить"
                    elif j == 2:
                        button_name = "добавить"
                    elif j == 3:
                        button_name = "перезагрузить"
                    else:
                        button_name = "сохранить"
                else:
                    if j == 0:
                        button_name = "продажа"
                    elif j == 1:
                        button_name = "приемка"
                    elif j == 2:
                        button_name = "списание"
                    elif j == 3:
                        button_name = "перемещение"
                    else:
                        continue
                pushButton = QtWidgets.QPushButton(button_name, horizontalLayoutWidget)
                pushButton.setObjectName(f"pushButton_{i*5+j+1}")
                horizontalLayout.addWidget(pushButton)

            tableWidget = QtWidgets.QTableWidget(tab)
            tableWidget.setGeometry(QtCore.QRect(0, 50, 911, 531))
            tableWidget.setObjectName(f"tableWidget_{i+1}")
            tableWidget.setColumnCount(4)
            tableWidget.setRowCount(4)
            for row in range(4):
                for col in range(4):
                    item = QtWidgets.QTableWidgetItem()
                    tableWidget.setItem(row, col, item)

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
        
        
        self.retranslateUi(Dialog)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "CRM"))
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
        row_number = current_tabel.currentRow()
        # item = self.current_tabel.item(row_number, 0)
        red = QtGui.QColor(255, 143, 135)

        for col in range(current_tabel.columnCount()):
            current_tabel.item(row_number, col).setBackground(red)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
