from PyQt5 import QtCore, QtGui, QtWidgets
import sqlite3
from CriarTabela import Ui_CriarTabela
from CriarCampos import Ui_CriarCampos
from SQLCommand import Ui_SQLCommand

class Ui_ManagementDatabase(object):
    def setupUi(self, ManagementDatabase):
        ManagementDatabase.setObjectName("ManagementDatabase")
        ManagementDatabase.setFixedSize(678, 508)
        ManagementDatabase.setStyleSheet("background-color: rgb(208, 226, 255);")
        self.centralwidget = QtWidgets.QWidget(ManagementDatabase)
        self.centralwidget.setObjectName("centralwidget")
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(0, 10, 1131, 16))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.BtnCriarTabelas = QtWidgets.QPushButton(self.centralwidget)
        self.BtnCriarTabelas.setGeometry(QtCore.QRect(0, 19, 131, 41))
        self.BtnCriarTabelas.setObjectName("BtnCriarTabelas")
        self.BtnCriarCampos = QtWidgets.QPushButton(self.centralwidget)
        self.BtnCriarCampos.setGeometry(QtCore.QRect(131, 19, 131, 41))
        self.BtnCriarCampos.setObjectName("BtnCriarCampos")
        self.treeView = QtWidgets.QTreeView(self.centralwidget)
        self.treeView.setGeometry(QtCore.QRect(1, 92, 391, 371))
        self.treeView.setObjectName("treeView")
        self.BtnRefresh = QtWidgets.QPushButton(self.centralwidget)
        self.BtnRefresh.setGeometry(QtCore.QRect(317, 465, 75, 23))
        self.BtnRefresh.setObjectName("BtnRefresh")
        self.BtnSQL = QtWidgets.QPushButton(self.centralwidget)
        self.BtnSQL.setGeometry(QtCore.QRect(262, 19, 131, 41))
        self.BtnSQL.setObjectName("BtnSQL")
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setGeometry(QtCore.QRect(-30, 60, 1131, 16))
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.EdtDatabaseAtual = QtWidgets.QLineEdit(self.centralwidget)
        self.EdtDatabaseAtual.setGeometry(QtCore.QRect(508, 30, 161, 20))
        self.EdtDatabaseAtual.setObjectName("EdtDatabaseAtual")
        self.EdtDatabaseAtual.setEnabled(False)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(412, 30, 91, 20))
        self.label.setObjectName("label")
        ManagementDatabase.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(ManagementDatabase)
        self.statusbar.setObjectName("statusbar")
        ManagementDatabase.setStatusBar(self.statusbar)
        self.actionBackup = QtWidgets.QAction(ManagementDatabase)
        self.actionBackup.setObjectName("actionBackup")
        self.actionCriar_usu_rio = QtWidgets.QAction(ManagementDatabase)
        self.actionCriar_usu_rio.setObjectName("actionCriar_usu_rio")


        self.retranslateUi(ManagementDatabase)
        QtCore.QMetaObject.connectSlotsByName(ManagementDatabase)

        self.BtnRefresh.clicked.connect(self.refresh_treeview)
        self.database_connection = None

        self.model = QtGui.QStandardItemModel()
        self.treeView.setModel(self.model)

        self.BtnCriarTabelas.clicked.connect(self.open_criar_tabela_form)

        self.BtnCriarCampos.clicked.connect(self.open_criar_campos_form)

        self.BtnSQL.clicked.connect(self.open_sql_command_form)


    def retranslateUi(self, ManagementDatabase):
        _translate = QtCore.QCoreApplication.translate
        ManagementDatabase.setWindowTitle(_translate("ManagementDatabase", "EasyTec - Management Database"))
        self.BtnCriarTabelas.setText(_translate("ManagementDatabase", "Criar Tabelas"))
        self.BtnCriarCampos.setText(_translate("ManagementDatabase", "Criar Campos"))
        self.BtnRefresh.setText(_translate("ManagementDatabase", "Refresh"))
        self.BtnSQL.setText(_translate("ManagementDatabase", "SQL Command"))
        self.label.setText(_translate("ManagementDatabase", "<html><head/><body><p><span style=\" font-weight:600;\">Database name</span></p></body></html>"))
        self.actionBackup.setText(_translate("ManagementDatabase", "Backup"))
        self.actionCriar_usu_rio.setText(_translate("ManagementDatabase", "Criar usuário"))

    def connect_to_database(self, db_name):
        try:
            self.database_connection = sqlite3.connect(db_name)
            QtWidgets.QMessageBox.information(None, "Conexão bem-sucedida", f"Conectado ao banco de dados: {db_name}")

            self.refresh_treeview()
        except sqlite3.Error as e:
            QtWidgets.QMessageBox.critical(None, "Erro de Conexão", f"Erro ao conectar ao banco de dados: {e}")

    def closeEvent(self, event):
        if self.database_connection:
            self.database_connection.close()

    def refresh_treeview(self):
        if self.database_connection is None:
            QtWidgets.QMessageBox.warning(None, "Sem conexão", "Você não está conectado a um banco de dados.")
            return

        db_name = self.EdtDatabaseAtual.text()

        try:
            cursor = self.database_connection.cursor()
            cursor.execute("PRAGMA foreign_keys = ON;")
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name != 'sqlite_sequence' AND name != 'EASYTEC_AUTENTICACAO';")
            tables = cursor.fetchall()

            self.clear_treeview()

            for table in tables:
                table_name = table[0]
                table_item = QtGui.QStandardItem(table_name)
                self.model.appendRow(table_item)

                cursor.execute(f"PRAGMA table_info({table_name});")
                fields = cursor.fetchall()

                for field in fields:
                    field_name = field[1]
                    field_item = QtGui.QStandardItem(field_name)
                    table_item.appendRow(field_item)

                cursor.execute(f"PRAGMA foreign_key_list({table_name});")
                foreign_keys = cursor.fetchall()

                if foreign_keys:
                    fk_item = QtGui.QStandardItem("Foreign Keys")
                    table_item.appendRow(fk_item)

                    for fk in foreign_keys:
                        fk_description = f"Column: {fk[3]}, Ref Table: {fk[2]}, Ref Column: {fk[4]}"
                        fk_detail_item = QtGui.QStandardItem(fk_description)
                        fk_item.appendRow(fk_detail_item)

        except sqlite3.Error as e:
            QtWidgets.QMessageBox.critical(None, "Erro ao atualizar", f"Erro ao atualizar treeView: {e}")

    def clear_treeview(self):
        self.model.removeRows(0, self.model.rowCount())

    def open_criar_tabela_form(self):
        global global_db_name
        global_db_name = self.EdtDatabaseAtual.text()
        self.criar_tabela_window = QtWidgets.QMainWindow()
        self.criar_tabela_ui = Ui_CriarTabela()
        self.criar_tabela_ui.setupUi(self.criar_tabela_window)
        self.criar_tabela_window.show()

    def open_criar_campos_form(self):
        global global_db_name
        global_db_name = self.EdtDatabaseAtual.text()
        self.criar_campos_window = QtWidgets.QMainWindow()
        self.criar_campos_ui = Ui_CriarCampos()
        self.criar_campos_ui.setupUi(self.criar_campos_window)
        self.criar_campos_window.show()

    def open_sql_command_form(self):
        global global_db_name
        global_db_name = self.EdtDatabaseAtual.text()
        self.sql_command_window = QtWidgets.QMainWindow()
        self.sql_command_ui = Ui_SQLCommand()
        self.sql_command_ui.setupUi(self.sql_command_window)
        self.sql_command_window.show()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ManagementDatabase = QtWidgets.QMainWindow()
    ui = Ui_ManagementDatabase()
    ui.setupUi(ManagementDatabase)
    ManagementDatabase.show()
    sys.exit(app.exec_())
