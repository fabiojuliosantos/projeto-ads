import sqlite3
from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from reportlab.pdfgen import canvas

subtotal_geral = 0
valor_pago = 0
troco = 0

clientes_pdf = []
produto_pdf = []
valor_produto_pdf = []
quant_pdf = []
num_produtos = 0
sub_produto_pdf = []
sub_pdf = 0

conexao = sqlite3.connect("produtos.db")
cursor = conexao.cursor()


def chama_principal():
    principal.show()


def chama_cadastro():
    principal.close()
    cadastro.show()


def chama_editar():
    principal.close()
    editar.show()


def chama_vendas():
    principal.close()
    vendas.show()


def chama_pagamento():
    global subtotal_geral
    pagamento.show()
    pagamento.lineEdit.setText(str(subtotal_geral))


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
    global clientes_pdf
    nome_cliente = vendas.lineEdit_2.text()
    cliente = "***Devlink Informática*** \n Cliente: "+str(nome_cliente) + \
        "\n------------------------------------------------"
    clientes_pdf.append(nome_cliente)
    vendas.listWidget.addItem(cliente)
    vendas.lineEdit_2.setText('')


def vendas_produtos():
    global subtotal_geral
    global valor_produto_pdf
    global produto_pdf
    global num_produtos
    global quant_pdf
    codigo_produto = vendas.lineEdit.text()
    quantidade = vendas.lineEdit_3.text()
    int_quant = int(quantidade)
    cursor.execute("SELECT * FROM produtos WHERE codigo="+str(codigo_produto))
    produto_saida = cursor.fetchall()
    produto_vendas = produto_saida[0][1]
    quantidade_estoque = int(produto_saida[0][2])
    valor_produto = produto_saida[0][3]

    if int_quant > quantidade_estoque:
        QMessageBox.about(vendas, "Erro", "Quantidade fora de estoque!")
    else:
        subtotal_produto = valor_produto * float(quantidade)
        subtotal_geral = round(subtotal_geral + subtotal_produto, 2)
        sub_produto_pdf.append(str(subtotal_produto))
        produto_pdf.append(str(produto_vendas))
        valor_produto_pdf.append(str(valor_produto))
        quant_pdf.append(str(quantidade))
        sub_produto_pdf.append(str(subtotal_produto))
        venda = "Produto: " + produto_vendas + \
            "\n Quantidade: " + str(quantidade) + \
            "\nValor Unitário: R$"+str(valor_produto).replace(".", ",") + \
            "\n Valor Produtos: R$"+str(subtotal_produto).replace(".", ",") + \
            "\n-------------------------------------------------"
        vendas.listWidget.addItem(venda)
        num_produtos = num_produtos + 1
        vendas.lineEdit.setText('')
        vendas.lineEdit_3.setText('')
        print(num_produtos)
        print(produto_pdf)
        print(subtotal_geral)


def consulta_produtos():
    cursor.execute("SELECT * FROM produtos")
    itens = cursor.fetchall()
    produtos.tableWidget.setRowCount(len(itens))
    produtos.tableWidget.setColumnCount(4)

    for i in range(0, len(itens)):
        for j in range(0, 4):
            produtos.tableWidget.setItem(
                i, j, QtWidgets.QTableWidgetItem(str(itens[i][j])))
    produtos.show()


def finaliza_compra():
    global subtotal_geral
    global valor_pago
    global troco
    flt_sub = float(subtotal_geral)
    valor_pago = float(pagamento.lineEdit_2.text())
    if valor_pago < flt_sub:
        QMessageBox.about(pagamento, "Erro",
                          "Valor abaixo do que deve ser pago!")
    else:
        troco = valor_pago - subtotal_geral
        pagamento.lineEdit_3.setText(str(troco))
        venda_1 = "Valor a ser pago: R$" + str(subtotal_geral) + \
                  "\n Valor Pago: R$" + str(valor_pago) + \
                  "\n Troco: R$" + str(troco)
        vendas.listWidget.addItem(venda_1)


