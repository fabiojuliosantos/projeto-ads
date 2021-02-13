from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QMessageBox

import sqlite3
conexao = sqlite3.connect("produtos.db")
cursor = conexao.cursor()


def chama_cadastro():
    cadastro.show()


def chama_editar():
    editar.show()


def chama_vendas():
    vendas.show()


def mostrar_produtos():
    cursor.execute("SELECT * FROM produtos")
    produtos = cursor.fetchall()
    editar.tableWidget.setRowCount(len(produtos))
    editar.tableWidget.setColumnCount(4)

    for i in range(0, len(produtos)):
        for j in range(0, 4):
            editar.tableWidget.setItem(
                i, j, QtWidgets.QTableWidgetItem(str(produtos[i][j])))


def ecluir_produtos():
    produto_selec = editar.tableWidget.currentRow()
    editar.tableWidget.removeRow(produto_selec)

    cursor.execute("SELECT codigo FROM produtos")
    vetor_produtos = cursor.fetchall()
    codigo_produto = vetor_produtos[produto_selec][0]
    cursor.execute("DELETE FROM produtos WHERE codigo="+str(codigo_produto))


def editar_produtos():

    produto_selec = editar.tableWidget.currentRow()

    cursor.execute("SELECT codigo FROM produtos")
    vetor_produtos = cursor.fetchall()
    codigo_produto = vetor_produtos[produto_selec][0]
    cursor.execute("SELECT * FROM produtos WHERE codigo="+str(codigo_produto))
    produto_editado = cursor.fetchall()
    editar_menu.show()
    editar_menu.lineEdit.setText(str(produto_editado[0][0]))
    editar_menu.lineEdit_2.setText(str(produto_editado[0][1]))
    editar_menu.lineEdit_3.setText(str(produto_editado[0][2]))
    editar_menu.lineEdit_4.setText(str(produto_editado[0][3]))
    print(produto_editado)


def entrada():
    codigo = cadastro.lineEdit.text()
    nome = cadastro.lineEdit_2.text()
    quantidade = cadastro.lineEdit_3.text()
    preco = cadastro.lineEdit_4.text()

    cursor.execute("INSERT INTO produtos(codigo,nome,quantidade,preco) VALUES(?,?,?,?)",
                   (codigo, nome, quantidade, preco))
    conexao.commit()
    codigo = cadastro.lineEdit.setText("")
    nome = cadastro.lineEdit_2.setText("")
    quantidade = cadastro.lineEdit_3.setText("")
    preco = cadastro.lineEdit_4.setText("")

    cursor.execute("SELECT * FROM produtos")
    produtos = cursor.fetchall()

    cadastro.tableWidget.setRowCount(len(produtos))
    cadastro.tableWidget.setColumnCount(4)

    for i in range(0, len(produtos)):
        for j in range(0, 4):
            cadastro.tableWidget.setItem(
                i, j, QtWidgets.QTableWidgetItem(str(produtos[i][j])))


app = QtWidgets.QApplication([])
cadastro = uic.loadUi('cadastro_produtos.ui')
editar = uic.loadUi('editar_produtos.ui')
editar_menu = uic.loadUi('editar.ui')
principal = uic.loadUi('principal.ui')
vendas = uic.loadUi('vendas.ui')

principal.pushButton.clicked.connect(chama_cadastro)
principal.pushButton_2.clicked.connect(chama_editar)
principal.pushButton_3.clicked.connect(chama_vendas)
editar.pushButton.clicked.connect(mostrar_produtos)
editar.pushButton_2.clicked.connect(editar_produtos)
editar.pushButton_3.clicked.connect(ecluir_produtos)
cadastro.pushButton.clicked.connect(entrada)

principal.show()
app.exec()
