from PyQt5 import QtCore, QtGui, QtWidgets
from database_class import Database


class Ui_Dialog_Acts(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(678, 453)
        self.horizontalLayoutWidget = QtWidgets.QWidget(Dialog)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(0, 10, 671, 38))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.comboBox = QtWidgets.QComboBox(self.horizontalLayoutWidget)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.horizontalLayout.addWidget(self.comboBox)
        self.pushButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.horizontalLayout.addWidget(self.pushButton)
        self.pushButton_2 = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.setFocusPolicy(QtCore.Qt.NoFocus)
        self.horizontalLayout.addWidget(self.pushButton_2)
        self.pushButton_3 = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.setFocusPolicy(QtCore.Qt.NoFocus)
        self.horizontalLayout.addWidget(self.pushButton_3)
        self.tableWidget = QtWidgets.QTableWidget(Dialog)
        self.tableWidget.setGeometry(QtCore.QRect(0, 50, 671, 391))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)

        self.comboBox.currentIndexChanged.connect(self.show_table)
        self.tableWidget.itemClicked.connect(self.on_item_clicked)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Акты"))
        self.comboBox.setItemText(0, _translate("Dialog", "Продажа"))
        self.comboBox.setItemText(1, _translate("Dialog", "Приемка"))
        self.comboBox.setItemText(2, _translate("Dialog", "Списание"))
        self.comboBox.setItemText(3, _translate("Dialog", "Перемещение"))
        self.pushButton.setText(_translate("Dialog", "новый акт"))
        self.pushButton_2.setText(_translate("Dialog", "удалить"))
        self.pushButton_3.setText(_translate("Dialog", "перезагрузить"))

        db = Database("Database1.db")
        self.sale_data = db.table_filling("Sale")
        self.receipt_data = db.table_filling("Receipt")
        self.write_off_data = db.table_filling("Write_off")
        self.transfer_data = db.table_filling("Transfer")
        self.table_tabs = []
        self.table_tabs.append(self.sale_data[1])
        self.table_tabs.append(self.receipt_data[1])
        self.table_tabs.append(self.write_off_data[1])
        self.table_tabs.append(self.transfer_data[1])

        tableWidget = QtWidgets.QTableWidget()
        tableWidget.setGeometry(QtCore.QRect(0, 50, 911, 531))
        tableWidget.setObjectName(f"tableWidget")
        self.show_table()


    def show_table(self):
        selected_index = self.comboBox.currentIndex()
        self.tableWidget.setColumnCount(len(self.table_tabs[selected_index]))
        content = []

        for index, value in enumerate(self.table_tabs[selected_index]):
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget.setHorizontalHeaderItem(index, item)
            item.setText(value)
        
        if selected_index == 0:
            content = self.sale_data[0]
        elif selected_index == 1:
            content = self.receipt_data[0]
        elif selected_index == 2:
            content = self.write_off_data[0]
        else:
            content = self.transfer_data[0]

        size_of_row = len(content)
        self.tableWidget.setRowCount(size_of_row)

        for index_row, row in enumerate(content):
            for index_value, value in enumerate(row):
                item = QtWidgets.QTableWidgetItem(str(value))
                self.tableWidget.setItem(index_row, index_value, item)
                item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEditable)

    def on_item_clicked(self, item):
            row = item.row()
            self.tableWidget.selectRow(row)




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog_Acts()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
