import sqlite3
from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from reportlab.pdfgen import canvas

subtotal_geral = 0

conexao = sqlite3.connect("produtos.db")
cursor = conexao.cursor()


def chama_principal():
    principal.show()


def chama_cadastro():
    # principal.close()
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
    conexao.commit()


codigo_editar = 0


def editar_produtos():
    global codigo_editar
    produto_selec = editar.tableWidget.currentRow()

    cursor.execute("SELECT codigo FROM produtos")
    vetor_produtos = cursor.fetchall()
    codigo_produto = vetor_produtos[produto_selec][0]
    codigo_editar = codigo_produto
    cursor.execute("SELECT * FROM produtos WHERE codigo="+str(codigo_produto))
    produto_editado = cursor.fetchall()
    editar_menu.show()
    editar_menu.lineEdit.setText(str(produto_editado[0][0]))
    editar_menu.lineEdit_2.setText(str(produto_editado[0][1]))
    editar_menu.lineEdit_3.setText(str(produto_editado[0][2]))
    editar_menu.lineEdit_4.setText(str(produto_editado[0][3]))


def atualiza_produtos():
    global codigo_editar
    codigo = editar_menu.lineEdit.text()
    nome = editar_menu.lineEdit_2.text()
    quantidade = editar_menu.lineEdit_3.text()
    preco = editar_menu.lineEdit_4.text()
    cursor.execute("UPDATE produtos SET codigo = ?, nome =?, quantidade = ?, preco = ? WHERE codigo="+str(codigo_editar),
                   (codigo, nome, quantidade, preco))
    conexao.commit()
    editar_menu.close()


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


def cliente_vendas():
    nome_cliente = vendas.lineEdit_2.text()
    cliente = "***Devlink Informática*** \n Cliente: "+str(nome_cliente) + \
        "\n------------------------------------------------"
    vendas.listWidget.addItem(cliente)
    vendas.lineEdit_2.setText('')


def vendas_produtos():
    global subtotal_geral
    codigo_produto = vendas.lineEdit.text()
    quantidade = vendas.lineEdit_3.text()
    cursor.execute("SELECT * FROM produtos WHERE codigo="+str(codigo_produto))
    produto_saida = cursor.fetchall()
    produto_vendas = produto_saida[0][1]
    valor_produto = produto_saida[0][3]
    subtotal_produto = valor_produto * float(quantidade)
    subtotal_geral = round(subtotal_geral + subtotal_produto, 2)
    venda = "Produto: " + produto_vendas + \
        "\n Quantidade: " + str(quantidade) + \
        "\nValor Unitário: R$"+str(valor_produto).replace(".", ",") + \
        "\n Valor Produtos: R$"+str(subtotal_produto).replace(".", ",") + \
        "\n-------------------------------------------------"
    vendas.listWidget.addItem(venda)
    vendas.lineEdit.setText('')
    vendas.lineEdit_3.setText('')
    vendas1 = vendas.listWidget
    print(vendas1)


def finaliza_compra():
    global subtotal_geral
    subtotal_compras = str(subtotal_geral).replace(".", ",")
    subtotal = "Valor total: R$" + subtotal_compras
    vendas.listWidget.addItem(subtotal)


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
editar_menu.pushButton_2.clicked.connect(atualiza_produtos)
cadastro.pushButton.clicked.connect(entrada)
vendas.pushButton.clicked.connect(vendas_produtos)
# vendas.pushButton_2.clicked.connect(gerar_pdf)
vendas.pushButton_3.clicked.connect(cliente_vendas)
vendas.pushButton_4.clicked.connect(finaliza_compra)

principal.show()
app.exec()
