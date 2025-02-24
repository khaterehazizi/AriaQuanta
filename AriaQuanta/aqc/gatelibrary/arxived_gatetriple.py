
#import numpy as np
from AriaQuanta._utils import np, swap_qubits, swap_qubits_density, is_unitary, reorder_state
from AriaQuanta.aqc.gatelibrary import I

#////////////////////////////////////////////////////////////////////////////////////
#------------------------------------------------------------------------------------
class GateTripleQubit():
    def __init__(self, name, matrix, target_qubits):

        # control_qubits: List of qubits that control the gate (now only one qubit)
        # target_qubits: List of target qubits on which the gate will be applied if controls are satisfied
        # base_gate: The gate to apply on the target qubits (e.g., X, H, etc.)

        #name = f"C{'C' * (len(control_qubits) - 1)}{base_gate.name}"

        self.name = name
        matrix = np.asarray(matrix)
        self.matrix = matrix

        target_qubits = [target_qubits]
        target_qubits = np.asarray(target_qubits, dtype=int).flatten()
        self.target_qubits = target_qubits

        self.qubits = target_qubits.tolist()

    def apply(self, num_of_qubits, multistate):
        
        target_qubits = self.target_qubits
        matrix = self.matrix
        
        #-----------------------------------------------------
        num_of_target_qubits = np.shape(target_qubits)[0]

        multistate_swaped = multistate
        for k1 in range(0, num_of_target_qubits):
            multistate_swaped = swap_qubits(k1, target_qubits[k1], num_of_qubits, multistate_swaped)

        #for k1 in reversed(range(num_of_target_qubits, num_of_qubits)):
        #    multistate_swaped = swap_qubits(k1, target_qubits[k1], num_of_qubits, multistate_swaped)

        if (num_of_qubits - num_of_target_qubits) > 0:
            dim = 2 ** (num_of_qubits - num_of_target_qubits)
            I2 = np.identity(dim, dtype=complex)
        else:
            I2 = 1         
    
        full_matrix = np.kron(matrix, I2)

        # reverse ordering as used by Qiskit
        #full_matrix = np.kron(I2, matrix)

        multistate_swaped = np.dot(full_matrix, multistate_swaped)

        for k1 in reversed(range(0, num_of_target_qubits)):
            multistate_swaped = swap_qubits(target_qubits[k1], k1, num_of_qubits, multistate_swaped)
        #for k1 in range(num_of_target_qubits, num_of_target_qubits):
        #    multistate_swaped = swap_qubits(target_qubits[k1], k1, num_of_qubits, multistate_swaped)


        multistate = multistate_swaped

        # because matrices are based on qiskit:
        #multistate = reorder_state(multistate)

        return multistate


    def apply_density(self, num_of_qubits, density_matrix):
        
        target_qubits = self.target_qubits
        matrix = self.matrix
        
        #-----------------------------------------------------
        num_of_target_qubits = np.shape(target_qubits)[0]

        density_matrix_swaped = density_matrix
        for k1 in range(0, num_of_target_qubits):
            density_matrix_swaped = swap_qubits_density(k1, target_qubits[k1], num_of_qubits, density_matrix_swaped)

        if (num_of_qubits - num_of_target_qubits) > 0:
            dim = 2 ** (num_of_qubits - num_of_target_qubits)
            I2 = np.identity(dim, dtype=complex)
        else:
            I2 = 1         
    
        full_matrix = np.kron(matrix, I2)
        
        density_matrix_swaped = full_matrix @ density_matrix_swaped @ np.conj(full_matrix.T)

        for k1 in reversed(range(0, num_of_target_qubits)):
            density_matrix_swaped = swap_qubits_density(target_qubits[k1], k1, num_of_qubits, density_matrix_swaped)

        density_matrix = density_matrix_swaped

        return density_matrix
        
#------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------

#------------------------------------------------------------------------------------
# Toffoli, controlled-controlled NOT
class CCXold(GateTripleQubit):
    def __init__(self, target_qubits_1=0, target_qubits_2=1, target_qubits_3=2):
        matrix = np.eye(8)

        #------------------------
        # based on q0 as control
        # Qiskit representation
        #matrix[3,7] = 1
        #matrix[7,3] = 1
        #matrix[3,3] = 0
        #matrix[7,7] = 0 
        
        #------------------------
        matrix[6,7] = 1
        matrix[7,6] = 1
        matrix[6,6] = 0
        matrix[7,7] = 0     

        controls = sorted([target_qubits_1, target_qubits_2])
        targets = [target_qubits_3]
        target_qubits = controls + targets
        self.matrix = matrix
        super().__init__(name='CCX', matrix=matrix, target_qubits=target_qubits)

#------------------------------------------------------------------------------------
# Margolus, simplified Toffoli
#class RCCXold(GateTripleQubit):
#    def __init__(self, target_qubits_1=0, target_qubits_2=1, target_qubits_3=2):
#
#        matrix = np.eye(8, dtype=complex)
#
#        #------------------------       
#        # based on q0 as control
#        # Qiskit representation
#        #matrix[3,7] = -1j
#        #matrix[3,3] = 0
#        #matrix[5,5] = -1
#        #matrix[7,7] = 0 
#
#        #------------------------
#        matrix[6,7] = -1j/np.sqrt(2)
#        matrix[7,6] = -1j/np.sqrt(2)
#        matrix[6,6] = 1/np.sqrt(2)
#        matrix[7,7] = 1/np.sqrt(2)
#
#        target_qubits = [target_qubits_1, target_qubits_2, target_qubits_3]
#
#        self.matrix=matrix
#        super().__init__(name='RCCX', matrix=matrix, target_qubits=target_qubits)   

#------------------------------------------------------------------------------------
# Fredkin, controlled swap
class CSWAPold(GateTripleQubit):
    def __init__(self, target_qubits_1=0, target_qubits_2=1, target_qubits_3=2):
        matrix = np.eye(8)

        #------------------------
        # based on q0 as control
        # Qiskit representation        
        #matrix[3,3] = 0
        #matrix[5,5] = 0
        #matrix[3,5] = 1
        #matrix[5,3] = 1

        #------------------------
        matrix[5,6] = 1
        matrix[6,5] = 1
        matrix[5,5] = 0
        matrix[6,6] = 0

        controls = [target_qubits_1]
        targets = sorted([target_qubits_2, target_qubits_3])
        target_qubits = controls + targets
        self.matrix = matrix
        super().__init__(name='CSWAP', matrix=matrix, target_qubits=target_qubits)  

