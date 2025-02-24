
#import numpy as np

from AriaQuanta.aqc.gatelibrary import X, Z, P, S, I, SWAP

from AriaQuanta._utils import np, swap_qubits, swap_qubits_density, is_unitary

#////////////////////////////////////////////////////////////////////////////////////
#------------------------------------------------------------------------------------
class GateControl:
    def __init__(self, name, base_matrix, control_qubits, target_qubits):

        # control_qubits: List of qubits that control the gate (now only one qubit)
        # target_qubits: List of target qubits on which the gate will be applied if controls are satisfied
        # base_gate: The gate to apply on the target qubits (e.g., X, H, etc.)

        #name = f"C{'C' * (len(control_qubits) - 1)}{base_gate.name}"

        self.name = name
        base_matrix = np.asarray(base_matrix)
        self.base_matrix = base_matrix

        control_qubits = [control_qubits]
        control_qubits = np.asarray(control_qubits, dtype=int).flatten()

        target_qubits = [target_qubits]
        target_qubits = np.asarray(target_qubits, dtype=int).flatten()

        self.control_qubits = control_qubits
        self.target_qubits = target_qubits

        qubits = np.concatenate((control_qubits, target_qubits))
        qubits = np.asarray(qubits, dtype=int).flatten()   
        self.qubits = qubits.tolist()
    
    def apply(self, num_of_qubits, multistate):

        base_matrix = self.base_matrix
        control_qubits = self.control_qubits
        target_qubits = self.target_qubits

        num_of_control_qubits = np.shape(control_qubits)[0]
        num_of_target_qubits = np.shape(target_qubits)[0]

        #-----------------------------------------------------
        # dim_of_controls = 2 * num_of_control_qubits # control_quibits is only 1 qubit at the moment (2 states)
        #dim_of_targets = np.shape(base_matrix)[0]
        #dim = 2 * dim_of_targets
        #control_matrix = np.identity(dim, dtype=complex) 

        #for k1 in range(dim_of_targets, dim):
        #    for k2 in range(dim_of_targets, dim):
        #        control_matrix[k1, k2] = base_matrix[k1 - dim_of_targets, k2 - dim_of_targets]
        control_matrix = self.matrix        
        #print("\ncontrol_matrix:", control_matrix)        

        #-----------------------------------------------------
        # update: corrected result for target_qubit=0
        # shift all the qubits to one ID higher, and increase the size of system to n+1
        one_state = np.array([[1], [0]], dtype=complex)
        multistate = np.kron(one_state,multistate)
        control_qubits = control_qubits + 1
        target_qubits = target_qubits + 1
        num_of_control_qubits = np.shape(control_qubits)[0]
        num_of_target_qubits = np.shape(target_qubits)[0]
        num_of_qubits += 1    

        #-----------------------------------------------------
        multistate_swaped = swap_qubits(0, control_qubits[0], num_of_qubits, multistate)

        for k1 in range(1, num_of_target_qubits+1):
            multistate_swaped = swap_qubits(k1, target_qubits[k1 - 1], num_of_qubits, multistate_swaped)

        if (num_of_qubits - num_of_control_qubits - num_of_target_qubits) > 0:
            dim = 2 ** (num_of_qubits - num_of_control_qubits - num_of_target_qubits)
            I2 = np.identity(dim, dtype=complex)
        else:
            I2 = 1  

        full_matrix = np.kron(control_matrix, I2)

        #if use_gpu_global:
        #    full_matrix = np.asnumpy(full_matrix)

        multistate_swaped = np.dot(full_matrix, multistate_swaped)

        for k1 in reversed(range(1, num_of_target_qubits+1)):
            multistate_swaped = swap_qubits(target_qubits[k1 - 1], k1, num_of_qubits, multistate_swaped)

        multistate = swap_qubits(control_qubits[0], 0, num_of_qubits, multistate_swaped)

        #-----------------------------------------------------
        #-----------------------------------------------------
        # update: corrected result for target_qubit=0
        # shift all the qubits to their original ID, and the size of system from n+1 to n
        multistate = multistate[:int(np.size(multistate)/2)]

        return multistate
    
    def apply_density(self, num_of_qubits, density_matrix):

        #base_matrix = self.base_matrix
        control_qubits = self.control_qubits
        target_qubits = self.target_qubits

        num_of_control_qubits = np.shape(control_qubits)[0]
        num_of_target_qubits = np.shape(target_qubits)[0]

        #-----------------------------------------------------
        # dim_of_controls = 2 * num_of_control_qubits # control_quibits is only 1 qubit at the moment (2 states)
        # dim_of_targets = np.shape(base_matrix)[0]
        # dim = 2 * dim_of_targets
        # control_matrix = np.identity(dim, dtype=complex) 

        # for k1 in range(dim_of_targets, dim):
        #    for k2 in range(dim_of_targets, dim):
        #        control_matrix[k1, k2] = base_matrix[k1 - dim_of_targets, k2 - dim_of_targets]
        control_matrix = self.matrix
        #-----------------------------------------------------

        density_matrix_swaped = swap_qubits_density(0, control_qubits[0], num_of_qubits, density_matrix)

        for k1 in range(1, num_of_target_qubits+1):
            density_matrix_swaped = swap_qubits_density(k1, target_qubits[k1 - 1], num_of_qubits, density_matrix_swaped)

        if (num_of_qubits - num_of_control_qubits - num_of_target_qubits) > 0:
            dim = 2 ** (num_of_qubits - num_of_control_qubits - num_of_target_qubits)
            I2 = np.identity(dim, dtype=complex)
        else:
            I2 = 1  

        full_matrix = np.kron(control_matrix, I2)

        #if use_gpu_global:
        #    full_matrix = np.asnumpy(full_matrix)

        density_matrix_swaped = full_matrix @ density_matrix_swaped @ np.conj(full_matrix.T)

        for k1 in reversed(range(1, num_of_target_qubits+1)):
            density_matrix_swaped = swap_qubits_density(target_qubits[k1 - 1], k1, num_of_qubits, density_matrix_swaped)

        density_matrix = swap_qubits_density(control_qubits[0], 0, num_of_qubits, density_matrix_swaped)

        return density_matrix 

