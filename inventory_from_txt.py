"""author: Roberto Saavedra"""

def load_inventory(file: str, sep=",") -> dict:
    """
    Read a file separated by , into a dictionary

    Parameters
    ----------

    file: str
        string path

    sep: str
        delimiter to use.

    Returns
    -------
        dictionary which contains an inventory

    Examples
    --------
    >>> almacen = load_inventory('inventarioAlmacen.txt')
    >>> print(almacen)
    {'001': [100, 25, 70, '001_AA', 'Yogures de fresa'], '002': .......
    """

    inventory = dict()
    with open(file, "r") as f:
        for line in f:
            el = line.split(sep)
            inventory[el[0].strip()] = list(map(int, el[1:4])) + list(map(lambda x: x.strip(), el[4:len(el)]))
    return inventory
