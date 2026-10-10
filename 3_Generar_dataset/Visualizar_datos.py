import numpy as np

import matplotlib.pyplot as plt

import glob



#todos los archivos que contengan "p" y con extension npy

path = r'P*.*npy'

files = glob.glob(path)

#Se define la graica

fig = plt.figure(figsize=(8, 8))

ax = fig.add_subplot(111, projection='3d')



#bucle para graficar cada uno de los datos sobre la misma grafica

for file in files:

   

    data = np.load(file)

    x = data[:, 0]*-1

    y = data[:, 1]*-1

    z = data[:, 2]*-1

   

    ax.scatter(x, y, z)
    ax.legend(files)

   

plt.show()