#////////////////////////////////////////////////////////////////////////////////////                

#------------------------------------------------------------------------------------
class CX(GateControl):
    def __init__(self, control_qubits=0, target_qubits=1): 
        #matrix_qiskit = np.array([[1, 0, 0, 0],
        #          [0, 0, 0, 1],
        #          [0, 0, 1, 0],
        #          [0, 1, 0, 0]])
        matrix_books = np.array([[1, 0, 0, 0],
                  [0, 1, 0, 0],
                  [0, 0, 0, 1],
                  [0, 0, 1, 0]])       
        #self.control_matrix = matrix_books
        self.matrix = matrix_books        
        super().__init__(name='CX', base_matrix=X().matrix, control_qubits=control_qubits, target_qubits=target_qubits) 

#------------------------------------------------------------------------------------
class CZ(GateControl):
    def __init__(self, control_qubits=0, target_qubits=1): 
        matrix = np.array([[1, 0, 0, 0],
                  [0, 1, 0, 0],
                  [0, 0, 1, 0],
                  [0, 0, 0, -1]])
        self.matrix = matrix          
        super().__init__(name='CZ', base_matrix=Z().matrix, control_qubits=control_qubits, target_qubits=target_qubits)  

#------------------------------------------------------------------------------------
class CP(GateControl):
    def __init__(self, phi, control_qubits=0, target_qubits=1): 
        self.phi = phi 
        this_matrix = P(phi).matrix
        matrix = np.array([[1, 0, 0, 0],
                  [0, 1, 0, 0],
                  [0, 0, 1, 0],
                  [0, 0, 0, np.exp(1j * phi)]])
        self.matrix = matrix         
        super().__init__(name='CP', base_matrix=this_matrix, control_qubits=control_qubits, target_qubits=target_qubits)

#------------------------------------------------------------------------------------
class CS(GateControl):
    def __init__(self, control_qubits=0, target_qubits=1): 
        matrix = np.array([[1, 0, 0, 0],
                  [0, 1, 0, 0],
                  [0, 0, 1, 0],
                  [0, 0, 0, 1j]])
        self.matrix = matrix         
        super().__init__(name='CS', base_matrix=S().matrix, control_qubits=control_qubits, target_qubits=target_qubits)
#------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------
class CSX(GateControl):
    def __init__(self, control_qubits=0, target_qubits=1): 
        this_matrix = [[np.exp(+1j * np.pi / 4), np.exp(-1j * np.pi / 4)], 
                       [np.exp(-1j * np.pi / 4), np.exp(+1j * np.pi / 4)]]
        matrix = [[1, 0, 0, 0],
                  [0, 1, 0, 0],
                  [0, 0, (1 + 1j)/2, (1 - 1j)/2],
                  [0, 0, (1 - 1j)/2, (1 + 1j)/2]] 
        self.matrix = matrix          
        super().__init__(name='CSX', base_matrix=this_matrix, control_qubits=control_qubits, target_qubits=target_qubits)             

#------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------
# Toffoli, controlled-controlled NOT
class CCX(GateControl):
    def __init__(self, qubits_1=0, qubits_2=1, qubits_3=2):
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

        controls = [qubits_1]
        targets = sorted([qubits_2, qubits_3])
        self.matrix = matrix
        super().__init__(name='CCX', base_matrix=CX().matrix, control_qubits=controls, target_qubits=targets)   

#------------------------------------------------------------------------------------
# Fredkin, controlled swap
class CSWAP(GateControl):
    def __init__(self, qubits_1=0, qubits_2=1, qubits_3=2):
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

        controls = [qubits_1]
        targets = sorted([qubits_2, qubits_3])
        self.matrix = matrix
        super().__init__(name='CSWAP', base_matrix=SWAP().matrix, control_qubits=controls, target_qubits=targets)                   

#------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------
# Control with an arbitray matrix - defined by the user
class CU(GateControl):
    def __init__(self, base_matrix, control_qubits=0, target_qubits=1):
        self.base_matrix=base_matrix                
        CU.namedraw='CU'
        if is_unitary(base_matrix) == False:
            raise('Custom matrix is not unitary')
        
        num_of_I_matrices = int(np.log2(base_matrix.shape[0]))
        zero = np.array([[1], [0]])
        one = np.array([[0], [1]])
        zero_zero = np.kron(zero, zero.T)
        one_one = np.kron(one, one.T)
        I_matrix = I().matrix
        
        # based on books (and not qiskit)
        # ∣0⟩⟨0∣⊗I+∣1⟩⟨1∣⊗G
        cmatrix_1 = np.kron(zero_zero, I_matrix)
        for i in range(num_of_I_matrices-1):
            cmatrix_1 = np.kron(cmatrix_1, I_matrix)

        cmatrix_2 = np.kron(one_one, base_matrix)

        controlled_matrix = cmatrix_1 + cmatrix_2

        self.matrix = controlled_matrix
    
        super().__init__(name='CU', base_matrix=base_matrix, control_qubits=control_qubits, target_qubits=target_qubits)                  
