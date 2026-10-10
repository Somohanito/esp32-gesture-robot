import numpy as np

class dataset:
     def __init__(self,numClass = 1):
          self.numClass = numClass
          self.totalSamples = 0
          self.numInputs = 0
          self.sizeSubClass = []
     def read(self):
          P = [] #[samples][sensor]
          # open output file for reading
          for i in range(self.numClass):
               with open('p'+str(i+1)+'.npy', 'rb') as f:
                    dataset = np.load(f)
               self.sizeSubClass.append(len(dataset))
               self.totalSamples  = self.totalSamples + self.sizeSubClass[i]  
               P.append(dataset)

          self.numInputs = len(P[0][0])
          # Dataset
          self.datasetInput = np.array(P[0])  #[sample,input]
          for i in range(self.numClass-1):
               classData = np.array(P[i+1])
               self.datasetInput = np.concatenate((self.datasetInput,classData))
     
