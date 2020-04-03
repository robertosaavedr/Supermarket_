"""author : Roberto Saavedra"""
from copy import deepcopy


class Warehouse:
    """
    Manages a supermarket inventory, allowing to operate with supermarket stock either adding up or subtracting, you are
    able to load your dictionary from a external file. Attributes are show below(products and _copy_products)

    products :
        A dictionary whose keys are the product code and its elements are the maximum and minimum number of units
        in our shelves, our actual stock for each product, their locations in our supermarket and a brief description.
    _copy_products :
        In order to implement a Context Manager we have deepcopied our dictionary products, this backup
        will be helpful if we want to undo an operation.
    """

    def __init__(self):
        """Constructor. Initialize our products dictionary"""
        self.products = dict()

    def __getitem__(self, code: str) -> list:
        """
        This magic method allows us to index our dict without write Warehouse.products[] using instead Warehouse[]

        Parameters
        ----------
        code :
            product code which is a dict key

        Example
        -------
            >>> amazon = Warehouse()
            >>> amazon.add_products('001', 4, 1, 2, 'SOUTH', 'Rice')
            >>> amazon['001']
            [4, 1, 2, 'SOUTH', 'Rice']
            >>> amazon.products['001']
            [4, 1, 2, 'SOUTH', 'Rice']
        """

        return self.products[code]

    def __enter__(self):
        """Backing up our main dictionary"""
        self._copy_products = deepcopy(self.products)  # deepcopying to deal with mutability
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        When exc_type is not None undo the operation deepcopying _copy_products

        Parameters
        ----------
        exc_type :
            exception type
        exc_val :
            exception value
        exc_tb :
            traceback
        """

        if exc_type:
            self.products = deepcopy(self._copy_products)  # deepcopy to deal with mutability

    def add_products(self, code, maximum, minimum, stock, location, description):
        """
        This method add a product to our dictionary.

        Parameters
        ----------
        code :
            product code
        maximum :
            maximum allowed in supermarket shelves
        minimum :
            minimum allowed in supermarket shelves
        stock :
            actual stock in shelves
        location :
            location in supermarket
        description :
            briefly descriptor
        """

        self.products[code] = [maximum, minimum, stock, location, description]

    def load_from_txt(self, file: str):
        """
        This method loads products from a external file into a dictionary

        Parameters
        ----------
        file :
            file path where our inventory is located
        """

        with open(file, 'r') as f:
            for line in f:
                aux = line.split(',')
                self.add_products(aux[0].strip(), int(aux[1]), int(aux[2]), int(aux[3]), aux[4].strip(), aux[5].strip())

    def update_stock(self, code: str, amount: int, sw: bool) -> ValueError:
        """
        This method updates the units of a given product either adding up or subtracting

        Parameters
        ----------
        code :
            Id of product
        amount :
            units of product, when is >0 is a restock else is a sell
        sw :
            1 when restocking, 0 when selling
        Return:
        -------
            A str containing the error description
        """

        try:
            with self:
                # our stock is either lower than 0 or greater than max allowed we do the transaction
                self.products[code][2] += amount
                # then, we check if we can do the sell or restock, if the ValueError is raised we will undo the
                # operation due to the magic method __exit__
                if sw and self[code][2] > self[code][0]:
                    raise ValueError(' REPOSICION IMPOSIBLE, NO CABEN MAS UNIDADES EN LAS ESTANTERIAS')
                if not sw and self[code][2] < 0:
                    raise ValueError(' VENTA IMPOSIBLE')
                return ''
        except ValueError as exc:
            if sw:  # if got an imposible restock we are going to restock as much units as possible
                self.products[code][2] += self[code][0] - self[code][2]
            return f'{exc} \n'

    def update_inventory_from_txt(self, file):
        """
        Given a file this method read every line, differencing between sells and restocks, updating the stock in a
        given inventory.

        Parameters
        ----------
        file :
            path to a file containing a supermarket transaction log
        """

        with open(file, 'r') as f:
            for line in f:
                transaction = line.split(' ', 4)
                sw = 0 if transaction[0] == 'venta' else 1
                transaction[4] = int(transaction[4])
                # amount e.g. if we got a sell and our units are 9, we want to subtract the current stock, as we got a
                # sell
                # sw=0, -(not 0) * 9 + 0 * 9 -> -9; sw=1, -(0) * 9 + 1*9 -> 9
                amount = -(not sw) * transaction[4] + sw * transaction[4]
                before = list(self[transaction[3]])  # saving dict['code'] to print later
                error = self.update_stock(transaction[3], amount, sw)  # saving error if there were
                restock_needed = self[transaction[3]][2] < self[transaction[3]][1]
                # we are using sw to print what we need in each situation, if got a sell(sw=0) we will print 'VENTA'
                print('\n OPERACION  : ', (not sw) * ' VENTA', sw * 'REPOSICION', *transaction[1:],
                      '\n ANTES DE   :  ', *before,  # printing the state of our inventory before update
                      restock_needed * '\n SE ACONSEJA REPONER',
                      '\n' + error,
                      'DESPUES DE :  ', *self[transaction[3]], '\n', '_' * 127)
