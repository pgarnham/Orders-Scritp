# Script principal para generar pedidos en formato pdf

import os
import time

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter


pedidos = []
contador = 0
with open("plantilla.csv", encoding='utf-8') as file:
    for linea in file:
        if contador == 0:
            header = linea.split(";")
            ultimo = header[-1]
            largo = len(ultimo)
            ultimo_bien = ultimo[:largo - 1]
            header[-1] = ultimo_bien
            contador += 1
        else:
            pedido = linea.split(";")
            lista_pedido = []
            for dato in pedido:
                if (dato != "\n"):
                    lista_pedido.append(dato)
                    pedidos.append(lista_pedido)

pedidos_en_tuplas = []
for lista in pedidos:
    tuplas_pedidos = list(zip(header, lista))
    pedidos_en_tuplas.append(tuplas_pedidos)


lista_definitiva = []

for pedido in pedidos_en_tuplas:
    pedido_final = []
    for tupla in pedido:
        if tupla[1] != "":
            pedido_final.append(tupla)
    lista_definitiva.append(pedido_final)


horario_ = time.strftime("%H %M %S")  # Formato de 24 horas
fecha = time.strftime("%d-%m-%y")
nombre_carpeta = f"Pedidos {fecha} {horario_}"
os.mkdir("pedidos_pdf/" + nombre_carpeta)


for pedido_ in lista_definitiva:
    carp_1 = "pedidos_pdf/"
    ruta = carp_1 + nombre_carpeta
    direccion = ruta + "/pedido_" + pedido_[1][1] + ".pdf"
    c = canvas.Canvas(direccion, pagesize=letter)
    c.setLineWidth(.3)
    c.setFont('Helvetica-Bold', 12)

    linea = 750  # Donde comienza la primera linea
    horiz_izq = 40  # Donde se ubica la lista de productos a la izq.
    horiz_der = 450  # Donde se ubica la lista de cantidades a la der.
    aux = 1
    aux_2 = 0
    linea_sig = 15  # Decremento normal para siguiente linea.

    for tupla in pedido_:
        if aux <= 5:
            c.drawString(horiz_izq, linea, f"{tupla[0]}:  {tupla[1]}")

            aux += 1
            if aux == 6:
                c.line(horiz_izq, linea - 2, 500, linea - 2)
                linea -= (linea_sig + 5)
            else:
                linea -= linea_sig
        else:
            if aux_2 == 0:
                c.setFont('Helvetica', 12)
                aux_2 += 1
            c.drawString(horiz_izq, linea, f"{tupla[0]}")
            c.drawString(horiz_der, linea, f"{tupla[1]}")
            c.rect(520, linea - 2, 70, 15)
            linea -= 20
    c.drawString(horiz_izq, linea, "Envío a Domicilio")
    c.drawString(horiz_der, linea, "1 envío")
    c.drawString(530, linea, "$ 1.500")
    c.rect(520, linea - 2, 70, 15)
    c.line(horiz_izq, linea - 7, 590, linea - 7)
    linea -= 30
    c.setFont('Helvetica-Bold', 17)
    c.drawString(70, linea, "TOTAL")
    c.rect(horiz_der, linea - 10, 150, 25)
    c.save()
