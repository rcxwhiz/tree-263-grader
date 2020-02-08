# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'xlsxfiles.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtWidgets

import helper_tools


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        self.stud_index = 0
        self.excel_data = helper_tools.io_data.ExcelResults()

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1404, 882)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.key_label = QtWidgets.QLabel(self.centralwidget)
        self.key_label.setGeometry(QtCore.QRect(50, 40, 641, 16))
        self.key_label.setObjectName("key_label")
        self.student_label = QtWidgets.QLabel(self.centralwidget)
        self.student_label.setGeometry(QtCore.QRect(750, 40, 631, 20))
        self.student_label.setObjectName("student_label")
        self.key_sheet_turner = QtWidgets.QSpinBox(self.centralwidget)
        self.key_sheet_turner.setGeometry(QtCore.QRect(10, 40, 31, 16))
        self.key_sheet_turner.setObjectName("key_sheet_turner")
        self.student_sheet_turner = QtWidgets.QSpinBox(self.centralwidget)
        self.student_sheet_turner.setGeometry(QtCore.QRect(710, 40, 31, 16))
        self.student_sheet_turner.setObjectName("student_sheet_turner")
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
        self.student_table = QtWidgets.QTableWidget(self.widget1)
        self.student_table.setObjectName("student_table")
        self.student_table.setColumnCount(0)
        self.student_table.setRowCount(0)
        self.display_container.addWidget(self.student_table, 0, 1, 1, 1)
        self.key_table = QtWidgets.QTableWidget(self.widget1)
        self.key_table.setObjectName("key_table")
        self.key_table.setColumnCount(0)
        self.key_table.setRowCount(0)
        self.display_container.addWidget(self.key_table, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.josh_hooks(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("Tree 263 xlsx Grader", "Tree 263 xlsx Grader"))
        self.key_label.setText(_translate("MainWindow", "TextLabel"))
        self.student_label.setText(_translate("MainWindow", "TextLabel"))
        self.previous_file_button.setText(_translate("MainWindow", "PushButton"))
        self.next_file_botton.setText(_translate("MainWindow", "PushButton"))

    def josh_hooks(self, MainWindow):
        self.previous_file_button.clicked.connect(self.move_page_back)
        self.next_file_botton.clicked.connect(self.move_page_forward)

        self.key_sheet_turner.setMinimum(1)
        self.key_sheet_turner.setRange(1, len(self.excel_data.key['sheets']))
        self.key_sheet_turner.setValue(1)
        self.student_sheet_turner.setMinimum(1)
        self.student_sheet_turner.setValue(1)
        self.key_sheet_turner.valueChanged.connect(self.update_page)
        self.student_sheet_turner.valueChanged.connect(self.update_page)

        self.update_page()

    def move_page_back(self):
        self.stud_index -= 1
        self.student_sheet_turner.setValue(1)
        self.update_page()

    def move_page_forward(self):
        self.stud_index += 1
        self.student_sheet_turner.setValue(1)
        self.update_page()

    def update_page(self):
        self.student_sheet_turner.setMaximum(len(self.excel_data.students[self.stud_index]['sheets']))

        if self.stud_index < 0:
            self.stud_index += self.excel_data.num_students
        elif self.stud_index >= self.excel_data.num_students:
            self.stud_index -= self.excel_data.num_students

        self.current_key_sheet_key = list(self.excel_data.key['sheets'].keys())[self.key_sheet_turner.value() - 1]
        self.current_student_sheet_key = list(self.excel_data.students[self.stud_index]['sheets'].keys())[self.student_sheet_turner.value() - 1]
        self.key_label.setText(f'{self.excel_data.key["file name"]} - {self.current_key_sheet_key}')
        self.student_label.setText(f'{self.excel_data.students[self.stud_index]["name"]} - {self.excel_data.students[self.stud_index]["file name"]} - {self.current_student_sheet_key}')

        self.next_file_botton.setText(self.excel_data.students[(self.stud_index + 1) % self.excel_data.num_students]['name'])
        self.previous_file_button.setText(self.excel_data.students[self.stud_index - 1]['name'])

        self.update_tables()

    def update_tables(self):
        key_arr = self.excel_data.key['sheets'][self.current_key_sheet_key]
        stud_arr = self.excel_data.students[self.stud_index]['sheets'][self.current_student_sheet_key]

        self.key_table.setRowCount(len(key_arr))
        self.key_table.setColumnCount(len(key_arr[0]))
        for i in range(len(key_arr)):
            for j in range(len(key_arr[0])):
                if key_arr[i][j] is None:
                    setting_item = QtWidgets.QTableWidgetItem('')
                else:
                    setting_item = QtWidgets.QTableWidgetItem(str(key_arr[i][j]))
                self.key_table.setItem(i, j, setting_item)

        self.student_table.setRowCount(len(stud_arr))
        self.student_table.setColumnCount(len(stud_arr[0]))
        for i in range(len(stud_arr)):
            for j in range(len(stud_arr[0])):
                if stud_arr[i][j] is None:
                    setting_item = QtWidgets.QTableWidgetItem('')
                else:
                    setting_item = QtWidgets.QTableWidgetItem(str(stud_arr[i][j]))
                self.student_table.setItem(i, j, setting_item)


def xlsx_ui():
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
