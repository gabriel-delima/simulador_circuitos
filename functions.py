import numpy as np
import math
import cmath


#---------------------------------------------------------------------- Main Matrix


def setResistorsOnMainMatrix(storage,matrix):
    numberOfNodes = len(storage['nodes'])
    for i in range(numberOfNodes):
        for j in range(numberOfNodes):
            if (storage['nodes'][i] != '0')and(storage['nodes'][j] != '0'): #not counting ground node
                if( i==j): # main diagonal -> sum of conductance
                    for resistor in (storage['Resistors']):
                        if ((resistor['n+'] == storage['nodes'][i]) or (resistor['n-']== storage['nodes'][i])) :
                            matrix[i-1][j-1] += (1/resistor['value'])
                else: # inverse of the conductance connecting nodes i and j
                    for resistor in (storage['Resistors']):
                        if  ((resistor['n+']==storage['nodes'][i])and(resistor['n-']==storage['nodes'][j])) or ((resistor['n+']==storage['nodes'][j])and(resistor['n-']==storage['nodes'][i])):
                            matrix[i-1][j-1] -= (1/resistor['value'])
    return matrix



def setVoltageSourcesOnMainMatrix(storage,matrix):
    numberOfNodes = len(storage['nodes'])
    numberOfCurrentVars = len(storage['currentVars'])
    matrixDimension = (numberOfNodes-1) + (numberOfCurrentVars)
    for voltageSource in storage['VS']:
        positiveIndex = int(voltageSource['vo+'])- 1
        negativeIndex = int(voltageSource['vo-'])- 1

        for i in range(numberOfNodes-1,matrixDimension):
            if (storage['currentVars'][i-numberOfNodes+1][1:] == voltageSource['name']): #found index of associated current Var
                ### relationship with current variable and nodes
                if (positiveIndex>=0):
                    matrix[positiveIndex][i] = 1
                    matrix[i][positiveIndex] = -1
                if (negativeIndex>=0):
                    matrix[negativeIndex][i] = -1
                    matrix[i][negativeIndex] = 1
    return matrix   




def setVCCSOnMainMatrix(storage, matrix):
    for vccs in (storage['VCCS']):
        a = int(vccs['io+'])-1
        b = int(vccs['io-'])-1
        c = int(vccs['vi+'])-1
        d = int(vccs['vi-'])-1
        if (a >= 0) and (c>=0):
            matrix[a][c] += vccs['transconductance']
        if (a >= 0) and (d>=0):
            matrix[a][d] -= vccs['transconductance']
        if (b >= 0) and (c>=0):
            matrix[b][c] -= vccs['transconductance']
        if (b >= 0) and (d>=0):
            matrix[b][d] += vccs['transconductance']
    return matrix



def setVCVSOnMainMatrix(storage,matrix):
    numberOfNodes = len(storage['nodes'])
    numberOfCurrentVars = len(storage['currentVars'])
    matrixDimension = (numberOfNodes-1) + (numberOfCurrentVars)

    for vcvs in storage['VCVS']:
        positiveIndex = int(vcvs['vo+'])- 1
        negativeIndex = int(vcvs['vo-'])- 1
        positiveControlVoltageIndex = int(vcvs['vi+'])- 1
        negativeControlVoltageIndex = int(vcvs['vi-'])- 1

        for i in range(numberOfNodes-1,matrixDimension):
            if (storage['currentVars'][i-numberOfNodes+1][1:] == vcvs['name']): #found index of associated current Var
                ### relationship with current variable and nodes
                if (positiveIndex>=0):
                    matrix[positiveIndex][i] = 1
                    matrix[i][positiveIndex] = -1
                if (negativeIndex>=0):
                    matrix[negativeIndex][i] = -1
                    matrix[i][negativeIndex] = 1

                ### gain
                if(positiveControlVoltageIndex)>=0 :
                    matrix[i][positiveControlVoltageIndex] += vcvs['gain']
                if(negativeControlVoltageIndex)>=0 :
                    matrix[i][negativeControlVoltageIndex] -= vcvs['gain']
    return matrix



