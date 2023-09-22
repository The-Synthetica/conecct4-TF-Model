import numpy as np
import random

# Esta disponible la fila (tiene un lugar vacio??)
async def isAvailable(arr):
    arr=(''.join(arr))[::-1]
    search= arr.find('-')
    
    if search!= -1:
        return (6-(search+1))+1
    return False

# Obtengamos un vector donde almacenemos las filas disponibles y sus lugares
async def dispMoves(matrix):
    arr=[]
    
    for i in range(0, 7):
        state= await isAvailable(matrix[:,i])
        if state: arr.append({'row': i, 'pos': state-1})
    
    if arr!=[] : return arr
    return False

# Elijamos uno de los posibles movimientos disponibles
async def randMov(matrix):
    arr= await dispMoves(matrix)
    if arr:
        random.shuffle(arr)
        return arr[0]
    
    return False



# Reset
def reset():
    matrix = np.array([   ['-', '-', '-', '-', '-', '-', '-'], 
                          ['-', '-', '-', '-', '-', '-', '-'], 
                          ['-', '-', '-', '-', '-', '-', '-'], 
                          ['-', '-', '-', '-', '-', '-', '-'], 
                          ['-', '-', '-', '-', '-', '-', '-'], 
                          ['-', '-', '-', '-', '-', '-', '-'],])

    return matrix