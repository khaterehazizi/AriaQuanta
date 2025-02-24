
#import numpy as np
from AriaQuanta._utils import np

class Qubit:
    def __init__(self, name='', state=np.array([[1], [0]])):
        self.state = state
        self.name = name

class MultiQubit:
    def __init__(self, num_of_qubits, list_of_qubits=[]):  # num_of_qubit, multistate, qubits

        qubits = [] 
 
        if list_of_qubits == []:
            qubit_0 = Qubit()
        else:
            qubit_0 = list_of_qubits[0]

        qubits.append(qubit_0)
        multistate = qubit_0.state            

        for i in range(1, num_of_qubits):

            if list_of_qubits == []:
                qubit_i = Qubit()
            else:
                qubit_i = list_of_qubits[i]

            state_i = qubit_i.state
            qubits.append(qubit_i)
            multistate = np.kron(multistate, state_i)

        MultiQubit.num_of_qubits = num_of_qubits    
        MultiQubit.multistate = multistate
        MultiQubit.qubits = qubits

def create_state(name, a):
    zero = np.array([[1], [0]])
    one = np.array([[0], [1]])
    b = np.sqrt(1-a**2)

    state = a*zero + b*one

    qubit = Qubit(name, state)
    return qubit       