def setCCVSOnMainMatrix(storage,matrix):
    numberOfNodes = len(storage['nodes'])
    numberOfCurrentVars = len(storage['currentVars'])
    matrixDimension = (numberOfNodes-1) + (numberOfCurrentVars)
    for ccvs in (storage['CCVS']):
        positiveIndex = int(ccvs['vo+'])- 1  
        negativeIndex = int(ccvs['vo-'])- 1
        positiveControlCurrentIndex = int(ccvs['ii+'])- 1
        negativeControlCurrentIndex = int(ccvs['ii-'])- 1

        for i in range(numberOfNodes-1,matrixDimension):
            if (storage['currentVars'][i-numberOfNodes+1][2:] == ccvs['name']):
                ### 
                if (positiveControlCurrentIndex>=0):
                    matrix[positiveControlCurrentIndex][i] += 1
                    matrix[i][positiveControlCurrentIndex] -= 1
                if (negativeControlCurrentIndex>=0):
                    matrix[negativeControlCurrentIndex][i] -= 1
                    matrix[i][negativeControlCurrentIndex] += 1

            if (storage['currentVars'][i-numberOfNodes+1][1:] == ccvs['name']): #found index of associated current Var
                ### relationship with current variable and nodes
                if (positiveIndex>=0):
                    matrix[positiveIndex][i] += 1
                    matrix[i][positiveIndex] -= 1
                if (negativeIndex>=0):
                    matrix[negativeIndex][i] -= 1
                    matrix[i][negativeIndex] += 1

                ### transresistance
                matrix[i][i-1] += ccvs['transresistance']

    return matrix



def setCCCSOnMainMatrix(storage,matrix):
    numberOfNodes = len(storage['nodes'])
    numberOfCurrentVars = len(storage['currentVars'])
    matrixDimension = (numberOfNodes-1) + (numberOfCurrentVars)
    for cccs in storage['CCCS']:
        positiveIndex = int(cccs['io+'])- 1  
        negativeIndex = int(cccs['io-'])- 1
        positiveControlCurrentIndex = int(cccs['ii+'])- 1
        negativeControlCurrentIndex = int(cccs['ii-'])- 1
        for i in range(numberOfNodes-1,matrixDimension):
            if (storage['currentVars'][i-numberOfNodes+1][2:] == cccs['name']): #found index of associated current Var
                if (positiveIndex>=0):
                    matrix[positiveIndex][i] += int(cccs['gain'])
                if (negativeIndex>=0):
                    matrix[negativeIndex][i] -= int(cccs['gain'])
                
                if (positiveControlCurrentIndex>=0):
                    matrix[positiveControlCurrentIndex][i] += 1
                    matrix[i][positiveControlCurrentIndex] -= 1
                if (negativeControlCurrentIndex>=0):
                    matrix[negativeControlCurrentIndex][i] -= 1
                    matrix[i][negativeControlCurrentIndex] += 1
    return matrix



def setCapacitorsOnMainMatrix(storage,matrix):
    for capacitor in (storage['capacitors']):
        a = int(capacitor['n+']) - 1
        b = int(capacitor['n-']) - 1
        aux = 1j*complex((storage['freq']))*complex((capacitor['capacitance']))
        if (a>=0):
            matrix[a][a] += aux 
        if (b>=0):
            matrix[b][b] += aux
        if (a>=0) and (b>=0):
            matrix[a][b] -= aux
            matrix[b][a] -= aux
    return matrix

def setInductorsOnMainMatrix(storage,matrix):
    for inductor in (storage['inductors']):
        a = int(inductor['n+']) - 1
        b = int(inductor['n-']) - 1
       
        aux = 1/(1j*complex((storage['freq']))*complex((inductor['inductance'])))
        if (a>=0):
            matrix[a][a] += aux 
        if (b>=0):
            matrix[b][b] += aux
        if (a>=0) and (b>=0):
            matrix[a][b] -= aux
            matrix[b][a] -= aux

    return matrix
        

def setTransformersOnMainMatrix(storage,matrix):
    numberOfNodes = len(storage['nodes'])
    numberOfCurrentVars = len(storage['currentVars'])
    matrixDimension = (numberOfNodes-1) + (numberOfCurrentVars)

    for transformer in (storage['transformers']):
        a= int(transformer['n1+']) -1
        b= int(transformer['n1-']) -1
        c= int(transformer['n2+']) -1 
        d= int(transformer['n2-']) -1
        for i in range(numberOfNodes-1,matrixDimension):
            if (storage['currentVars'][i-numberOfNodes+1] == "j1"+transformer['name']): #found index of associated current Var 1 
                if(a>=0):
                    matrix[a][i]+= 1
                    matrix[i][a]-= 1
                if (b>=0):
                    matrix[b][i]-= 1
                    matrix[i][b]+= 1  
                index1 = i
            if (storage['currentVars'][i-numberOfNodes+1] == "j2"+transformer['name']): #found index of associated current Var 2
                if(c>=0):
                    matrix[c][i]+= 1
                    matrix[i][c]-= 1
                if (d>=0):
                    matrix[d][i]-= 1
                    matrix[i][d]+= 1  
                index2=i
        matrix[index1][index1] += 1j*complex(storage['freq'])*complex(transformer['inductance1'])
        matrix[index1][index2] += 1j*complex(storage['freq'])*complex(transformer['relation'])
        matrix[index2][index1] += 1j*complex(storage['freq'])*complex(transformer['relation'])
        matrix[index2][index2] += 1j*complex(storage['freq'])*complex(transformer['inductance2'])
    return matrix

