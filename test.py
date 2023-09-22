import numpy as np
import modelPlay as mp
import asyncio


async def main():
    # state= np.array([       ['o', 'o', 'o', '-', 'x', 'o', '-'], 
    #                         ['x', 'x', 'x', '-', 'x', 'x', '-'], 
    #                         ['o', 'o', 'x', 'o', 'x', 'o', '-'], 
    #                         ['x', 'o', 'x', 'x', 'o', 'o', '-'], 
    #                         ['x', 'x', 'o', 'x', 'o', 'o', 'o'], 
    #                         ['o', 'x', 'o', 'x', 'o', 'x', 'x'],])
    state= np.array([       ['-', '-', '-', '-', '-', '-', '-'], 
                            ['-', '-', '-', 'o', '-', '-', '-'], 
                            ['-', '-', 'o', 'x', 'x', '-', '-'], 
                            ['-', '-', 'x', 'x', 'o', '-', '-'], 
                            ['-', '-', 'o', 'o', 'x', 'o', '-'], 
                            ['-', '-', 'o', 'x', 'x', 'x', 'o'],])

    print(state)

    next_move , xs = await mp.genModelMove(state, 'x', 'x') 

    print(next_move)

asyncio.run(main())