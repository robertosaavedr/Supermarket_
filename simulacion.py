"""author : Roberto Saavedra"""

from datetime import datetime, timedelta
from scipy.stats import expon, randint, binom
from class_warehouse import Warehouse
import argparse


def format_date(dt):
    meses = ("ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep",
             "oct", "nov", "dic")
    day, month, year, hour, minute = dt.day, meses[dt.month-1], dt.year, dt.hour, dt.minute
    return "{}-{}-{} {}:{:02d}".format(day, month, year, hour, minute)


def supermarket_log(starting_time, finish_time, warehouse, file):  # one day operation
    """
    Simulating one day of restock and sells in a supermarket, the events in the supermarket follow an exponential
    distribution with an average time between events of 5 minutes. Each time that an event occur, the next event
    (restock or sell) is chosen with a binomial distribution where a sell has probability 0.65 and a restock 0.35.
    When a client buy a product, that product is selected randomly uniformly, whereas the quantity is chosen
    from a binomial with n=(max quantity of the product chosen) and p=0.15
    We are making one restock at once, each time that a restock is made the product selected is randomly uniformly
    chosen, meanwhile the quantity of the product to restock is chosen from a binomial where
    n=(max quantity allowed in shelves), p=0.65

    Parameters
    ----------
    starting_time:
        supermarket opening time
    finish_time:
        supermarket closing time
    warehouse:
        class Warehouse where our products catalog is saved, we need this information to know products and their codes
        in our supermarket
    file:
        file path in which save our daily log
    """

    log = []
    last_hour = starting_time
    while last_hour < finish_time:  # our loop finish when the last transaction has passed finish_time
        if binom.rvs(1, 0.65):
            product_chosen = list(warehouse.products.keys())[randint.rvs(1, 19) - 1]
            last_hour += timedelta(minutes=float(expon.rvs(scale=5, size=1)))
            aux = ['venta', last_hour, product_chosen, binom.rvs(n=warehouse[product_chosen][0], p=0.15, loc=1)]
            log.append(aux)
        else:
            last_hour += timedelta(minutes=float(expon.rvs(scale=5, size=1)))
            product_chosen = list(warehouse.products.keys())[randint.rvs(0, len(amazon.products) - 1)]
            log.append(['repo', last_hour, product_chosen, binom.rvs(n=warehouse[product_chosen][0], p=0.65, loc=1)])
    with open(file, 'w') as f:
        text = ""
        for el in log:
            text += el[0] + ' ' + format_date(el[1]) + " " + el[2] + " " + str(el[3]) + "\n"
        f.write(text)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Para poder ejecutar este script, debe poner como primer argumento'
                                                 ' el archivo donde se almacena su inventario para que la simulación '
                                                 'tenga esos productos como ejemplos', epilog='Enjoy the script!!!')
    parser.add_argument('inventario', help='archivo que contiene la información para cada producto')
    args = parser.parse_args()

    amazon = Warehouse()
    amazon.load_from_txt(args.inventario)
    supermarket_log(datetime(2006, 10, 20, 8, 30, 00), datetime(2006, 10, 20, 21, 30, 00), amazon, 'guardar')
