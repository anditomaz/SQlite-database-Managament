from PyQt5 import QtCore, QtGui, QtWidgets
import sqlite3
import ManagementDatase

class Ui_CriarCampos(object):
    def setupUi(self, CriarCampos):
        CriarCampos.setObjectName("CriarCampos")
        CriarCampos.setFixedSize(526, 444)
        CriarCampos.setStyleSheet("background-color: rgb(208, 226, 255);")
        self.centralwidget = QtWidgets.QWidget(CriarCampos)
        self.centralwidget.setObjectName("centralwidget")
        self.EdtTabela = QtWidgets.QComboBox(self.centralwidget)
        self.EdtTabela.setGeometry(QtCore.QRect(175, 70, 180, 22))
        self.EdtTabela.setObjectName("EdtTabela")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(175, 52, 111, 16))
        self.label.setObjectName("label")
        self.EdtCampo = QtWidgets.QLineEdit(self.centralwidget)
        self.EdtCampo.setGeometry(QtCore.QRect(175, 118, 180, 20))
        self.EdtCampo.setObjectName("EdtCampo")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(176, 101, 101, 16))
        self.label_2.setObjectName("label_2")
        self.radioButton = QtWidgets.QRadioButton(self.centralwidget)
        self.radioButton.setGeometry(QtCore.QRect(193, 214, 141, 17))
        self.radioButton.setObjectName("radioButton")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(174, 250, 121, 16))
        self.label_3.setObjectName("label_3")
        self.EdtTabelaFK = QtWidgets.QComboBox(self.centralwidget)
        self.EdtTabelaFK.setGeometry(QtCore.QRect(175, 268, 181, 22))
        self.EdtTabelaFK.setObjectName("EdtTabelaFK")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(175, 300, 121, 16))
        self.label_4.setObjectName("label_4")
        self.EdtCampoFK = QtWidgets.QComboBox(self.centralwidget)
        self.EdtCampoFK.setGeometry(QtCore.QRect(176, 318, 181, 22))
        self.EdtCampoFK.setObjectName("EdtCampoFK")
        self.BtnCriarCampo = QtWidgets.QPushButton(self.centralwidget)
        self.BtnCriarCampo.setGeometry(QtCore.QRect(228, 364, 75, 23))
        self.BtnCriarCampo.setObjectName("BtnCriarCampo")
        self.EdtTipoCampo = QtWidgets.QComboBox(self.centralwidget)
        self.EdtTipoCampo.setGeometry(QtCore.QRect(175, 163, 181, 22))
        self.EdtTipoCampo.setObjectName("EdtTipoCampo")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(175, 146, 31, 16))
        self.label_5.setObjectName("label_5")
        CriarCampos.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(CriarCampos)
        self.statusbar.setObjectName("statusbar")
        CriarCampos.setStatusBar(self.statusbar)

        self.retranslateUi(CriarCampos)
        QtCore.QMetaObject.connectSlotsByName(CriarCampos)

        self.radioButton.toggled.connect(self.toggle_fk_fields)
        self.EdtTabelaFK.currentIndexChanged.connect(self.update_fields_fk)

        self.EdtTabelaFK.setEnabled(False)
        self.EdtCampoFK.setEnabled(False)

        self.database_connection = None
        self.connect_to_database()

        self.BtnCriarCampo.clicked.connect(self.criar_campo)

        self.EdtTipoCampo.addItems(["INTEGER", "REAL", "TEXT", "BLOB", "NUMERIC", "FLOAT", "DOUBLE", "DECIMAL", "BOOLEAN", "DATE", "DATETIME"])

    def retranslateUi(self, CriarCampos):
        _translate = QtCore.QCoreApplication.translate
        CriarCampos.setWindowTitle(_translate("CriarCampos", "EasyTec - Criar Campos"))
        self.label.setText(_translate("CriarCampos", "<html><head/><body><p><span style=\" font-weight:600;\">Selecione a tabela</span></p></body></html>"))
        self.label_2.setText(_translate("CriarCampos", "<html><head/><body><p><span style=\" font-weight:600;\">Nome do campo</span></p></body></html>"))
        self.radioButton.setText(_translate("CriarCampos", "Adicionar FOREIGN KEY"))
        self.label_3.setText(_translate("CriarCampos", "<html><head/><body><p><span style=\" font-weight:600;\">Tabela de referência</span></p></body></html>"))
        self.label_4.setText(_translate("CriarCampos", "<html><head/><body><p><span style=\" font-weight:600;\">Campo de referência</span></p></body></html>"))
        self.BtnCriarCampo.setText(_translate("CriarCampos", "Criar campo"))
        self.label_5.setText(_translate("CriarCampos", "<html><head/><body><p><span style=\" font-weight:600;\">Tipo</span></p></body></html>"))

    def toggle_fk_fields(self, checked):
        self.EdtTabelaFK.setEnabled(checked)
        self.EdtCampoFK.setEnabled(checked)

    def connect_to_database(self):
        db_name = ManagementDatase.global_db_name
        try:
            self.database_connection = sqlite3.connect(db_name)
            cursor = self.database_connection.cursor()
            cursor.execute("PRAGMA foreign_keys = ON;")
            self.populate_tables_fk()
        except sqlite3.Error as e:
            QtWidgets.QMessageBox.critical(None, "Erro de Conexão", f"Erro ao conectar ao banco de dados: {e}")

    def populate_tables_fk(self):
        if self.database_connection:
            try:
                cursor = self.database_connection.cursor()
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name != 'sqlite_sequence'AND name != 'EASYTEC_AUTENTICACAO';")
                tables = cursor.fetchall()
                self.EdtTabela.clear()
                self.EdtTabelaFK.clear()
                for table in tables:
                    self.EdtTabela.addItem(table[0])
                    self.EdtTabelaFK.addItem(table[0])
            except sqlite3.Error as e:
                QtWidgets.QMessageBox.critical(None, "Erro ao carregar tabelas", f"Erro ao carregar tabelas: {e}")

    def update_fields_fk(self):
        selected_table = self.EdtTabelaFK.currentText()
        if self.database_connection and selected_table:
            try:
                cursor = self.database_connection.cursor()
                cursor.execute(f"PRAGMA table_info({selected_table});")
                fields = cursor.fetchall()
                self.EdtCampoFK.clear()
                for field in fields:
                    self.EdtCampoFK.addItem(field[1])
            except sqlite3.Error as e:
                QtWidgets.QMessageBox.critical(None, "Erro ao carregar campos", f"Erro ao carregar campos: {e}")

    def criar_campo(self):
        nome_campo = self.EdtCampo.text()
        tabela_selecionada = self.EdtTabela.currentText()
        tipo_campo = self.EdtTipoCampo.currentText()

        try:
            cursor = self.database_connection.cursor()
            self.database_connection.execute("BEGIN TRANSACTION;")

            if self.radioButton.isChecked():
                tabela_fk = self.EdtTabelaFK.currentText()
                campo_fk = self.EdtCampoFK.currentText()

                cursor.execute(f"PRAGMA table_info({tabela_selecionada});")
                fields = cursor.fetchall()

                fields_def = ", ".join([f"{field[1]} {field[2]}" for field in fields])
                new_table_def = f"CREATE TABLE {tabela_selecionada}_new ({fields_def}, {nome_campo} {tipo_campo}, FOREIGN KEY({nome_campo}) REFERENCES {tabela_fk}({campo_fk}))"
                cursor.execute(new_table_def)

                fields_names = ", ".join([field[1] for field in fields])
                cursor.execute(
                    f"INSERT INTO {tabela_selecionada}_new ({fields_names}) SELECT {fields_names} FROM {tabela_selecionada}")

                cursor.execute(f"DROP TABLE {tabela_selecionada}")

                cursor.execute(f"ALTER TABLE {tabela_selecionada}_new RENAME TO {tabela_selecionada}")

            else:
                cursor.execute(f"ALTER TABLE {tabela_selecionada} ADD COLUMN {nome_campo} {tipo_campo}")

            self.database_connection.commit()
            QtWidgets.QMessageBox.information(None, "Campo Criado", "Campo criado com sucesso!")

        except sqlite3.Error as e:
            self.database_connection.rollback()
            QtWidgets.QMessageBox.critical(None, "Erro ao criar campo", f"Erro ao criar campo: {e}")



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    CriarCampos = QtWidgets.QMainWindow()
    ui = Ui_CriarCampos()
    ui.setupUi(CriarCampos)
    CriarCampos.show()
    sys.exit(app.exec_())
