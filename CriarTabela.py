from PyQt5 import QtCore, QtGui, QtWidgets
import sqlite3
import ManagementDatase

class Ui_CriarTabela(object):
    def setupUi(self, CriarTabela):
        CriarTabela.setObjectName("CriarTabela")
        CriarTabela.setFixedSize(373, 310)
        CriarTabela.setStyleSheet("background-color: rgb(208, 226, 255);")
        self.centralwidget = QtWidgets.QWidget(CriarTabela)
        self.centralwidget.setObjectName("centralwidget")
        self.EdtNomeTabela = QtWidgets.QLineEdit(self.centralwidget)
        self.EdtNomeTabela.setGeometry(QtCore.QRect(90, 137, 201, 20))
        self.EdtNomeTabela.setObjectName("EdtNomeTabela")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(90, 118, 91, 16))
        self.label.setObjectName("label")
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(-10, 50, 411, 16))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(130, 16, 121, 21))
        self.label_2.setObjectName("label_2")
        self.BtnCriar = QtWidgets.QPushButton(self.centralwidget)
        self.BtnCriar.setGeometry(QtCore.QRect(216, 163, 75, 23))
        self.BtnCriar.setObjectName("BtnCriar")
        CriarTabela.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(CriarTabela)
        self.statusbar.setObjectName("statusbar")
        CriarTabela.setStatusBar(self.statusbar)

        self.retranslateUi(CriarTabela)
        QtCore.QMetaObject.connectSlotsByName(CriarTabela)

        self.BtnCriar.clicked.connect(self.criar_tabela)

    def retranslateUi(self, CriarTabela):
        _translate = QtCore.QCoreApplication.translate
        CriarTabela.setWindowTitle(_translate("CriarTabela", "EasyTec - Criar Tabela"))
        self.label.setText(_translate("CriarTabela", "<html><head/><body><p><span style=\" font-weight:600;\">Nome da tabela</span></p></body></html>"))
        self.label_2.setText(_translate("CriarTabela", "<html><head/><body><p><span style=\" font-size:14pt; font-weight:600;\">Criar Tabela</span></p></body></html>"))
        self.BtnCriar.setText(_translate("CriarTabela", "Criar"))

    def criar_tabela(self):
        nome_tabela = self.EdtNomeTabela.text()

        basededados = ManagementDatase.global_db_name

        try:
            conn = sqlite3.connect(basededados)
            cursor = conn.cursor()
            cursor.execute("PRAGMA foreign_keys = ON;")

            cursor.execute(f"CREATE TABLE IF NOT EXISTS {nome_tabela} (ID INTEGER PRIMARY KEY AUTOINCREMENT)")
            conn.commit()
            conn.close()

            QtWidgets.QMessageBox.information(None, "Tabela Criada", f"Tabela '{nome_tabela}' criada com sucesso!")
        except sqlite3.Error as e:
            QtWidgets.QMessageBox.critical(None, "Erro ao criar tabela", f"Erro ao criar tabela: {e}")

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    CriarTabela = QtWidgets.QMainWindow()
    ui = Ui_CriarTabela()
    ui.setupUi(CriarTabela)
    CriarTabela.show()
    sys.exit(app.exec_())
