from copy import deepcopy

class Warehouse:
    def __init__(self):
        self.products = dict()

    def load_from_txt(self, file):
        with open(file, 'r') as f:
            for line in f:
                aux = line.split(',')
                self.add_products(aux[0].strip(), int(aux[1]), int(aux[2]), int(aux[3]), aux[4].strip(), aux[5].strip())

    def add_products(self, code, max, min, stock, location, description):

        self.products[code] = [max, min, stock, location, description]

    def sell(self, code, units_sold):
        #if self.products[code][2] - units_sold >= 0:
        if True:
            self.products[code][2] -= units_sold

    def restock(self, code, units_restocked):
        #if self.products[code][2] + units_restocked <= self.products[code][0]:
        if True:
            self.products[code][2] += units_restocked

    def __len__(self):
        return len(self.products)

    def __getitem__(self, code):
        return self.products[code]

    def  __str__(self):
        return f'almacen bastante bacano con {len(self)} productos'

    def __enter__(self):
        self._copy_products = deepcopy(self.products)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.products = deepcopy(self._copy_products)
        else:
            print('DONE')

  amazon = Warehouse()
    amazon.load_from_txt(r"C:\Users\Roberto Saavedra\Documents\Data Science\ESTADÍSTICA APLICADA\2\cuatri 2\python\supe"
                         r"rmarket\inventarioAlmacen.txt")
try:
    with amazon as a:
        a.restock('001', 40)
        if a['001'][2] > a['001'][0]:
            print('mamajuana')
            raise ValueError('sorry cannot go in debt')
        print('hakunamatata')
except ValueError as exc:
print(exc)

import copy
c = dict(amazon.products)
a
amazon.products['019'] = []

amazon.products['018'] = []