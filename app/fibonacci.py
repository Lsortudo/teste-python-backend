#Logica do CMD de fibonacci

def fibonacci(n):
    fib_list = [0, 1]
    for i in range(2, n):
      fib_list.append(fib_list[i-1] + fib_list[i-2])
    return fib_list[:n]

"""
Jeito antigo que vai retornar APENAS o fibonacci especificado, ex: o usuario digitou 7, ele vai fazer ate o 7 numero e retornar o valor do SETIMO
def fibonacciteste(n):
    if n < 0:
        raise ValueError("Número deve ser positivo")
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)
"""