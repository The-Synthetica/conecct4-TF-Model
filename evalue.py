import numpy as np

# Buscamos si alguien gano y retornamos TRUE de haber un ganador
# Como el juego es por turnos, basta con buscar si hay una fila ganadora (el turno es obvio)


def compare(arr):
    arr=''.join(arr)
    if arr.find('oooo') != -1 : return True
    if arr.find('xxxx') != -1 : return True

    return False


def evaluate(matrix):
    inverted_matrix= np.rot90(matrix)

    # Verticales
    for i in range(0,7):
        if compare(matrix[:, i]): 
            return True

    # Horizontales
    for i in range(0,6):
        if compare(matrix[i]):
            return True

    # Diagonales de linea principal
    for i in range(0,7):
        if compare(np.diagonal(matrix, offset=(-3+i))): 
            return True

    #Diagonales de linea invertida
    for i in range(0,7):
        if compare(np.diagonal(inverted_matrix, offset=(-3+i))): 
            return True

    return False