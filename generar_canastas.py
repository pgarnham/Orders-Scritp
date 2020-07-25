# Script para generar lista de compras en formato pdf

import os
import time
from datetime import date
from copy import copy, deepcopy
import tkinter.filedialog
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
import pandas as pd
from tkinter import getint
from decimal import Decimal

import tkinter as tk
from tkinter.simpledialog import askstring, askinteger
from tkinter.messagebox import showerror

from productos import frutas_prod, verduras_prod


def to_integer(number):
    """Convierte a entero si se puede."""
    if number % 1 == 0:
        return int(number)
    else:
        return number


def cut_name(name):
    """Recorta partes innecesarias del nombre
        del producto."""
    precio = False
    admitidos = set([str(i) for i in range(0, 10)])
    admitidos |= set([".", ",", "$", " "])
    nombre_final = ""
    for letra in name:
        if letra == "$":
            precio = True
        if not precio:
            nombre_final += letra
        elif precio and (letra in admitidos):
            nombre_final += letra
    return nombre_final
        


def clean_safe(cantidad):
    """Limpia datos de entrada."""
    numero = list()
    divisor = list()
    hay_divisor = False
    cifras = set([str(i) for i in range(0, 10)])
    dots = set([",", "."])
    for caracter in cantidad:
        if not hay_divisor:
            # print("not")
            if caracter in cifras:
                numero.append(caracter)
            elif caracter in dots:
                numero.append(".")
            elif caracter == "/":
                hay_divisor = True
        else:
            if caracter in cifras:
                divisor.append(caracter)
            elif caracter in dots:
                pass

    numero_final = ""
    num_divisor = ""
    for elems in numero:
        numero_final += elems
    if hay_divisor:
        for elems in divisor:
            num_divisor += elems
        numero_final = Decimal(numero_final)
        num_divisor = Decimal(num_divisor)
        return numero_final / num_divisor
    # print(f"el numero final es: {numero_final}")
    return Decimal(numero_final)


def display_2(lista, ventana, l_agregados, l_eliminados):
    inicio = entry_1.get()
    fin = entry_2.get()
    agregados = entry_3.get()
    eliminados = entry_4.get()
    agregados = agregados.split(",")
    eliminados = eliminados.split(",")
    print(agregados)
    print(eliminados)
    if agregados != [""]:
        for ag in agregados:
            l_agregados.append(int(ag))
    if eliminados != [""]:
        for el in eliminados:
            l_eliminados.append(int(el))

    try:
       inicio = int(inicio)
       fin = int(fin)
    # ValueError is the type of error expected from this conversion
    except ValueError:
        #Display Error Window (Title, Prompt)
        showerror('Non-Int Error', 'Please enter an integer')
    else:
        lista.append(inicio)
        lista.append(fin)
        ventana.destroy()


# Create the main window
root = tk.Tk()
root.title("Seleccionar Pedidos")

# Create the widgets
entry_1 = tk.Entry(root)
# btn_1 = tk.Button(root, text = "Display Text", command = display_2)

entry_2 = tk.Entry(root)
entry_3 = tk.Entry(root)
entry_4 = tk.Entry(root)
label_1 = tk.Label(root, text="Desde:")
label_2 = tk.Label(root, text="Hasta:")
label_3 = tk.Label(root, text="Considerar extras:")
label_4 = tk.Label(root, text="No considerar:")
separador = tk.Label(root, text="               ")
separador_2 = tk.Label(root, text="               ")
inputs = []
agregar = []
eliminar = []
btn_2 = tk.Button(root, text = "Continuar",
                  command = lambda: display_2(inputs, root, agregar, eliminar))


# Grid is used to add the widgets to root
# Alternatives are Pack and Place
separador_2.grid(row=0, padx=10, pady=10)
label_1.grid(row=1, column=0, padx=10)
label_2.grid(row=1, column=1, padx=10)
entry_1.grid(row = 2, column = 0, padx=10)
entry_2.grid(row = 2, column = 1, padx=10)
separador.grid(row=3, padx=10, pady=10)
label_3.grid(row=4, column=0, sticky="E")
entry_3.grid(row = 4, column=1, pady=10)
label_4.grid(row=5, column=0, sticky="E")
entry_4.grid(row = 5, column=1, pady=10)
btn_2.grid(row = 6, column = 1, padx=10, pady=10)

root.mainloop()


excel_path = tkinter.filedialog.askopenfilename()
read_file = pd.read_excel(rf"{excel_path}", sheet_name=0)
read_file.to_csv(r't.csv', index=None, header=True, encoding='utf8', sep=";")