def SetOpAmpOnMainMatrix(storage,matrix):
    numberOfNodes = len(storage['nodes'])
    numberOfCurrentVars = len(storage['currentVars'])
    matrixDimension = (numberOfNodes-1) + (numberOfCurrentVars)
    for opAmp in storage['OpAmps']:
        a= int(opAmp['vo1']) -1
        b= int(opAmp['vo2']) -1
        c= int(opAmp['vi1']) -1 
        d= int(opAmp['vi2']) -1
        for i in range(numberOfNodes-1,matrixDimension):
            if (storage['currentVars'][i-numberOfNodes+1] == "j"+opAmp['name']): #found index of associated current Var
                if(a>=0):
                    matrix[a][i] += 1
                if(b>=0):
                    matrix[b][i] -= 1
                if(c>=0):
                    matrix[i][c] += 1
                if(d>=0):
                    matrix[i][d] -= 1
    return matrix

#---------------------------------------------------------------------- Main Matrix 
def buildMainMatrix(storage):
    numberOfNodes = len(storage['nodes'])
    numberOfCurrentVars = len(storage['currentVars'])
    matrixDimension = (numberOfNodes-1) + (numberOfCurrentVars)
    if (storage['isOnsinusoidalSteadyState'] == False):
        matrix = np.zeros([matrixDimension, matrixDimension],dtype=float)
    elif (storage['isOnsinusoidalSteadyState'] == True):
        matrix = np.zeros([matrixDimension, matrixDimension],dtype=complex)
    matrix = setResistorsOnMainMatrix(storage,matrix)
    matrix = setVoltageSourcesOnMainMatrix(storage,matrix)   
    matrix = setVCCSOnMainMatrix(storage,matrix)
    matrix = setVCVSOnMainMatrix(storage,matrix)
    matrix = setCCVSOnMainMatrix(storage,matrix)
    matrix = setCCCSOnMainMatrix(storage,matrix)
    matrix = setCapacitorsOnMainMatrix(storage,matrix)
    matrix = setInductorsOnMainMatrix(storage,matrix)
    matrix = setTransformersOnMainMatrix(storage,matrix)
    matrix = SetOpAmpOnMainMatrix(storage,matrix)
    return matrix   

#---------------------------------------------------------------------- Matrix to be calculated
def buildSecondMatrix(storage):
    numberOfNodes = len(storage['nodes'])
    numberOfCurrentVars = len(storage['currentVars'])
    matrixDimension = (numberOfNodes-1) + (numberOfCurrentVars)
    matrix = np.empty([matrixDimension,1], dtype=object)
    for i in range(0,len(storage['nodes'])-1):
        matrix[i][0] = "e"+storage['nodes'][i+1]
    for i in range(len(storage['nodes'])-1,matrixDimension):
        matrix[i][0] = storage['currentVars'][i-len(storage['nodes'])+1]
    return matrix



#---------------------------------------------------------------------- Third Matrix
def buildthirdMatrix(storage):
    # building matrix
    numberOfNodes = len(storage['nodes'])
    numberOfCurrentVars = len(storage['currentVars'])
    matrixDimension = (numberOfNodes-1) + (numberOfCurrentVars)
    if (storage['isOnsinusoidalSteadyState'] == False):
        matrix = np.zeros([matrixDimension,1], dtype=float)
    elif (storage['isOnsinusoidalSteadyState'] == True):
        matrix = np.zeros([matrixDimension,1], dtype=complex)
    # setting current sources
    for i in range(0,len(storage['nodes'])-1):
        for currentSource in storage['CS']:
            if(currentSource['io+'] == storage['nodes'][i+1]):
                if(len(currentSource)==4):
                    matrix[i][0] -= currentSource['current']
                elif(len(currentSource)==9):
                    matrix[i][0] -= currentSource['continuousLevel']
                    matrix[i][0] -= cmath.rect(currentSource['amplitude'],math.radians(currentSource['TD']))
            elif(currentSource['io-'] == storage['nodes'][i+1]):
                if(len(currentSource)==4):
                    matrix[i][0] += currentSource['current']
                elif(len(currentSource)==9):
                    matrix[i][0] += currentSource['continuousLevel']
                    matrix[i][0] += cmath.rect(currentSource['amplitude'],math.radians(currentSource['TD']))
    # setting voltage sources
    for i in range(len(storage['nodes'])-1,matrixDimension):
        for voltageSource in storage['VS']:
            if(storage['currentVars'][i-len(storage['nodes'])+1][1:] == voltageSource['name']):
                if(len(voltageSource)==4):
                    matrix[i][0] -= voltageSource['voltage']
                elif(len(voltageSource)==9):
                    matrix[i][0] -= voltageSource['continuousLevel']
                    matrix[i][0] -= cmath.rect(voltageSource['amplitude'],math.radians(voltageSource['TD']))
    return matrix


