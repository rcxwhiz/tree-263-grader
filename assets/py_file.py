# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtWidgets

# Form implementation generated from reading ui file 'pyfiles.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!
import helper_tools


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        self.code_index = 0
        self.io_data = helper_tools.io_data.IOResults()

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1404, 882)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.key_label = QtWidgets.QLabel(self.centralwidget)
        self.key_label.setGeometry(QtCore.QRect(10, 40, 691, 16))
        self.key_label.setObjectName("key_label")
        self.student_label = QtWidgets.QLabel(self.centralwidget)
        self.student_label.setGeometry(QtCore.QRect(710, 30, 671, 20))
        self.student_label.setObjectName("student_label")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(20, 10, 521, 25))
        self.widget.setObjectName("widget")
        self.button_container = QtWidgets.QHBoxLayout(self.widget)
        self.button_container.setContentsMargins(0, 0, 0, 0)
        self.button_container.setObjectName("button_container")
        self.previous_file_button = QtWidgets.QPushButton(self.widget)
        self.previous_file_button.setObjectName("previous_file_button")
        self.button_container.addWidget(self.previous_file_button)
        self.next_file_botton = QtWidgets.QPushButton(self.widget)
        self.next_file_botton.setObjectName("next_file_botton")
        self.button_container.addWidget(self.next_file_botton)
        self.widget1 = QtWidgets.QWidget(self.centralwidget)
        self.widget1.setGeometry(QtCore.QRect(10, 60, 1381, 811))
        self.widget1.setObjectName("widget1")
        self.display_container = QtWidgets.QGridLayout(self.widget1)
        self.display_container.setContentsMargins(0, 0, 0, 0)
        self.display_container.setObjectName("display_container")
        self.key_source_display = QtWidgets.QTextBrowser(self.widget1)
        self.key_source_display.setObjectName("key_source_display")
        self.display_container.addWidget(self.key_source_display, 0, 0, 1, 1)
        self.student_source_display = QtWidgets.QTextBrowser(self.widget1)
        self.student_source_display.setObjectName("student_source_display")
        self.display_container.addWidget(self.student_source_display, 0, 1, 1, 1)
        self.key_out_display = QtWidgets.QTextBrowser(self.widget1)
        self.key_out_display.setObjectName("key_out_display")
        self.display_container.addWidget(self.key_out_display, 1, 0, 1, 1)
        self.student_out_display = QtWidgets.QTextBrowser(self.widget1)
        self.student_out_display.setObjectName("student_out_display")
        self.display_container.addWidget(self.student_out_display, 1, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.josh_hooks(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("Tree 263 py Grader", "Tree 263 py Grader"))
        self.key_label.setText(_translate("MainWindow", "TextLabel"))
        self.student_label.setText(_translate("MainWindow", "TextLabel"))
        self.previous_file_button.setText(_translate("MainWindow", "PushButton"))
        self.next_file_botton.setText(_translate("MainWindow", "PushButton"))

    def josh_hooks(self, MainWindow):
        self.previous_file_button.clicked.connect(self.move_page_back)
        self.next_file_botton.clicked.connect(self.move_page_forward)
        self.update_page()

    def move_page_back(self):
        self.code_index -= 1
        self.update_page()

    def move_page_forward(self):
        self.code_index += 1
        self.update_page()

    def update_page(self):
        if self.code_index < 0:
            self.code_index += self.io_data.num_students
        elif self.code_index >= self.io_data.num_students:
            self.code_index -= self.io_data.num_students

        self.key_label.setText(f'Key - {self.io_data.key["file name"]}')
        self.student_label.setText(f'{self.io_data.students[self.code_index]["name"]} - {self.code_index + 1}/{self.io_data.num_students} - {self.io_data.students[self.code_index]["file name"]}')

        self.next_file_botton.setText(self.io_data.students[(self.code_index + 1) % self.io_data.num_students]['name'])
        self.previous_file_button.setText(self.io_data.students[self.code_index - 1]['name'])

        self.key_source_display.setText(self.io_data.key['source'])
        self.key_out_display.setText(self.io_data.key['out'])
        self.student_source_display.setText(self.io_data.students[self.code_index]['source'])
        self.student_out_display.setText(self.io_data.students[self.code_index]['out'])



def py_ui():
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