pedidos = []
contador = 0
with open("t.csv", "r", encoding="utf-8") as file:
    for linea in file:
        if contador == 0:
            header = linea.split(";")
            productos = dict()
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

lista_productos = copy(header)
lista_productos = lista_productos[6:]
# print(lista_productos)
diccionario_productos = dict((producto, 0) for producto in lista_productos)
lista_definitiva = []

# print(len(pedidos_en_tuplas))
contador = 1
for pedido in pedidos_en_tuplas:
    pedido_final = []
    for tupla in pedido:
        if (tupla[1] != "") and (tupla[0] != "nro_pedido"):
            pedido_final.append(tupla)
    lista_definitiva.append((contador, pedido_final))
    contador += 1


agregados_s = set(agregar)
eliminados_s = set(eliminar)
set_rango = set([i for i in range(inputs[0], inputs[1] + 1)])
deben_estar = (set_rango | agregados_s) - eliminados_s
lista_definitiva = [pedido for indice, pedido in lista_definitiva if indice in deben_estar]

# lista_definitiva = lista_definitiva[inputs[0] - 1:inputs[1]]
# print(len(lista_definitiva))
dicc_frutas = dict((fruta, dict()) for fruta in frutas_prod)
dicc_verduras = dict((verdura, dict()) for verdura in verduras_prod)

for pedido in lista_definitiva:
    for item in pedido:
        if item[0] in dicc_frutas:
            if item[1] in dicc_frutas[item[0]]:
                dicc_frutas[item[0]][item[1]] += 1
            else:
                dicc_frutas[item[0]][item[1]] = 1
        if item[0] in dicc_verduras:
            if item[1] in dicc_verduras[item[0]]:
                dicc_verduras[item[0]][item[1]] += 1
            else:
                dicc_verduras[item[0]][item[1]] = 1


horario_ = str(time.strftime("%H %M %S"))  # Formato de 24 horas
fecha = time.strftime("%d-%m-%y")
today = date.today()
week_number = today.isocalendar()[1]
if not os.path.exists("Produccion"):
    os.mkdir("Produccion")

nombre_carpeta = f"Produccion Semana {week_number}"
ruta = f"Produccion" + "/" + nombre_carpeta
# ruta = os.join("Compras", nombre_carpeta)
if not os.path.exists(ruta):
    os.mkdir(ruta)

nombre_archivo = f"Produccion Semana {week_number}    (pedidos del {inputs[0]} al {inputs[1]})"
ruta_final = ruta + "/" + nombre_archivo

encabezado = []
hora_fecha = f"Documento de produccion generado el {fecha} a las {horario_}"
encabezado.append(nombre_archivo)
encabezado.append(hora_fecha)
sacados = f"Los pedidos no considerados son: "
con = 0

if eliminar == []:
    encabezado.append(" ")
if eliminar != []:
    for num in eliminar:
        if con != 0:
            sacados += " - "
        sacados += str(num)
        con += 1
    encabezado.append(sacados)
agregado = f"Los pedidos agregados son: "
con = 0
if agregar == []:
    encabezado.append(" ")
if agregar != []:
    for num in agregar:
        if con != 0:
            agregado += " - "
        agregado += str(num)
        con += 1
    encabezado.append(agregado) 


f_dict_verduras = deepcopy(dicc_verduras)
f_dict_frutas = deepcopy(dicc_frutas)

for key, value in dicc_frutas.items():
    lista = [(peso, veces) for peso, veces in value.items()]
    lista.sort(key=lambda x: x[0], reverse=False)
    f_dict_frutas[key] = copy(lista)
    if lista == []:
        del f_dict_frutas[key]
    
for key, value in dicc_verduras.items():
    lista = [(peso, veces) for peso, veces in value.items()]
    lista.sort(key=lambda x: x[0], reverse=False)
    f_dict_verduras[key] = copy(lista)
    if lista == []:
        del f_dict_verduras[key]
    

for key, value in f_dict_frutas.items():
    print(f"{key}  ----->   {f_dict_frutas[key]}")
for key, value in f_dict_verduras.items():
    print(f"{key}  ----->   {f_dict_verduras[key]}")


