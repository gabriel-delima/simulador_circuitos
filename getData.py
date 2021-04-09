"""
appendNewNode -> simple auxiliar function to add(if it's a new one) a node to the storage
"""
def appendNewNode(storage, node):
    if (node not in storage['nodes']):
            storage['nodes'].append(node)
    return storage

"""
sortNodes-> sorts nodes for later use
"""
def sortNodes(storage):
    nodesAux = storage['nodes']
    for i in range(len(nodesAux)):
        nodesAux[i] = int(nodesAux[i])
    nodesAux.sort()
    for i in range(len(nodesAux)):
        nodesAux[i] = str(nodesAux[i])
        storage['nodes'][i] = nodesAux[i]
    return storage

""" 
getComponentValues -> Organize the properties of the components of each line in the appropriate space in "storage"
"""
def getComponentValues(component,storage):
    ###################################################################### Time Invariant
    # Resistor
    if ((component[0][0]) == "R"):
        aux = {}
        aux['name'] = component[0]
        aux['n+'] = component[1]
        storage = appendNewNode(storage, component[1])
        aux['n-'] = component[2]
        storage = appendNewNode(storage, component[2])
        aux['value'] = float(component[3])
        storage['Resistors'].append(aux)
    # Voltage Controlled Current Source
    elif ((component[0][0]) == "G"):
        aux = {}
        aux['name'] = component[0]
        aux['io+'] = component[1]
        storage = appendNewNode(storage, component[1])
        aux['io-'] = component[2]
        storage = appendNewNode(storage, component[2])
        aux['vi+'] = component[3]
        storage = appendNewNode(storage, component[3])
        aux['vi-'] = component[4]
        storage = appendNewNode(storage, component[4])
        aux['transconductance'] = float(component[5])
        storage['VCCS'].append(aux)
    # Voltage Controlled Voltage Source
    elif ((component[0][0]) == "E"):
        aux = {}
        aux['name'] = component[0]
        storage['currentVars'].append('j'+ component[0])
        aux['vo+'] = component[1]
        storage = appendNewNode(storage, component[1])
        aux['vo-'] = component[2]
        storage = appendNewNode(storage, component[2])
        aux['vi+'] = component[3]
        storage = appendNewNode(storage, component[3])
        aux['vi-'] = component[4]
        storage = appendNewNode(storage, component[4])
        aux['gain'] = float(component[5])
        storage['VCVS'].append(aux)
    # Current Controlled Current Source
    elif ((component[0][0]) == "F"):
        aux = {}
        aux['name'] = component[0]
        storage['currentVars'].append('jx'+ component[0])
        aux['io+'] = component[1]
        storage = appendNewNode(storage, component[1])
        aux['io-'] = component[2]
        storage = appendNewNode(storage, component[2]) 
        aux['ii+'] = component[3]
        storage = appendNewNode(storage, component[3])
        aux['ii-'] = component[4]
        storage = appendNewNode(storage, component[4])
        aux['gain'] = float(component[5])
        storage['CCCS'].append(aux)
    # Current Controlled Current Source
    elif ((component[0][0]) == "H"):
        aux = {}
        aux['name'] = component[0]
        storage['currentVars'].append('jx'+ component[0])
        storage['currentVars'].append('j'+ component[0])
        aux['vo+'] = component[1]
        storage = appendNewNode(storage, component[1])
        aux['vo-'] = component[2]
        storage = appendNewNode(storage, component[2])
        aux['ii+'] = component[3]
        storage = appendNewNode(storage, component[3])
        aux['ii-'] = component[4]
        storage = appendNewNode(storage, component[4])
        aux['transresistance'] = float(component[5])
        storage['CCVS'].append(aux)
    # Operational Amplifier
    elif ((component[0][0]) == "O"):
        aux = {}
        aux['name'] = component[0]
        storage['currentVars'].append('j'+ component[0])
        aux['vo1'] = component[1]
        storage = appendNewNode(storage, component[1])
        aux['vo2'] = component[2]
        storage = appendNewNode(storage, component[2])
        aux['vi1'] = component[3]
        storage = appendNewNode(storage, component[3])
        aux['vi2'] = component[4]
        storage = appendNewNode(storage, component[4])
        storage['OpAmps'].append(aux)
    # Current Source
    elif ((component[0][0] == "I") and ((component[3] == "DC") or (component[3] == "dc"))):
        aux = {}
        aux['name'] = component[0]
        aux['io+'] = component[1]
        storage = appendNewNode(storage, component[1])
        aux['io-'] = component[2]
        storage = appendNewNode(storage, component[2])
        aux['current'] = float(component[4])
        storage['CS'].append(aux)
    # Voltage Source
    elif ((component[0][0] == "V") and ((component[3] == "DC") or (component[3] == "dc")) ):
        aux = {}
        aux['name'] = component[0]
        storage['currentVars'].append('j'+ component[0])
        aux['vo+'] = component[1]
        storage = appendNewNode(storage, component[1])
        aux['vo-'] = component[2]
        storage = appendNewNode(storage, component[2])
        aux['voltage'] = float(component[4])
        storage['VS'].append(aux)
    ###################################################################### Time domain
    # Sinusoidal Current Source
    elif ((component[0][0] == "I") and ((component[3] == "SIN") or (component[3] == "sin") or (component[3] == "Sin")) ):
        aux = {}
        aux['name'] = component[0]
        aux['io+'] = component[1]
        storage = appendNewNode(storage, component[1])
        aux['io-'] = component[2]
        storage = appendNewNode(storage, component[2])
        aux['continuousLevel'] = float(component[4])
        aux['amplitude'] = float(component[5])
        aux['FREQ'] = float(component[6])
        storage['freq'] = float(component[6])
        storage['isOnsinusoidalSteadyState'] = True
        aux['TD'] = float(component[7])
        aux['THETA'] = float(component[8])
        aux['PHASE'] = float(component[9])
        storage['CS'].append(aux)
    # Sinusoidal Voltage Source
    elif ((component[0][0] == "V") and ((component[3] == "SIN") or (component[3] == "sin") or (component[3] == "Sin")) ):
        aux = {}
        aux['name'] = component[0]
        storage['currentVars']. append('j'+ component[0])
        aux['vo+'] = component[1]
        storage = appendNewNode(storage, component[1])
        aux['vo-'] = component[2]
        storage = appendNewNode(storage, component[2])
        aux['continuousLevel'] = float(component[4])
        aux['amplitude'] = float(component[5])
        aux['FREQ'] = float(component[6])
        storage['freq'] = float(component[6])
        storage['isOnsinusoidalSteadyState'] = True
        aux['TD'] = float(component[7])
        aux['THETA'] = float(component[8])
        aux['PHASE'] = float(component[9])            
        storage['VS'].append(aux)
    # Capacitor
    elif ((component[0][0]) == "C"):
        aux = {}
        aux['name'] = component[0]
        aux['n+'] = component[1]
        storage = appendNewNode(storage, component[1])
        aux['n-'] = component[2]
        storage = appendNewNode(storage, component[2])
        aux['capacitance'] = component[3]
        #optional
        if (len(component) == 5):
            aux['InitialVoltage'] = component[4]
        storage['capacitors'].append(aux)
    # Inductor 
    elif ((component[0][0]) == "L"):
        aux = {}
        aux['name'] = component[0]
        #storage['currentVars'].append('j'+ component[0])
        aux['n+'] = component[1]
        storage = appendNewNode(storage, component[1])
        aux['n-'] = component[2]
        storage = appendNewNode(storage, component[2])
        aux['inductance'] = component[3]
        #optional
        if (len(component) == 5):
            aux['initialCurrent'] = component[4]
        storage['inductors'].append(aux)
    # Transformer
    elif ((component[0][0]) == "K"):
        aux = {}
        aux['name'] = component[0]
        storage['currentVars']. append('j1'+ component[0])
        storage['currentVars']. append('j2'+ component[0]) 
        aux['n1+'] = component[1]
        storage = appendNewNode(storage, component[1])
        aux['n1-'] = component[2]
        storage = appendNewNode(storage, component[2])
        aux['inductance1'] = component[3]
        aux['n2+'] = component[4]
        storage = appendNewNode(storage, component[4])
        aux['n2-'] = component[5]
        storage = appendNewNode(storage, component[5])
        aux['inductance2'] = component[6]
        aux['relation'] = component[7]
        storage['transformers'].append(aux)
    return storage
    
"""
setComponentsInStorage -> Creates and completes the dictionary that will store all the data, 
                            it was designed to work similar to a json
"""     
def setComponentsInStorage():
    storage = { 'Resistors': [], 
                'VCCS':[], 
                'VCVS':[], 
                'CCCS':[], 
                'CCVS':[], 
                'CS':[], 
                'VS':[], 
                'OpAmps':[],
                'nodes': [],  
                'currentVars': [],
                'capacitors': [],
                'inductors': [],
                'transformers':[],
                'isOnsinusoidalSteadyState': False,
                'freq': 0 
            }
    file = open('data.txt' , 'rt')
    for line in file:
        if (line!=" ") and (line!="\n") and (line!=""):
            line = line.strip()
            component = line.split(" ")      
            storage = getComponentValues(component,storage)
    file.close()
    storage = sortNodes(storage)
    ###################################################################### DEBUG
    print("storage = ", storage)
    return storage