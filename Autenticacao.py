from PyQt5 import QtCore, QtGui, QtWidgets
import sqlite3
import hashlib
from ManagementDatase import Ui_ManagementDatabase

glob_database = None

class Ui_Autenticacao(object):
    def setupUi(self, Autenticacao):
        Autenticacao.setObjectName("Autenticacao")
        Autenticacao.setFixedSize(377, 305)
        Autenticacao.setStyleSheet("background-color: rgb(208, 226, 255);")
        self.centralwidget = QtWidgets.QWidget(Autenticacao)
        self.centralwidget.setObjectName("centralwidget")
        self.EdtUsuario = QtWidgets.QLineEdit(self.centralwidget)
        self.EdtUsuario.setGeometry(QtCore.QRect(94, 96, 191, 20))
        self.EdtUsuario.setObjectName("EdtUsuario")
        self.EdtSenha = QtWidgets.QLineEdit(self.centralwidget)
        self.EdtSenha.setGeometry(QtCore.QRect(94, 142, 191, 20))
        self.EdtSenha.setObjectName("EdtSenha")
        self.EdtSenha.setEchoMode(QtWidgets.QLineEdit.Password)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(94, 80, 47, 13))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(94, 127, 47, 13))
        self.label_2.setObjectName("label_2")
        self.BtnConectar = QtWidgets.QPushButton(self.centralwidget)
        self.BtnConectar.setGeometry(QtCore.QRect(210, 169, 75, 23))
        self.BtnConectar.setObjectName("BtnConectar")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(126, 10, 131, 31))
        self.label_3.setObjectName("label_3")
        Autenticacao.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(Autenticacao)
        self.statusbar.setObjectName("statusbar")
        Autenticacao.setStatusBar(self.statusbar)

        self.retranslateUi(Autenticacao)
        QtCore.QMetaObject.connectSlotsByName(Autenticacao)

        self.BtnConectar.clicked.connect(self.authenticate_user)

    def connect_to_database(self, db_name):
        global glob_database
        try:
            self.database_connection = sqlite3.connect(db_name)
            glob_database = db_name
        except sqlite3.Error as e:
            QtWidgets.QMessageBox.critical(None, "Erro de Conexão", f"Erro ao conectar ao banco de dados: {e}")

    def open_management_database(self):
        global glob_database
        selected_db = glob_database
        if selected_db:
            self.management_database_window = QtWidgets.QMainWindow()
            self.management_database_ui = Ui_ManagementDatabase()
            self.management_database_ui.setupUi(self.management_database_window)
            self.management_database_ui.EdtDatabaseAtual.setText(selected_db)
            self.management_database_ui.connect_to_database(selected_db)
            self.management_database_window.show()
            QtWidgets.QApplication.instance().activeWindow().close()

    def authenticate_user(self):
        username = self.EdtUsuario.text()
        password = self.EdtSenha.text()
        self.validate_user(username, password)

    def validate_user(self, username, password):
        global glob_database
        if glob_database:
            try:
                cursor = self.database_connection.cursor()
                cursor.execute("SELECT EA_SENHA FROM EASYTEC_AUTENTICACAO WHERE EA_NOME = ?", (username,))
                result = cursor.fetchone()
                if result:
                    stored_password = result[0]
                    hashed_password = hashlib.sha256(password.encode()).hexdigest()
                    if stored_password == hashed_password:
                        self.open_management_database()
                        return True
            except sqlite3.Error as e:
                QtWidgets.QMessageBox.critical(None, "Erro de Consulta", f"Erro ao consultar o banco de dados: {e}")
        QtWidgets.QMessageBox.warning(None, "Autenticação Falhou", "Usuário ou senha incorretos.")
        return False

    def retranslateUi(self, Autenticacao):
        _translate = QtCore.QCoreApplication.translate
        Autenticacao.setWindowTitle(_translate("Autenticacao", "EasyTec - Autenticação"))
        self.label.setText(_translate("Autenticacao", "<html><head/><body><p><span style=\" font-weight:600;\">Usuário</span></p></body></html>"))
        self.label_2.setText(_translate("Autenticacao", "<html><head/><body><p><span style=\" font-weight:600;\">Senha</span></p></body></html>"))
        self.BtnConectar.setText(_translate("Autenticacao", "Conectar"))
        self.label_3.setText(_translate("Autenticacao", "<html><head/><body><p><span style=\" font-size:14pt; font-weight:600;\">Autenticação</span></p></body></html>"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Autenticacao = QtWidgets.QMainWindow()
    ui = Ui_Autenticacao()
    ui.setupUi(Autenticacao)
    ui.connect_to_database('caminho_para_seu_banco_de_dados.db')  # Ajuste o caminho para seu banco de dados
    Autenticacao.show()
    sys.exit(app.exec_())
