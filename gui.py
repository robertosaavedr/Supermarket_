import tkinter as tk
from class_warehouse import Warehouse
from ABC import cargar_datos
import pandas as pd
from pandastable import Table, TableModlog

ventana = tk.Tk()

reponer = tk.Label(ventana, text="Necesidad de reponer!")

def ventas_reposiciones(inventario, archivo):
    f = open(archivo, 'r')
    for operacion in f:
        if operacion[:5] == 'venta':
            ventas = operacion[6:].split(" ", 3)
            ventas[3] = int(ventas[3])
            tk.Label(ventana, text=("Venta :" + str(ventas) + "\n" + "Antes de : " + str(inventario.productos[ventas[2]]))).pack()
            if inventario.productos[ventas[2]][2] - ventas[3] > 0:
                inventario.ventas(ventas[2], int(ventas[3]))
                tk.Label(ventana, text=("Después de : " + str(inventario.productos[ventas[2]]))).pack()
                if inventario.productos[ventas[2]][2] <= inventario.productos[ventas[2]][1]:
                    tk.Label(ventana, text=('Necesidad de reponer')).pack()
            else:
                tk.Label(ventana, text="venta imposible" + "\n Necesidad de reponer").pack()
        else:
            repo = operacion[6:].split(" ", 3)
            repo[3] = int(repo[3])
            tk.Label(ventana, text=("Reposición :" + str(repo) +   "\n" + "Antes de : " + str(inventario.productos[repo[2]]))).pack()
            if inventario.productos[repo[2]][2] + repo[3] <= inventario.productos[repo[2]][0]:
                inventario.repo(repo[2], int(repo[3]))
                tk.Label(ventana, text=("Después de : " + str(inventario.productos[repo[2]]))).pack
            else:
                tk.Label(ventana, text=('reposición imposible, repondremos hasta el máximo permitido')).pack
                inventario.productos[repo[2]][2] = inventario.productos[repo[2]][0]
                tk.Label(ventana, text=("Después de : " +  str(inventario.productos[repo[2]]))).pack()
    f.close()

ventana.title('MERCADONA')
ventana.geometry('380x300')
ventana.configure(background='peach puff')
amazon = Warehouse()
cargar_datos(r"C:\Users\Roberto Saavedra\Documents\Data Science\ESTADÍSTICA APLICADA\2\cuatri 2\python\supermarket"
                 r"\inventarioAlmacen.txt", amazon)
ventas_reposiciones(amazon, r"C:\Users\Roberto Saavedra\Documents\Data Science\ESTADÍSTICA APLICADA\2\cuatri 2\pyth"
                 r"on\supermarket\ventas_y_reposiciones.txt")

#mostramos el dataframe
df = pd.DataFrame.from_dict(amazon.productos, orient='index', columns=['MAX', 'MIX', 'STOCK', 'UBICACION', 'DESCRIP'])

root = tk.Tk()

rows, cols = df.shape

for r in range(rows):
    for c in range(cols):
        e = tk.Entry(root)
        e.insert(0, df.iloc[r, c])
        e.grid(row=r, column=c)
        # ENTER
        # e.bind('<Return>', lambda event, y=r, x=c: change(event, y,x))
        # ENTER on keypad
        # e.bind('<Return>', lambda event, y=r, x=c: change(event, y,x))
ventana.mainloop()
