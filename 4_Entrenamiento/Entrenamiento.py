import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.utils import to_categorical

from arduinoKeras import weights
from arduinoKeras import layers
from arduinoKeras import scaling

import matplotlib.pyplot as plt

# Importar datos
num_classes = 5
P = np.load('P.npy')
T = np.load('T.npy')

# Preprocesamiento de datos
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler().fit(P)

P = scaler.transform(P)
one_hot_labels = to_categorical(T,num_classes = num_classes) #574, 5

# Dividir el conjunto de datos en conjunto de entrenamiento y validacion
from sklearn.model_selection import train_test_split

P_train, P_test, T_train, T_test = train_test_split(P,one_hot_labels,test_size=0.20,random_state = 42)

# Establecer hiperparametros de algoritmo (tasa aprendizaje, epocas)
epochs = 1000

# Definir la aquitectura de la red neuronal
hiddenNodes = 2
inputs = 3

model = Sequential()
model.add(Dense(hiddenNodes, activation = 'relu', input_dim=inputs))
model.add(Dense(num_classes, activation = 'softmax'))
model.summary()

# Declarar Funcion de perdida
loss = 'categorical_crossentropy'

# Optimizador
optimizer = tf.keras.optimizers.Adam()


# Entrenamiento
model.compile(loss = loss,
              optimizer = optimizer,
              metrics = "accuracy")

history = model.fit(P_train, T_train, epochs = epochs, verbose = 1, validation_split = 0.1)
plt.xlabel('Epocas')
plt.ylabel('Perdida')
plt.plot(history.epoch, np.array(history.history['loss']),'b', label='Perdida de entrenamiento')
plt.plot(history.epoch, np.array(history.history['val_loss']),'r', label='Perdida de validacion')
plt.grid()
plt.legend()

plt.figure()
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.legend(['Exactitud de entrenamiento','Exactitud de validacion'])
plt.grid()

print(f"Exactitud de validacion sklearn: {model.evaluate(P_test, T_test)[1]}")


# Extraer el modelo neuronal para Arduino
weights(model.layers,3) # Pesos y bias
scaling(scaler,3) # Media y la desviacion estandar
layers(model.layers) # Arquitectura de la red neuronal

plt.show()










