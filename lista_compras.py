# Script para generar lista de compras en formato pdf

from copy import copy
import tkinter.filedialog
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import pandas as pd
from tkinter import getint

import tkinter as tk
from tkinter.simpledialog import askstring, askinteger
from tkinter.messagebox import showerror


def clean_item(cantidad):
    """Procesa la cantidad a sumar."""
    cantidad = cantidad.strip()
    l_cant = cantidad.split(" ")
    elemento = l_cant[0]
    if "," in elemento:
        componentes = elemento.split(",")
        elemento = float(f"{componentes[0]}.{componentes[1]}")
    else:
        elemento = float(elemento)
    return elemento


def clean_safe(cantidad):
    """Limpia datos de entrada."""
    numero = list()
    divisor = list()
    hay_divisor = False
    cifras = set([str(i) for i in range(0, 10)])
    dots = set([",", "."])
    for caracter in cantidad:
        if not hay_divisor:
            print("not")
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
        numero_final = float(numero_final)
        num_divisor = float(num_divisor)
        return numero_final / num_divisor
    print(f"el numero final es: {numero_final}")
    return float(numero_final)


def display_2(lista, ventana):
    inicio = entry_1.get()
    fin = entry_2.get()

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

# Create the widgets
entry_1 = tk.Entry(root)
# btn_1 = tk.Button(root, text = "Display Text", command = display_2)

entry_2 = tk.Entry(root)
inputs = []
btn_2 = tk.Button(root, text = "Ingresar Límites", command = lambda: display_2(inputs, root))


# Grid is used to add the widgets to root
# Alternatives are Pack and Place
entry_1.grid(row = 1, column = 0, padx=10, pady=10)
entry_2.grid(row = 1, column = 1, padx=10, pady=10)
btn_2.grid(row = 2, column = 1, padx=10, pady=10)

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

for pedido in pedidos_en_tuplas:
    pedido_final = []
    for tupla in pedido:
        if (tupla[1] != "") and (tupla[0] != "nro_pedido"):
            pedido_final.append(tupla)
    lista_definitiva.append(pedido_final)

lista_definitiva = lista_definitiva[inputs[0]:inputs[1]]

nro_pedido = 1
for pedido in lista_definitiva:
    for item in pedido:
        print(item)
        if item[0] in diccionario_productos:
            diccionario_productos[item[0]] += float(clean_safe(item[1]))
    print(" $$$$$$$$$$$$$$$$$$$$$$$$$$$$$")

for key, value in diccionario_productos.items():
    print("---  inicio  ---")
    print(key)
    print(value)
    print("---  fin ---\n")
