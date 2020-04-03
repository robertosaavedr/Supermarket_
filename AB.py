"""author : Roberto Saavedra"""

import argparse
from inventory_from_txt import load_inventory


def sells_and_restocks(inventory, file):
    """
    Procedure which read every line of a given file, in the follawing format:
    [VENTA | REPO] [DAY-MONTH(e.g. 'OCT', 'ENE')] [TIME(24H)] [PRODUCT CODE] [PRODUCT UNITS]
    Then, updates current stock in the given inventory

    Parameters
    ----------

    inventory:
        dictionary which contains products which we want to update
    file:
        string path
    """

    with open(file, 'r') as f:
        for line in f:
            transaction = line[:5]
            log = line[6:].split(' ', 3)
            log[3] = int(log[3])
            print(transaction.capitalize(), *log, "\n", "Antes de : ", *inventory[log[2]])
            if transaction == 'venta':
                if inventory[log[2]][2] - log[3] > 0:  # checking if there are enough units to make the sell
                    inventory[log[2]][2] -= log[3]
                    if inventory[log[2]][2] - log[3] <= inventory[log[2]][1]:  # checking if a restock is needed
                        print(" ======>Necesidad de reponer<========")
                else:  # not enough units
                    print(" =========>Venta imposible<========", "\n =======>Necesidad de reponer<=======")
            else:
                if inventory[log[2]][2] + log[3] <= inventory[log[2]][0]:  # checking if there are enough space
                    inventory[log[2]][2] += log[3]
                else:
                    print(' =========>Reposición imposible<========')
                    # we are going to restock as much units as possible
                    inventory[log[2]][2] += inventory[log[2]][0] - inventory[log[2]][2]
            print(" Después de : ", *inventory[log[2]], '\n', '_'*73, '\n')


if __name__ == '__main__':
    my_parser = argparse.ArgumentParser(description='Para poder ejecutar este script, debe poner como primer argumentp '
                                                    'el archivo donde se almacena su inventario y como segundo argumento'
                                                    ' el log de ventas y reposiciones                    '
                                                    '  e.g.:   > python A.py inventarioAlmacen.txt ventas_'
                                                    'reposiciones.txt', epilog='Enjoy the script!!!')
    my_parser.add_argument('inventario', help='archivo que contiene la información para cada producto')
    my_parser.add_argument('ventas_reposiciones', help='archivo con las ventas y reposiciones a lo largo de un día')
    args_ = my_parser.parse_args()

    supermarket = load_inventory(args_.inventario)
    sells_and_restocks(supermarket, args_.ventas_reposiciones)
