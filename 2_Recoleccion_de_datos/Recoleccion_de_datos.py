from pyArduino import * #pip install pyserial
import collections
import matplotlib.pyplot as plt #pip install matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.animation as animation
from tkinter import *
import copy

# Comunicacion Serial
serialPort = 'COM4'
baudRate  = 115200
sizeData = 3

#P1 Adelante
#P2 Atras
#P3 Derecha
#P4 Izquierda
#P5 Detener

def start():
    global isCollect
    isCollect = True
    estado.config(text = "Recolectando datos")
    
def pause():
    global isCollect
    isCollect = False
    estado.config(text = "Pausa")

def delete():
    global isCollect
    isCollect = False
    del collectData[:]
    estado.config(text = "Datos borrados")
    
def save():
    global isCollect
    isCollect = False
    estado.config(text = "Guardando datos")
    with open(entry.get()+'.npy','wb') as f:
        np.save(f,collectData)
    delete()
    estado.config(text = entry.get()+ " Guardado")
    
    

def onClosing():
     root.quit()
     arduino.close()
     root.destroy()

def plotData(self,lines, lineValueText):
     for i in range(sizeData):
          data[i].append(arduino.rawData[i])
          lines[i].set_data(range(samples),data[i])
          lineValueText[i].set_text('signal'+str(i)+' = ' + str(arduino.rawData[i]))

     if isCollect:
         collectData.append(copy.deepcopy(arduino.rawData))


# Almacenamiento de datos
isCollect = False
collectData = []


# Graficas
samples  = 100
sampleTime = 200
data = []

for i in range(sizeData):
     data.append(collections.deque([0]*samples, maxlen = samples))
     
xmin = 0
xmax = samples
ymin = -15
ymax = 15

lines = []
lineValueText = []

################# Crear grafica ##################

fig = plt.figure()
ax = plt.axes(xlim= (xmin,xmax), ylim=(ymin,ymax))
plt.title('Monitoreo en tiempo real')
plt.grid()
ax.set_xlabel('Muestras')
ax.set_ylabel('Medida')

for i in range(sizeData):
     lines.append(ax.plot([], [], label='signal'+str(i))[0])
     lineValueText.append(ax.text(0.65, 0.90-i*0.05, '', transform=ax.transAxes))

plt.legend(loc="upper left")

############## Abrir puerto serial ##############
arduino = serialArduino(serialPort,baudRate,sizeData)# Objeto serial
arduino.readSerialStart() # Inicia lectura de datos

############### Intefaz Grafica ####################

root = Tk()
root.protocol('WM_DELETE_WINDOW', onClosing)

canvas = FigureCanvasTkAgg(fig, master = root)
canvas._tkcanvas.grid(row = 0,column = 0)

entry = Entry(root, justify = LEFT)
entry.insert(END,'P1')
entry.grid(row = 1, column = 0, padx = 20, pady = 20)

button1 = Button(root,text='Iniciar',command = start,font=16)
button1.grid(row = 2,column = 0, padx = 20, pady = 20)

estado = Label(root,text = "Clic para iniciar")
estado.grid(row = 3,column = 0, padx = 20, pady = 20)

button2 = Button(root,text='Pausar',command = pause,font=16)
button2.grid(row = 2,column = 1, padx = 20, pady = 20)

button3 = Button(root,text='Borrar',command = delete,font=16)
button3.grid(row = 2,column = 2, padx = 20, pady = 20)

button4 = Button(root,text='Guardar',command = save,font=16)
button4.grid(row = 2,column = 4, padx = 20, pady = 20)


anim = animation.FuncAnimation(fig,plotData, cache_frame_data=False, fargs=(lines, lineValueText), interval=sampleTime)    # fargs has to be a tuple

root.configure(bg='white')
root.mainloop()

















     
