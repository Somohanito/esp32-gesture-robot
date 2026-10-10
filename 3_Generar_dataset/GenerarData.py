from readDataset import *
import matplotlib.pyplot as plt

sizeClass = 5 # Cantidad de clases a clasificar


################## DATOS DE ENTRADA ################

d = dataset(sizeClass)

d.read()


print(f" Tamaño Entrada : {d.datasetInput.shape}")

for i in range(sizeClass):
    print(f" Tamano Clase {i} : {d.sizeSubClass[i]}")


################# DATOS DE SALIDA ##################

T = np.concatenate((np.zeros((d.sizeSubClass[0],1)),
                    np.ones((d.sizeSubClass[1],1)),
                    2*np.ones((d.sizeSubClass[2],1)),
                    3*np.ones((d.sizeSubClass[3],1)),
                    4*np.ones((d.sizeSubClass[4],1))), axis=0)

print(f" Tamaño Salida : {T.shape}")                

np.save('P', d.datasetInput)
np.save('T', T)

for i in range(d.numInputs):
    plt.plot(d.datasetInput[:,i],label  = 'Data' +str(i+1))
    plt.legend(loc = "upper left")
    

plt.grid()
plt.show()

