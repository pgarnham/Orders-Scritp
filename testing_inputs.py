import tkinter as tk
from tkinter.simpledialog import askstring, askinteger
from tkinter.messagebox import showerror


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
