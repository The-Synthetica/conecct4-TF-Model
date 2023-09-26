
# Proyecto Modelo Connect4 TF

Voy a dejar este documento exclusivamente en español y casi como un apunte sobre como fue el desarrollo hasta este punto de un modelo predictivo del juego 4 en Linea. 💀👉👈

Intentare hacer detalle de los errores y el planeamiento del mismo. Espero que tambien pueda ayudarte 😅

Nota: Los tableros son SIEMPRE de 6x7


---
.

.

## Modulos y Funciones para el juego

#### Modulos
Comence creando varios (que fui modificando conforme avance en el desarrollo del modelo, como la aplicacion de asyncronismos para la espera de las predicciones o la adaptabilidad de los tableros)

Lo importante es entender que tenemos 3 modulos super importantes para la funcionalidad:

* **evalue.py**
    >> Recibe un tablero y retorna `True` -> Si tenemos un    ganador.
* **playableFunctions.py**
    >> Son las funciones que usa el modulo para asegurar que el los movimientos en realizados son validos. Tales como generarlos o asegurarse de que esten disponibles.
* **play.py**
    >> Es destinado a generar juegos validos y aleatorios, guardando el proceso, para el dataset que utilizara la IA.

.
#### Funciones
Las mas importantes de estos modulos, son:

**evalue.eval( tablero )** : Evaluamos si hubo ganadores
**play.playGame( player1 )** : Generamos un juego donde empieza pl1


---
.

.

## Modulos y Funciones para el entrenamieto
Genial, ahora que nos aseguramos de que nuestro juego es legal y valido (aunque no estamos seguros de su calidad, debido a la aleatoreidad de los movimientos)

Procedemos a usar los datos para entrenar y testear la IA!

#### Modulos

* **main.py**
    >> Este modulo esta diseñado para crear el modelo. Tuvo muchisimos rediseños y todavia sigo experimentando con la estructura de la red neuronal. 
    * Composicion de red:
        * Capa convulsional LSTM 100 neuronas (Linear)
        * Capa densa de 100 neuronas (Linear)
        * Capa de clasificacion de 3 neuronas (x, o, empate)
    * Forma de datos:
        * Un vector np donde cada elemento es un tablero de 6x7 con la representacion numerica correspondiente a cada jugador (-1, 1, 0)
        * Un vector np donde cada elemento corresponde a el resultado final de cada tablero del vector de tableros

* **modelPlay.py**
    >> Modulo encargado de utilizar el modelo para generar predicciones y movimientos basados en las mismas. Con este modulo ya podemos utilizar la IA
* **test.py**
    >> Probamos mediciones del modelo, tambien sirve para poder jugar una partida entera de forma mas prolija.

.
#### Funciones
Las mas importantes de estos modulos, son:

**modulePlay.predict( tablero, movimiento, intent, player )** : 
Predice cual es el "peso" para un movimiento simulado en el tablero, basado en la intencion del jugador, y el jugador que mueve.
| Parametro | Tipo     | Descripcion              |
| :-------- | :------- | :------------------------- |
| `tablero` | `Matriz 6x7` | Compuesta por 'x' 'o' '-' |
| `movimiento` | ` { Fila: n ; Columna: m}` | El movimiento a simular|
| `intent` | `'x'` `'o'` `'draw'` | Intencion del movimiento |
| `player` | `'x'` `'o'` | Quien realiza el movimiento |


```Retorna un valor numerico sobre la prediccion```

.

**modulePlay.bestMove( tablero, intent, player)**: Simula todos los posibles movimientos con la funcion prediccion, y retorna el mejor de todos 

```Retorna un objeto con el mejor tiro```

.

**modulePlay.genModelMove( tablero, intent, player)** : El modelo genera un movimiento basado en el tablero actual, la intencion del movimiento y el jugador que mueve.

```Retorna el tablero con el movimiento generado```

---
.

.

## Desarrollo e Implementacion
Ay porfavor, hubo demasiados errores en el proceso. Usual considerando que es uno de mis primeros proyectos con tensorflow.

* Red simple lineal
    >Primero pense en una red de 42 neuronas (tablero) que se conectan a la capa de clasificacion de 3 posibles estados de la partida.

    >> Salio mal... 💀

    >> Resultado? Una prediccion muy matematica que usaba regresiones lineares y ni si quiera podia distinguir estados. Digamos que solo era buena para saber quien habia ganado (muy tarde para hacer movimientos)

* Red convulsional (Relu??)
    > Investique y lo cambie a algo muy cercano a la configuracion actual. Ahora sabia clasificar de forma relativamente correcta! 🥳 (y los cambios chicos no mataban la clasificacion)
    
    > Pero olvide que habia estado aplicando relu 😃

    > Y el jugador 'o' en mi matriz se representa con -1 😐
    
    > Asi que solo podia clasificar para 1 💀

* LSTM (esta vez con Linear y listo)
    > Ahora si quedo joya 😅
    
    >Es el modelo actual, tiene muchas cosas que mejorar, como seguir experimentando con la cantidad de neuronas en vez de tirar 100
    
    >O estar seguro de que al menos, esta aprovechando bien los datos
.

.

.

.

## Posibles mejoras
Estuve pensando en pausar un poco este proyecto para seguir con otros y luego retomarlo, pero para dejar constancia hay 2 mejoras que pueden ser sustanciales.

* Metodo predictivo
    >> Literalmente solo compara los valores, estaria bueno pensar en tener tambien una funcion de respuesta para los mismos. 

    >> Por ejemplo, en vez de comparar solo las predicciones, comparar las mismas con el valor actual del tablero

* Calidad de datos
    >> Use varios csv, aunque solo me quede con uno que me gusto por ser de origen humano. Pero tener datos generados aleatoriamente no nos asegura NADA, sobre la calidad de la IA. 

    >> Podriamos usar modelos anteriores (que hay un monton) y tener datos que sean utiles para evidenciar puntos debiles de los 2 modelos Actuales de la IA.

* Podriamos implementar IA generativa, que vaya escalando desde cero y que mejore conforme va aprendiendo a derrotar a este modelo actual. seria intereseante pero todavia queda mucho por aprender.

.

.

## Links de bibliografia

- [Redes convulsionales](https://www.youtube.com/watch?v=4sWhhQwHqug&t=330s)
- [Funciones de Activacion](https://www.youtube.com/watch?v=_0wdproot34&t=21s)
- [Dimensionalidad de Datos](https://saturncloud.io/blog/tensorflow-logits-and-labels-must-have-the-same-first-dimension/)
- [Dataset del modelo entrenado con CSV humano](https://www.kaggle.com/datasets/tbrewer/connect-4)

-El resto de informacion general la extraen de la pagina oficial de
[TensorFlow](https://www.tensorflow.org/resources/models-datasets?hl=es-419)
o usen GPT 💀💀💀💀
![Logo](https://the-synthetica.github.io/src/proto.png)