def gerar_pdf():
    cont_pdf = 0
    y = 0
    pdf = canvas.Canvas("Compra.pdf")
    pdf.setFont("Times-Bold", 10)
    pdf.drawString(100, 800, "***DevLink Informática***")
    pdf.drawString(100, 785, "Cliente: "'{}'.format(clientes_pdf[0]))
    pdf.drawString(100, 775, "----------------------------------------")
    for produto in produto_pdf:
        y = y+10
        pdf.drawString(
            100, 770 - y, "Produto: "'{}'.format(produto_pdf[cont_pdf]))
        y = y+10
        pdf.drawString(
            100, 770-y, "Valor do produto R$: "'{}'.format(valor_produto_pdf[cont_pdf]))
        y = y+10
        pdf.drawString(
            100, 770 - y, "Quantidade: "'{}'.format(quant_pdf[cont_pdf]))
        y = y+10
        pdf.drawString(
            100, 770 - y, "Subtotal: R$"'{}'.format(sub_produto_pdf[cont_pdf]))
        y = y+10
        pdf.drawString(100, 770 - y, "---------------------------------------")
        cont_pdf = cont_pdf + 1
        y_total = y
    pdf.drawString(
        100, 755 - y_total, "Total a pagar: R$ " '{}'.format(subtotal_geral))
    pdf.drawString(100, 755 - (y_total + 10),
                   "Valor pago: R$"'{}'.format(valor_pago))
    pdf.drawString(100, 755 - (y_total + 20), "Troco: R$"'{}'.format(troco))
    print(clientes_pdf)
    print(produto_pdf)
    print(valor_produto_pdf)
    pdf.save()
    vendas.listWidget.clear()


clientes_pdf = []
produto_pdf = []
valor_produto_pdf = []
quant_pdf = []
num_produtos = 0
sub_produto_pdf = []
sub_pdf = 0

app = QtWidgets.QApplication([])
cadastro = uic.loadUi('cadastro_produtos.ui')
editar = uic.loadUi('editar_produtos.ui')
editar_menu = uic.loadUi('editar.ui')
principal = uic.loadUi('principal.ui')
vendas = uic.loadUi('vendas.ui')
produtos = uic.loadUi('produtos.ui')
pagamento = uic.loadUi('pagamento.ui')

principal.pushButton.clicked.connect(chama_cadastro)
principal.pushButton_2.clicked.connect(chama_editar)
principal.pushButton_3.clicked.connect(chama_vendas)
editar.pushButton.clicked.connect(mostrar_produtos)
editar.pushButton_2.clicked.connect(editar_produtos)
editar.pushButton_3.clicked.connect(ecluir_produtos)
editar_menu.pushButton_2.clicked.connect(atualiza_produtos)
cadastro.pushButton.clicked.connect(entrada)
vendas.pushButton.clicked.connect(vendas_produtos)
vendas.pushButton_2.clicked.connect(gerar_pdf)
vendas.pushButton_3.clicked.connect(cliente_vendas)
vendas.pushButton_4.clicked.connect(chama_pagamento)
vendas.pushButton_5.clicked.connect(consulta_produtos)
pagamento.pushButton_2.clicked.connect(finaliza_compra)
editar.actionPrincipal.triggered.connect(chama_principal)
editar.actionAdicionar_Itens.triggered.connect(chama_cadastro)
editar.actionVendas.triggered.connect(chama_vendas)
cadastro.actionPrincipal.triggered.connect(chama_principal)
cadastro.actionEditar_Itens.triggered.connect(chama_editar)
cadastro.actionVendas.triggered.connect(chama_vendas)
vendas.actionPrincipal.triggered.connect(chama_principal)
vendas.actionAdicionar_Itens.triggered.connect(chama_cadastro)
vendas.actionEditar_Itens.triggered.connect(chama_editar)
principal.show()
app.exec()
