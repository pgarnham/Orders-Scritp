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




horario_ = time.strftime("%H %M %S") #Formato de 24 horas
fecha = time.strftime("%d-%m-%y")
nombre_carpeta = f"Pedidos {fecha} {horario_}"
os.mkdir("pedidos_pdf/" + nombre_carpeta)




for pedido_ in lista_definitiva:
	direccion ="pedidos_pdf/" + nombre_carpeta + "/pedido_" + pedido_[1][1] + ".pdf"
	c = canvas.Canvas(direccion, pagesize=letter)
	c.setLineWidth(.3)
	c.setFont('Helvetica-Bold', 12)

	linea = 750
	aux = 1
	aux_2 = 0

	for tupla in pedido_:
		if aux <= 5:
			c.drawString(40, linea, f"{tupla[0]}:  {tupla[1]}")
			
			aux += 1
			if aux == 6:
				c.line(40,linea - 2,500,linea - 2)
				linea -= 20
			else:
				linea -= 15
		else:
			if aux_2 == 0:
				c.setFont('Helvetica', 12)
				aux_2 += 1
			c.drawString(40, linea, f"{tupla[0]}")
			c.drawString(450, linea, f"{tupla[1]}")
			c.rect(520, linea - 2, 70, 15)
			linea -= 20
	c.drawString(40, linea, "Envío a Domicilio")
	c.drawString(450, linea, "1 envío")
	c.drawString(530, linea, "$ 1.500")
	c.rect(520, linea - 2, 70, 15)
	c.line(40,linea - 7,590,linea - 7)
	linea -= 30
	c.setFont('Helvetica-Bold', 17)	
	c.drawString(70, linea, "TOTAL")
	c.rect(450, linea - 10, 150, 25)
	c.save()

