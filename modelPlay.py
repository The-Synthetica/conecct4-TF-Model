import numpy as np
import evalue
import playableFunctions as pf
from keras.models import load_model
import random
import asyncio


# Define una función para convertir un símbolo en su valor numérico correspondiente
def symbol_to_numeric(symbol):
    symbol_to_value = {'x': 1, 'o': -1, '-': 0}
    return symbol_to_value[symbol]


# Carga el modelo desde el archivo
model = load_model('./newGuildvtest2LINEARV.h5')  # Cargamos el modelo

# Tablero
table= pf.reset()


async def predict(matrix, move, intent, player):

    state= np.array(matrix)
    state[move['pos'], move['row']]= player

    if evalue.evaluate(state):
        if intent=='draw':
            return 5
        elif intent=='x':
            return 5
        else:
            return 5

    # state = np.array(state)
    # Aplica la función de mapeo a toda la matriz states
    vectorized_symbol_to_numeric = np.vectorize(symbol_to_numeric)
    state = vectorized_symbol_to_numeric(state)
    state= np.array([state])

    prediction = model.predict(state, verbose=False)

    if intent=='draw':
        return prediction[0][0]
    elif intent=='x':
        return prediction[0][1]
    else:
        return prediction[0][2]

async def bestMove(tablero, intent, player):

    if player=='x': player2='o'
    else: player2='x'


    moves= await pf.dispMoves(tablero)

    if moves:
        resAmigo= await asyncio.gather(*[predict(tablero, move, intent, player) for move in moves])
        resEnemigo= await asyncio.gather(*[predict(tablero, move, player2, player2) for move in moves])

        pos= 0

        arr1=[]
        for i in range(len(resAmigo)):
            if resAmigo[i] > resAmigo[pos] or arr1==[]:
                pos= i
                arr1=[]
                arr1.append(i)
            elif resAmigo[i] == resAmigo[pos]:
                arr1.append(i)

        arr2=[]
        for i in range(len(resEnemigo)):
            if resEnemigo[i] > resEnemigo[pos] or arr2==[]:
                pos= i
                arr2=[]
                arr2.append(i)
            elif resEnemigo[i] == resEnemigo[pos]:
                arr2.append(i)

        print(resAmigo, arr1)
        print(resEnemigo, arr2)

        random.shuffle(arr1)
        random.shuffle(arr2)
    
        if(resAmigo[arr1[0]] > resEnemigo[arr2[0]]): return moves[arr1[0]]
        
        return moves[arr2[0]]

    return False

async def genModelMove(tablero, intent, player):
    
    Mov= await bestMove(tablero, intent, player)

    if Mov:    
        tablero[Mov['pos'], Mov['row']]= player
        return tablero, True
    
    else:
        return tablero, False

async def play(player1, tablero):

    # Player Check
    if player1=='o': 
        player2='x'
    else: 
        player2='o'


    # Gen Moves
    tablero, move= await genModelMove(tablero, player1, player1)
    if move:

        if evalue.evaluate(tablero):
            return {'tablero': tablero, 'winner': player1}
                
        else:
            return play(player2, tablero)
    
    else:
        return {'tablero': tablero, 'winner': 'draw'}


async def playGame(player):
    tablero= pf.reset()
    return await play(player, tablero)