c = canvas.Canvas(ruta_final, pagesize=A4)
c.setLineWidth(.3)
c.setFont('Helvetica-Bold', 16)
linea = 785  # Donde comienza la primera linea
horiz_izq = 40  # Donde se ubica la lista de productos a la izq.
horiz_der = 450  # Donde se ubica la lista de cantidades a la der.
aux = 1
aux_2 = 0
linea_sig = 15  # Decremento normal para siguiente linea.
contador = 0
for elemento in encabezado:
    c.drawString(horiz_izq, linea, elemento)
    c.setFont('Helvetica-Bold', 12)
    aux += 1
    if aux == 5:
        c.line(horiz_izq, linea - 2, 500, linea - 2)
        linea -= (linea_sig + 5)
    else:
        linea -= linea_sig

c.setFont('Helvetica', 12)
for fruta, cantidades in f_dict_frutas.items():
    if contador + len(cantidades) >= 34:
        contador = -3
        c.showPage()
        linea = 785  # Donde comienza la primera linea
        horiz_izq = 40  # Donde se ubica la lista de productos a la izq.
        horiz_der = 450  # Donde se ubica la lista de cantidades a la der.
        linea_sig = 15  # Decremento normal para siguiente linea.
    c.rect(horiz_izq - 3, linea - 4, horiz_der - horiz_izq + 15, 20)
    c.drawString(horiz_izq, linea, f"{cut_name(fruta)}")
    contador += 1
    linea -= linea_sig
    for cantidad in cantidades:
        c.drawString(horiz_izq + 15, linea, f"{cantidad[0]} ------->")
        c.drawString(horiz_izq + 55, linea, f"{cantidad[1]}")
        contador += 1
        linea -= linea_sig
    linea -= 5

contador = -3
c.showPage()
linea = 785  # Donde comienza la primera linea
horiz_izq = 40  # Donde se ubica la lista de productos a la izq.
horiz_der = 450  # Donde se ubica la lista de cantidades a la der.
linea_sig = 15  # Decremento normal para siguiente linea.

for verdura, cantidades in f_dict_verduras.items():
    if contador + len(cantidades) >= 34:
        contador = -3
        c.showPage()
        linea = 785  # Donde comienza la primera linea
        horiz_izq = 40  # Donde se ubica la lista de productos a la izq.
        horiz_der = 450  # Donde se ubica la lista de cantidades a la der.
        linea_sig = 15  # Decremento normal para siguiente linea.
    c.rect(horiz_izq - 3, linea - 4, horiz_der - horiz_izq + 15, 20)
    c.drawString(horiz_izq, linea, f"{cut_name(verdura)}")
    contador += 1
    linea -= 20
    for cantidad in cantidades:
        c.drawString(horiz_izq + 15, linea, f"{cantidad[0]} ------->")
        c.drawString(horiz_izq + 55, linea, f"{cantidad[1]}")
        contador += 1
        linea -= 20
c.save()











c = canvas.Canvas(ruta_final, pagesize=A4)
c.setLineWidth(.3)
c.setFont('Helvetica-Bold', 16)
linea = 785  # Donde comienza la primera linea
horiz_izq = 40  # Donde se ubica la lista de productos a la izq.
horiz_der = 450  # Donde se ubica la lista de cantidades a la der.
aux = 1
aux_2 = 0
linea_sig = 15  # Decremento normal para siguiente linea.
contador = 0
for elemento in encabezado:
    if aux <= 4:
        c.drawString(horiz_izq, linea, encabezado[aux - 1])
        c.setFont('Helvetica-Bold', 12)
        aux += 1
        if aux == 5:
            # c.line(horiz_izq, linea - 2, 500, linea - 2)
            linea -= (linea_sig + 5)
        else:
            linea -= linea_sig
    else:
        if aux_2 == 0:
            c.setFont('Helvetica', 12)
            aux_2 += 1
        c.rect(horiz_izq - 3, linea - 4, horiz_der - horiz_izq + 15, 20)
        c.drawString(horiz_izq, linea, f"{cut_name(producto)}")
        c.drawString(horiz_der - 25, linea, f"{str(to_integer(cantidad))}")
        c.rect(horiz_der + 12, linea - 4, 105, 20)
        c.rect(horiz_der + 12, linea - 4, 52, 20)
        contador = contador + 1
        linea -= 20

    if contador > 34: # original 28
        contador = -3
        c.showPage()
        linea = 785  # Donde comienza la primera linea
        horiz_izq = 40  # Donde se ubica la lista de productos a la izq.
        horiz_der = 450  # Donde se ubica la lista de cantidades a la der.
        linea_sig = 15  # Decremento normal para siguiente linea.
c.save()
