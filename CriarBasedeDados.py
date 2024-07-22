from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
import sqlite3
import os
import hashlib

class Ui_CriarBasedeDados(object):
    def setupUi(self, CriarBasedeDados):
        CriarBasedeDados.setObjectName("CriarBasedeDados")
        CriarBasedeDados.resize(501, 392)
        CriarBasedeDados.setStyleSheet("background-color: rgb(208, 226, 255);")
        self.centralwidget = QtWidgets.QWidget(CriarBasedeDados)
        self.centralwidget.setObjectName("centralwidget")
        self.EdtNomeDatabase = QtWidgets.QLineEdit(self.centralwidget)
        self.EdtNomeDatabase.setGeometry(QtCore.QRect(134, 151, 241, 20))
        self.EdtNomeDatabase.setObjectName("EdtNomeDatabase")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(164, 19, 171, 31))
        self.label.setObjectName("label")
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(-10, 60, 521, 20))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(134, 133, 41, 16))
        self.label_2.setObjectName("label_2")
        self.BtnCriarBase = QtWidgets.QPushButton(self.centralwidget)
        self.BtnCriarBase.setGeometry(QtCore.QRect(300, 178, 75, 23))
        self.BtnCriarBase.setObjectName("BtnCriarBase")
        CriarBasedeDados.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(CriarBasedeDados)
        self.statusbar.setObjectName("statusbar")
        CriarBasedeDados.setStatusBar(self.statusbar)

        self.retranslateUi(CriarBasedeDados)
        QtCore.QMetaObject.connectSlotsByName(CriarBasedeDados)

        self.BtnCriarBase.clicked.connect(self.criar_base_sqlite)

    def criar_base_sqlite(self):
        nome_database = self.EdtNomeDatabase.text().strip()

        if not nome_database:
            QMessageBox.critical(None, "Erro", "Por favor, insira um nome para a base de dados.")
            return

        caminho_database = os.path.join(os.getcwd(), nome_database + ".db")

        try:
            conexao = sqlite3.connect(caminho_database)
            cursor = conexao.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS EASYTEC_AUTENTICACAO (
                    EA_NOME TEXT NOT NULL,
                    EA_SENHA TEXT NOT NULL
                )
            """)

            nome_usuario = "easy"
            senha_usuario = "tec"
            senha_criptografada = hashlib.sha256(senha_usuario.encode()).hexdigest()

            cursor.execute("""
                INSERT INTO EASYTEC_AUTENTICACAO (EA_NOME, EA_SENHA)
                VALUES (?, ?)
            """, (nome_usuario, senha_criptografada))

            conexao.commit()
            conexao.close()

            QMessageBox.information(None, "Sucesso", f"Base de dados '{nome_database}' criada com sucesso.")

        except Exception as e:
            QMessageBox.critical(None, "Erro", f"Erro ao criar base de dados: {str(e)}")

    def retranslateUi(self, CriarBasedeDados):
        _translate = QtCore.QCoreApplication.translate
        CriarBasedeDados.setWindowTitle(_translate("CriarBasedeDados", "EasyTec - Criar Base de dados"))
        self.label.setText(_translate("CriarBasedeDados",
                                      "<html><head/><body><p><span style=\" font-size:12pt; font-weight:600;\">Criar Base de dados</span></p></body></html>"))
        self.label_2.setText(_translate("CriarBasedeDados",
                                        "<html><head/><body><p><span style=\" font-weight:600;\">Nome</span></p></body></html>"))
        self.BtnCriarBase.setText(_translate("CriarBasedeDados", "Criar Base"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    CriarBasedeDados = QtWidgets.QMainWindow()
    ui = Ui_CriarBasedeDados()
    ui.setupUi(CriarBasedeDados)
    CriarBasedeDados.show()
    sys.exit(app.exec_())
