from PyQt5 import QtCore, QtGui, QtWidgets
from CriarBasedeDados import Ui_CriarBasedeDados
from ManagementDatase import Ui_ManagementDatabase
from Autenticacao import Ui_Autenticacao
import os

class Ui_Acesso(object):
    def setupUi(self, Acesso):
        Acesso.setObjectName("Acesso")
        Acesso.setFixedSize(373, 304)
        Acesso.setStyleSheet("background-color: rgb(208, 226, 255);")
        self.centralwidget = QtWidgets.QWidget(Acesso)
        self.centralwidget.setObjectName("centralwidget")
        self.EdtDatabaseName = QtWidgets.QComboBox(self.centralwidget)
        self.EdtDatabaseName.setGeometry(QtCore.QRect(86, 107, 201, 22))
        self.EdtDatabaseName.setObjectName("EdtDatabaseName")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(86, 89, 151, 16))
        self.label.setObjectName("label")
        self.BtnAcessar = QtWidgets.QPushButton(self.centralwidget)
        self.BtnAcessar.setGeometry(QtCore.QRect(150, 151, 75, 23))
        self.BtnAcessar.setObjectName("BtnAcessar")
        self.commandLinkButton = QtWidgets.QCommandLinkButton(self.centralwidget)
        self.commandLinkButton.setGeometry(QtCore.QRect(122, 192, 131, 41))
        self.commandLinkButton.setObjectName("commandLinkButton")
        Acesso.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(Acesso)
        self.statusbar.setObjectName("statusbar")
        Acesso.setStatusBar(self.statusbar)

        self.retranslateUi(Acesso)
        QtCore.QMetaObject.connectSlotsByName(Acesso)

        self.commandLinkButton.clicked.connect(self.open_criar_basede_dados)
        self.BtnAcessar.clicked.connect(self.open_autentication)
        self.update_combobox()

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.check_for_new_databases)
        self.timer.start(1000)

        self.last_db_files = []

    def open_criar_basede_dados(self):
        self.criar_basede_dados_window = QtWidgets.QMainWindow()
        self.criar_basede_dados_ui = Ui_CriarBasedeDados()
        self.criar_basede_dados_ui.setupUi(self.criar_basede_dados_window)
        self.criar_basede_dados_window.show()


    def open_autentication(self):
        selected_db = self.EdtDatabaseName.currentText()
        if selected_db:
            self.autentication_window = QtWidgets.QMainWindow()
            self.autentication_ui = Ui_Autenticacao()
            self.autentication_ui.setupUi(self.autentication_window)
            self.autentication_ui.connect_to_database(selected_db)
            self.autentication_window.show()
            Acesso.close()

    def update_combobox(self):
        self.EdtDatabaseName.clear()

        diretorio_atual = os.getcwd()

        arquivos = os.listdir(diretorio_atual)

        arquivos_db = [arquivo for arquivo in arquivos if arquivo.endswith(".db")]

        self.EdtDatabaseName.addItems(arquivos_db)

    def check_for_new_databases(self):
        diretorio_atual = os.getcwd()

        arquivos = os.listdir(diretorio_atual)

        arquivos_db = [arquivo for arquivo in arquivos if arquivo.endswith(".db")]

        if arquivos_db != self.last_db_files:
            self.last_db_files = arquivos_db
            self.update_combobox()

    def retranslateUi(self, Acesso):
        _translate = QtCore.QCoreApplication.translate
        Acesso.setWindowTitle(_translate("Acesso", "EasyTec - Acesso Database"))
        self.label.setText(_translate("Acesso", "<html><head/><body><p><span style=\" font-weight:600;\">Selecione a base de dados</span></p></body></html>"))
        self.BtnAcessar.setText(_translate("Acesso", "Acessar"))
        self.commandLinkButton.setText(_translate("Acesso", "Criar database"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Acesso = QtWidgets.QMainWindow()
    ui = Ui_Acesso()
    ui.setupUi(Acesso)
    Acesso.show()
    sys.exit(app.exec_())
