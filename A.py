"""author : Roberto Saavedra"""

import argparse
from inventory_from_txt import load_inventory


def sells(inventory: dict, file: str):
    """
    Procedure which reads a file containing a supermarket selling log, then updates a dictionary which contains
    supermarket stock

    Parameters
    ----------
    inventory :
        dict which contains information about each product
    file:
        string path

    Example
    -------
    >>> almacen = load_inventory('inventarioAlmacen.txt')
    >>> sells(almacen, 'ventasCajas.txt')
    Venta : 20-oct-2006 12:25 001 34
    Antes de :  100 25 70 001_AA Yogures de fresa
    Después de :  100 25 36 001_AA Yogures de fresa
    ======>Necesidad de reponer<========
    """

    with open(file, 'r') as f:
        for line in f:
            el = line.split(" ", 3)
            el[3] = int(el[3])
            print(" Venta :", *el, "\n", "Antes de : ", *inventory[el[2]])
            if inventory[el[2]][2] - el[3] > 0:  # checking if there are enough units to make the sell
                inventory[el[2]][2] -= el[3]
                print(" Después de : ", *inventory[el[2]])
                if inventory[el[2]][2] - el[3] <= inventory[el[2]][1]:  # checking if a restock is needed
                    print(" ======>Necesidad de reponer<========")
            else:
                print(" =========>Venta imposible<========", "\n =======>Necesidad de reponer<=======")
            print("\n--------------------------------------------\n")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Para poder ejecutar este script, debe poner como primer argumento'
                                                 ' el archivo donde se almacena su inventario y como segundo argumento'
                                                 ' el log de ventas  e.g.:   > python A.py inventarioAlmacen.txt '
                                                 'ventasCajas.txt', epilog='Enjoy the script!!!')
    parser.add_argument('inventario', help='archivo que contiene la información para cada producto')
    parser.add_argument('ventas', help='archivo con las ventas a lo largo de un día')
    args = parser.parse_args()

    supermarket = load_inventory(args.inventario)
    sells(supermarket, args.ventas)
