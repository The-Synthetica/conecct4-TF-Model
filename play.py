import numpy as np
import evalue
import playableFunctions as pf

# Tablero
table= pf.reset()

async def genMove(tablero, player):
    Mov= await pf.randMov(tablero)

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
    tablero, move= await genMove(tablero, player1)
    cpyTablero= np.array(tablero)


    if move:

        if evalue.evaluate(tablero): 
            return {'tableros': [cpyTablero], 'winner': player1}
                
        else:
            nextmove= await play(player2, tablero)
            return {'tableros': [cpyTablero] + nextmove['tableros'], 'winner': nextmove['winner']}
            
    
    else:
        return {'tableros': [cpyTablero], 'winner': 'draw'}


async def playGame(player):
    tablero= pf.reset()
    return await play(player, tablero)