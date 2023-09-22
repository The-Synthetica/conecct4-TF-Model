import play
import numpy as np
import asyncio
import csv

csvfile= "./c4_game_database.csv"

# Importamos
import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense
from keras.losses import binary_crossentropy
from keras.optimizers import Adam
from keras.utils import to_categorical
from keras.layers import LSTM

# Esta funcion extrae la data pasada de un csv
def extractCSVdata(file):
    res=[]
    data=[]

    with open(file, 'r') as file:
            csvreader = csv.reader(file)
            for row in csvreader:
                # Convierte todos los elementos de la fila a enteros
                row = [int(item) if item != '' else 0 for item in row]
                
                data.append(np.array([row[0:42]]).reshape(6,7))
                res.append(row[42])


    data.pop(0)
    print(res[0])
    res.pop(0)

    return data, res


# Define una función para convertir un símbolo en su valor numérico correspondiente
def symbol_to_numeric(symbol):
    symbol_to_value = {'x': 1, 'o': -1, '-': 0}
    return symbol_to_value[symbol]

# Generamos una cantidad de juegos (con su desarrollo y final)
async def generate_games(number_of_games):
    games = []

    for _ in range(number_of_games):
        data = await play.playGame('x')
        tableData=[]

        for tablero in data['tableros']:
            table= np.array(tablero)

            # Aplica la función de mapeo a toda la matriz states
            vectorized_symbol_to_numeric = np.vectorize(symbol_to_numeric)
            table = vectorized_symbol_to_numeric(table)

            tableData.append(table)
        
        tableData= np.array(tableData)

        game_data = {
            'tableros': tableData,
            'winner': 1 if data['winner'] == 'x' else -1 if data['winner'] == 'o' else 0
        }
        
        games.append(game_data)

    return games


# Define el modelo con una capa LSTM, una densa y oculta,
model = tf.keras.Sequential([
    tf.keras.layers.LSTM(100, activation='linear', input_shape=(6, 7)),
    tf.keras.layers.Dense(100, activation='linear'),
    tf.keras.layers.Dense(3, activation='softmax')
])


# Define la función de pérdida
loss_fn = tf.keras.losses.CategoricalCrossentropy()

# Define the optimizer
optimizer = tf.keras.optimizers.Adam()

# Compila el modelo
model.compile(optimizer=optimizer, loss=loss_fn, metrics=['accuracy'])

states=[]
results=[]

# csv extract
states, results= extractCSVdata(csvfile)

# Train the model
for epoch in range(0):
  # Generate training data
  print('Epoch ', epoch ,' data generated correctly')
  games = asyncio.run( generate_games(100) )

  for i in range(0,100):

    for tablero in games[i]['tableros']:
            states.append(tablero)
            results.append(games[i]['winner'])

states = np.array(states)
results = np.array(results)

results= results.astype(np.float32)

print(results.dtype)

# Codifica etiquetas en formato one-hot
results_one_hot = to_categorical(results, num_classes=3)
results_one_hot = np.array(results_one_hot)

# Ahora, states contiene la representación numérica de todos los tableros en tu conjunto de datos
# Confirmemos las dimensiones y comparemos resultados.
print("Dimensiones de states:", states.shape)
print("Dimensiones de results:", results.shape)
print("Dimensiones de results:", results_one_hot.shape)

print(results_one_hot[0], results[0])
print(results_one_hot[1], results[1])
print(results_one_hot[2], results[2])



# Entrena el modelo
model.fit(states, results_one_hot, epochs=50, batch_size=128)



# Evaluate the model
games = asyncio.run( generate_games(100) )

test_states=[]
test_results=[]

for i in range(0,100):

    for tablero in games[i]['tableros']:
            test_states.append(tablero)
            test_results.append(games[i]['winner'])

test_states = np.array(test_states)
test_results = np.array(test_results)

test_results = test_results.astype(np.float32)  # Convertir a flotantes si es necesario

# Codifica tus etiquetas de prueba en formato one-hot
test_results_one_hot = to_categorical(test_results, num_classes=3)

test_loss = model.evaluate(test_states, test_results_one_hot, verbose=0)


print("Test loss:", test_loss)

# Guardar el modelo en un archivo
model.save("newGuildvtest2LINEARV.h5")
print('guardado')

tabletest= np.array([     ['-', '-', '-', '-', '-', '-', '-'], 
                          ['-', '-', '-', '-', '-', '-', '-'], 
                          ['-', '-', '-', 'x', '-', 'o', '-'], 
                          ['-', '-', 'o', 'o', 'o', 'x', '-'], 
                          ['-', '-', 'x', 'o', 'o', 'x', '-'], 
                          ['-', '-', 'x', 'o', 'o', 'x', 'x'],])

# Aplica la función de mapeo a toda la matriz states
vectorized_symbol_to_numeric = np.vectorize(symbol_to_numeric)
tabletest = vectorized_symbol_to_numeric(tabletest)
tabletest= np.array([tabletest])

print(tabletest, tabletest.shape)

# Predict the next move
next_move = model.predict(tabletest)

# Print the next move
print(next_move)