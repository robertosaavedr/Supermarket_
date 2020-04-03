"""author : Roberto Saavedra """

from class_warehouse import Warehouse
import argparse


parser = argparse.ArgumentParser(description='Para poder ejecutar este script, debe poner como primer argumento'
                                             ' el archivo donde se almacena su inventario y como segundo argumento'
                                             ' el log de ventas y reposiciones', epilog='Enjoy the script!!!')
parser.add_argument('inventario', help='archivo que contiene la información para cada producto')
parser.add_argument('ventas_reposiciones', help='archivo con las ventas y reposiciones a lo largo de un día')
args = parser.parse_args()

if __name__ == '__main__':
    amazon = Warehouse()
    amazon.load_from_txt(args.inventario)
    amazon.update_inventory_from_txt(args.ventas_reposiciones)
