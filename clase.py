def suma_recursiva(m, n):
    if n == 1:
        return m
    else:
        return m + (suma_recursiva(m, n-1))


def prod_recursivo(a, n):
    if n == 1:
        return a
    else:
        return a*prod_recursivo(a, n-1)

if __name__ == '__main__':
    print('rayo homosexual ')