from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog_filter(object):
    def setupUi(self, Dialog_filter):
        Dialog_filter.setObjectName("Dialog_filter")
        Dialog_filter.resize(334, 416)
        self.label = QtWidgets.QLabel(Dialog_filter)
        self.label.setGeometry(QtCore.QRect(0, 40, 91, 20))
        self.label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.lineEdit = QtWidgets.QLineEdit(Dialog_filter)
        self.lineEdit.setGeometry(QtCore.QRect(120, 40, 91, 21))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(Dialog_filter)
        self.lineEdit_2.setGeometry(QtCore.QRect(242, 40, 81, 21))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.label_2 = QtWidgets.QLabel(Dialog_filter)
        self.label_2.setGeometry(QtCore.QRect(100, 40, 16, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Dialog_filter)
        self.label_3.setGeometry(QtCore.QRect(220, 40, 16, 16))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(Dialog_filter)
        self.label_4.setGeometry(QtCore.QRect(0, 80, 101, 20))
        self.label_4.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_4.setObjectName("label_4")
        self.lineEdit_3 = QtWidgets.QLineEdit(Dialog_filter)
        self.lineEdit_3.setGeometry(QtCore.QRect(110, 80, 211, 21))
        self.lineEdit_3.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.label_5 = QtWidgets.QLabel(Dialog_filter)
        self.label_5.setGeometry(QtCore.QRect(10, 110, 91, 16))
        self.label_5.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_5.setObjectName("label_5")
        self.comboBox = QtWidgets.QComboBox(Dialog_filter)
        self.comboBox.setGeometry(QtCore.QRect(110, 110, 221, 32))
        self.comboBox.setObjectName("comboBox")
        self.pushButton = QtWidgets.QPushButton(Dialog_filter)
        self.pushButton.setGeometry(QtCore.QRect(162, 380, 161, 32))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.pushButton_2 = QtWidgets.QPushButton(Dialog_filter)
        self.pushButton_2.setGeometry(QtCore.QRect(10, 380, 151, 32))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.setFocusPolicy(QtCore.Qt.NoFocus)

        self.pushButton_2.clicked.connect(self.reset)

        self.retranslateUi(Dialog_filter)
        QtCore.QMetaObject.connectSlotsByName(Dialog_filter)

    def retranslateUi(self, Dialog_filter):
        _translate = QtCore.QCoreApplication.translate
        Dialog_filter.setWindowTitle(_translate("Dialog_filter", "Фильтр"))
        self.label.setText(_translate("Dialog_filter", "Количество"))
        self.label_2.setText(_translate("Dialog_filter", "от"))
        self.label_3.setText(_translate("Dialog_filter", "до"))
        self.label_4.setText(_translate("Dialog_filter", "Название"))
        self.label_5.setText(_translate("Dialog_filter", "Склад"))
        self.pushButton.setText(_translate("Dialog_filter", "Применить"))
        self.pushButton_2.setText(_translate("Dialog_filter", "Cброс"))

    def reset(self):
        self.lineEdit.clear()
        self.lineEdit_2.clear()
        self.lineEdit_3.clear()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog_filter = QtWidgets.QDialog()
    ui = Ui_Dialog_filter()
    ui.setupUi(Dialog_filter)
    Dialog_filter.show()
    sys.exit(app.exec_())
