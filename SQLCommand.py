from PyQt5 import QtCore, QtGui, QtWidgets
import ManagementDatase
import sqlite3
import re

class Ui_SQLCommand(object):
    def setupUi(self, SQLCommand):
        SQLCommand.setObjectName("SQLCommand")
        SQLCommand.setFixedSize(914, 637)
        SQLCommand.setStyleSheet("background-color: rgb(208, 226, 255);")
        self.centralwidget = QtWidgets.QWidget(SQLCommand)
        self.centralwidget.setObjectName("centralwidget")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(10, 8, 891, 260))
        self.textEdit.setStyleSheet("\n"
"background-color: rgb(85, 170, 255);")
        self.textEdit.setObjectName("textEdit")
        self.BtnExecutar = QtWidgets.QPushButton(self.centralwidget)
        self.BtnExecutar.setGeometry(QtCore.QRect(800, 270, 101, 31))
        self.BtnExecutar.setObjectName("BtnExecutar")
        self.line_3 = QtWidgets.QFrame(self.centralwidget)
        self.line_3.setGeometry(QtCore.QRect(-10, 302, 1001, 20))
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(11, 325, 891, 271))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(1)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        self.line_4 = QtWidgets.QFrame(self.centralwidget)
        self.line_4.setGeometry(QtCore.QRect(-20, 602, 1011, 20))
        self.line_4.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        SQLCommand.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(SQLCommand)
        self.statusbar.setObjectName("statusbar")
        SQLCommand.setStatusBar(self.statusbar)

        self.retranslateUi(SQLCommand)
        QtCore.QMetaObject.connectSlotsByName(SQLCommand)

        db_name = ManagementDatase.global_db_name

        self.database_connection = sqlite3.connect(db_name)

        self.BtnExecutar.clicked.connect(self.execute_sql_command)

    def retranslateUi(self, SQLCommand):
        _translate = QtCore.QCoreApplication.translate
        SQLCommand.setWindowTitle(_translate("SQLCommand", "EasyTec - SQL Command"))
        self.BtnExecutar.setText(_translate("SQLCommand", "Executar"))
        item = self.tableWidget.horizontalHeaderItem(0)

    def execute_sql_command(self):
        cursor = self.textEdit.textCursor()
        selection_start = cursor.selectionStart()
        selection_end = cursor.selectionEnd()

        selected_text = self.textEdit.toPlainText()[selection_start:selection_end].strip().replace('\n', ' ')

        if selected_text:
            if selected_text.split()[0].upper() in ("SELECT", "INSERT", "UPDATE", "DELETE"):
                sql_command = selected_text
            else:
                QtWidgets.QMessageBox.warning(None, "Erro", "Selecione um comando SQL válido para execução.")
                return
        else:
            all_text = self.textEdit.toPlainText().strip()
            sql_commands = [cmd.strip() for cmd in all_text.split(';') if cmd.strip()]

            if len(sql_commands) == 1 and sql_commands[0].split()[0].upper() in (
                    "SELECT", "INSERT", "UPDATE", "DELETE"):
                sql_command = sql_commands[0]
            else:
                QtWidgets.QMessageBox.warning(None, "Erro", "Selecione apenas um comando SQL válido para execução.")
                return

        try:
            cursor = self.database_connection.cursor()
            cursor.execute(sql_command)
            self.database_connection.commit()


            if sql_command.upper().startswith("SELECT"):
                results = cursor.fetchall()
                column_names = [description[0] for description in cursor.description]

                self.tableWidget.setColumnCount(len(column_names))
                self.tableWidget.setHorizontalHeaderLabels(column_names)

                self.tableWidget.setRowCount(len(results))

                for row_index, row_data in enumerate(results):
                    for column_index, column_data in enumerate(row_data):
                        self.tableWidget.setItem(row_index, column_index,
                                                 QtWidgets.QTableWidgetItem(str(column_data)))
            else:
                self.tableWidget.clear()

            cursor.close()
        except sqlite3.Error as e:
            QtWidgets.QMessageBox.critical(None, "Erro", f"Erro ao executar o comando SQL: {e}")
            self.database_connection.rollback()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    SQLCommand = QtWidgets.QMainWindow()
    ui = Ui_SQLCommand()
    ui.setupUi(SQLCommand)
    SQLCommand.show()
    sys.exit(app.exec_())
