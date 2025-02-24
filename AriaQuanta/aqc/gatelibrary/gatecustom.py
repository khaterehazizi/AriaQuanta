
#import numpy as np
from AriaQuanta._utils import np, swap_qubits, swap_qubits_density, is_unitary
from AriaQuanta.aqc.gatelibrary import I

#////////////////////////////////////////////////////////////////////////////////////
#------------------------------------------------------------------------------------
class GateCustom:
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

        #-----------------------------------------------------
        # update: corrected result for target_qubit=0
        # shift all the qubits to one ID higher, and increase the size of system to n+1
        one_state = np.array([[1], [0]], dtype=complex)
        multistate = np.kron(one_state,multistate)
        target_qubits = target_qubits + 1
        num_of_target_qubits = np.shape(target_qubits)[0]
        num_of_qubits += 1 

        multistate_swaped = multistate
        for k1 in range(0, num_of_target_qubits):
            multistate_swaped = swap_qubits(k1, target_qubits[k1], num_of_qubits, multistate_swaped)

        if (num_of_qubits - num_of_target_qubits) > 0:
            dim = 2 ** (num_of_qubits - num_of_target_qubits)
            I2 = np.identity(dim, dtype=complex)
        else:
            I2 = 1         
    
        full_matrix = np.kron(matrix, I2)
        
        multistate_swaped = np.dot(full_matrix, multistate_swaped)

        for k1 in reversed(range(0, num_of_target_qubits)):
            multistate_swaped = swap_qubits(target_qubits[k1], k1, num_of_qubits, multistate_swaped)

        multistate = multistate_swaped

        #-----------------------------------------------------
        #-----------------------------------------------------
        # update: corrected result for target_qubit=0
        # shift all the qubits to their original ID, and the size of system from n+1 to n
        multistate = multistate[:int(np.size(multistate)/2)]
        
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
class Custom(GateCustom):
    def __init__(self, matrix=I().matrix, target_qubits=0):
        this_matrix = matrix
        if is_unitary(this_matrix) == False:
            raise('Custom matrix is not unitary')    
        super().__init__(name='Custom', matrix=matrix, target_qubits=target_qubits)  
               