#---------------------------------------------------------------------- Solving System
def solveSystem(Amatrix,XMatrix,BMatrix,storage):
    resultMatrix = np.linalg.solve(Amatrix,BMatrix)
    print("---------------------------")
    print(resultMatrix,"  =  ")
    print(XMatrix)
    print("--------------------------")
    file = open("results.txt", 'wt', encoding="utf-8")
    for i in range (len(XMatrix)):
        if (storage['isOnsinusoidalSteadyState'] == False):
            if (str(resultMatrix[i][0]) == '-0.0'):
                auxString = str(XMatrix[i][0]) + " = 0.0"
            else:
                auxString = str(XMatrix[i][0]) + " = " + str(resultMatrix[i][0])

        elif (storage['isOnsinusoidalSteadyState'] == True):
            result = cmath.polar(resultMatrix[i][0])
            if(math.degrees(result[1]) > 0):
                auxString = str(XMatrix[i][0]) + " = " + str(result[0])+" cos( "+ str(storage['freq'])+"t + "+str(math.degrees(result[1]))+" )"
            elif(math.degrees(result[1]) < 0):
                auxString = str(XMatrix[i][0]) + " = " + str(result[0])+" cos( "+ str(storage['freq'])+"t "+str(math.degrees(result[1]))+" )"
            elif(math.degrees(result[1])==0):
                auxString = str(XMatrix[i][0]) + " = " + str(result[0])+" cos( "+ str(storage['freq'])+"t )"
        
        file.write(auxString)

        # add V -> volts or A-> amperes
        if (XMatrix[i][0][0] == 'e' ):
            auxString = " V \n"
        elif (XMatrix[i][0][0] == 'j' ):
            auxString = " A \n"
        file.write(auxString)

    auxString = "\n \nResultado aproximado\n \n"
    file.write(auxString)
    for i in range (len(XMatrix)):
        if (storage['isOnsinusoidalSteadyState'] == False):
            if (str(round(resultMatrix[i][0],3)) == '-0.0'):
                auxString = str(XMatrix[i][0]) + " = 0.0"
            else:
                auxString = str(XMatrix[i][0]) + " = " + str(round(resultMatrix[i][0],3))
            file.write(auxString)

        elif (storage['isOnsinusoidalSteadyState'] == True):
            result = cmath.polar(resultMatrix[i][0])
            if(math.degrees(result[1]) > 0):
                auxString = str(XMatrix[i][0]) + " = " + str(round(result[0],3))+" cos( "+ str(storage['freq'])+"t + "+str(round(math.degrees(result[1]),3)) +"° )"
            elif(math.degrees(result[1]) < 0):
                auxString = str(XMatrix[i][0]) + " = " + str(round(result[0],3))+" cos( "+ str(storage['freq'])+"t "+str(round(math.degrees(result[1]),3))+"° )"
            elif(math.degrees(result[1])==0):
                auxString = str(XMatrix[i][0]) + " = " + str(round(result[0],3))+" cos( "+ str(storage['freq'])+"t )"
            
            file.write(auxString)
        
        # add V -> volts or A-> amperes
        if (XMatrix[i][0][0] == 'e' ):
            auxString = " V \n"
        elif (XMatrix[i][0][0] == 'j' ):
            auxString = " A \n"
        file.write(auxString)

    if (storage['isOnsinusoidalSteadyState'] == True):
        auxString = "\n \nOutro Formato\n \n"
        file.write(auxString)
        for i in range (len(XMatrix)):
            auxString = str(XMatrix[i][0]) + " = " + str(round((resultMatrix[i][0]).real,3)) +" cos( "+ str(storage['freq'])+"t )"
            file.write(auxString)
            if((resultMatrix[i][0]).imag) >= 0:
                auxString = " - " + str(round(abs((resultMatrix[i][0]).imag),3))+" sin( "+ str(storage['freq'])+"t )"
            else:
                auxString = " + " + str(round(abs((resultMatrix[i][0]).imag),3))+" sin( "+ str(storage['freq'])+"t )"
            file.write(auxString)
            # add V -> volts or A-> amperes
            if (XMatrix[i][0][0] == 'e' ):
                auxString = " V \n"
            elif (XMatrix[i][0][0] == 'j' ):
                auxString = " A \n"
            file.write(auxString)



    file.close()

