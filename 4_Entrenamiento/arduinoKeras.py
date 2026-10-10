import numpy as np

def weights(layer,n):
    dim=len(layer);
    W="\n\n///////////////////////////////// Variables Red Neuronal /////////////////////////////////\n"
    b="\n"
    for k in range(dim):

        weights = layer[k].get_weights()[0].T
        biases  = layer[k].get_weights()[1]
        
        rowB = biases.shape[0]

        
        rowW = weights.shape[0]
        colW = weights.shape[1]
        W = W+"double a"+str(k)+"["+str(colW)+"];\n"
        W = W+"double W"+str(k+1)+"[" + str(rowW) + "][" +str(colW) + "] = {{"
        for i in range(rowW):
            for j in range(colW):
                if j==colW-1:
                    W = W+str(round(weights[i][j],n))+"}"
                else:
                    W = W+str(round(weights[i][j],n))+","
            if i==rowW-1:
                W = W +"};\n"
            else:
                W = W +",{"

        b = b+ "double b"+str(k+1)+"[" + str(rowB) + "]= {"
        for i in range(rowB):
            if i==rowB-1:
                b = b+str(round(biases[i],n))+"};\n"
            else:
                b = b+str(round(biases[i],n))+","
    W = W+"double a"+str(dim)+"["+str(rowB)+"];"
    b = b + "double aux = 0.0;\n"
    b = b + "//////////////////////////////////////////////////////////////////\n\n\n"
    
    print(W,b)
        
def scaling(scaler,n):
    meanData = "///////////////////////////////// Preprocesamiento Red Neuronal /////////////////////////////////\n"
    dim = scaler.mean_.shape[0]
    meanData =meanData+ "double mean["+str(dim)+"]={"
    stdData = "double dstd["+str(dim)+"]={"
    
    for i in range(dim):
        if i==dim-1:
            meanData = meanData+str(round(scaler.mean_[i],n))+"};"
            stdData = stdData+str(round(np.sqrt(scaler.var_[i]),n))+"};"
        else:
            meanData = meanData+str(round(scaler.mean_[i],n))+","
            stdData = stdData+str(round(np.sqrt(scaler.var_[i]),n))+","
        
    print(meanData)
    print(stdData)
    print("///////////////////////////////////////////////////////////////////////////////////////////////////////\n\n")

def layers(layer):
    print("///////////////////////////////// Estructura Red Neuronal /////////////////////////////////")
    for k in range(len(layer)):
        
        weights = layer[k].get_weights()[0].T;
        biases  = layer[k].get_weights()[1];
        
        rowB = biases.shape[0]
        rowW = weights.shape[0]
        colW = weights.shape[1]
        
        if layer[k].get_config()['activation']=='softmax':  
            capa = "double aux1 = 0;\nfor(int i = 0 ; i<"+str(rowW)+"; i++ ) {aux=0.0;for(int j = 0 ; j <"+str(colW)+" ; j++ )"
            capa = capa+"{ aux=aux+W"+str(k+1)+"[i][j]*a"+str(k)+"[j];} a"+str(k+1)+"[i]=(aux+b"+str(k+1)+"[i]);aux1=aux1+exp(a"+str(k+1)+"[i]);}"
            capa = capa+"\ndouble minimo = 0.0;"
            capa = capa+"\nint classes = 0;"
            capa = capa+ "\nfor(int i = 0;  i<"+str(rowW)+"; i++){a"+str(k+1)+"[i] = exp(a"+str(k+1)+"[i])/aux1;"+"if(a"+str(k+1)+"[i]>minimo){minimo=a"+str(k+1)+"[i];classes=i;}}"
        else:
           capa = "for(int i = 0 ; i<"+str(rowW)+"; i++ ) {aux=0.0;for(int j = 0 ; j <"+str(colW)+" ; j++ ) { aux=aux+W"+str(k+1)+"[i][j]*a"+str(k)+"[j];} a"+str(k+1)+"[i]="+layer[k].get_config()['activation']+"(aux+b"+str(k+1)+"[i]);}"
 
        print(capa)
    print("//////////////////////////////////////////////////////////////////////////////////////////\n\n") 
