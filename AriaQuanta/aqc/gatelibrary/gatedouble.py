
#import numpy as np
from AriaQuanta._utils import np, swap_qubits, swap_qubits_density, is_unitary

#////////////////////////////////////////////////////////////////////////////////////
#------------------------------------------------------------------------------------
class GateDoubleQubit:
    def __init__(self, name, matrix, target_qubits):
        
        self.name = name
        matrix = np.asarray(matrix)
        self.matrix = matrix

        target_qubits = [target_qubits]
        target_qubits = np.asarray(target_qubits, dtype=int).flatten()
        self.target_qubits = target_qubits
    
        self.qubits = target_qubits.tolist()
        
    #----------------------------------------------
    def apply(self, num_of_qubits, multistate):
        
        target_qubits = self.target_qubits
        matrix = self.matrix

        multistate_swaped = swap_qubits(0, target_qubits[0], num_of_qubits, multistate)
        multistate_swaped = swap_qubits(1, target_qubits[1], num_of_qubits, multistate_swaped)  # it was multistate- is that correct?

        if (num_of_qubits - len(target_qubits)) > 0:
            dim = 2 ** (num_of_qubits - len(target_qubits))
            I2 = np.identity(dim, dtype=complex)
        else:
            I2 = 1         
    
        full_matrix = np.kron(matrix, I2)       
        # reverse ordering as used by Qiskit
        #full_matrix = np.kron(I2, matrix)

        multistate_swaped = np.dot(full_matrix, multistate_swaped)

        multistate_swaped = swap_qubits(target_qubits[1], 1, num_of_qubits, multistate_swaped)
        multistate = swap_qubits(target_qubits[0], 0, num_of_qubits, multistate_swaped)

        return multistate
    
    def apply_density(self, num_of_qubits, density_matrix):
        
        target_qubits = self.target_qubits
        matrix = self.matrix

        density_matrix_swaped = swap_qubits_density(0, target_qubits[0], num_of_qubits, density_matrix)
        density_matrix_swaped = swap_qubits_density(1, target_qubits[1], num_of_qubits, density_matrix_swaped)

        if (num_of_qubits - len(target_qubits)) > 0:
            dim = 2 ** (num_of_qubits - len(target_qubits))
            I2 = np.identity(dim, dtype=complex)
        else:
            I2 = 1         
    
        full_matrix = np.kron(matrix, I2)
        
        density_matrix_swaped = full_matrix @ density_matrix_swaped @ np.conj(full_matrix.T)

        density_matrix_swaped = swap_qubits_density(target_qubits[1], 1, num_of_qubits, density_matrix_swaped)
        density_matrix = swap_qubits_density(target_qubits[0], 0, num_of_qubits, density_matrix_swaped)

        return density_matrix
    
#////////////////////////////////////////////////////////////////////////////////////
#///////// 2-Qubit Gates /////////
#------------------------------------------------------------------------------------
class SWAP(GateDoubleQubit):
    def __init__(self, target_qubits_1=0, target_qubits_2=1):
        matrix = [[1, 0, 0, 0],
                  [0, 0, 1, 0],
                  [0, 1, 0, 0],
                  [0, 0, 0, 1]]
        target_qubits = [target_qubits_1, target_qubits_2]
        target_qubits = sorted(target_qubits)
        super().__init__(name='SWAP', matrix=matrix, target_qubits=target_qubits)  

#------------------------------------------------------------------------------------
class ISWAP(GateDoubleQubit):
    def __init__(self, target_qubits_1=0, target_qubits_2=1):
        matrix = [[1, 0, 0, 0],
                  [0, 0, +1j, 0],
                  [0, +1j, 0, 0],
                  [0, 0, 0, 1]]
        target_qubits = [target_qubits_1, target_qubits_2]   
        target_qubits = sorted(target_qubits)
        super().__init__(name='ISWAP', matrix=matrix, target_qubits=target_qubits) 

#------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------
class SWAPsqrt(GateDoubleQubit):
    def __init__(self, target_qubits_1=0, target_qubits_2=1):
        matrix = [[1, 0, 0, 0],
                  [0, 1 / 2 * (1 + 1j), 1 / 2 * (1 - 1j), 0],
                  [0, 1 / 2 * (1 - 1j), 1 / 2 * (1 + 1j), 0],
                  [0, 0, 0, 1]]
        target_qubits = [target_qubits_1, target_qubits_2] 
        target_qubits = sorted(target_qubits)
        super().__init__(name='SWAPsqrt', matrix=matrix, target_qubits=target_qubits)

#------------------------------------------------------------------------------------
#class ISWAPsqrt(GateDoubleQubit):
#    def __init__(self, target_qubits_1=0, target_qubits_2=1):
#        matrix = [[1, 0, 0, 0],
#                  [0, 1 / np.sqrt(2), +1j / np.sqrt(2), 0],
#                  [0, +1j / np.sqrt(2), 1 / np.sqrt(2), 0],
#                  [0, 0, 0, 1]]
#        target_qubits = [target_qubits_1, target_qubits_2] 
#        target_qubits = sorted(target_qubits)
#        super().__init__(name='ISWAPsqrt', matrix=matrix, target_qubits=target_qubits)

#------------------------------------------------------------------------------------
class SWAPalpha(GateDoubleQubit):
    def __init__(self, alpha, target_qubits_1=0, target_qubits_2=1):
        self.alpha = alpha
        matrix = [[1, 0, 0, 0],
                  [0, 1 / 2 * (1 + np.exp(+1j * np.pi * alpha)), 1 / 2 * (1 - np.exp(+1j * np.pi * alpha)), 0],
                  [0, 1 / 2 * (1 - np.exp(+1j * np.pi * alpha)), 1 / 2 * (1 + np.exp(+1j * np.pi * alpha)), 0],
                  [0, 0, 0, 1]]
        target_qubits = [target_qubits_1, target_qubits_2] 
        target_qubits = sorted(target_qubits)
        super().__init__(name='SWAPalpha', matrix=matrix, target_qubits=target_qubits)  

#------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------
class RXX(GateDoubleQubit):
    def __init__(self, phi, target_qubits_1=0, target_qubits_2=1):
        self.phi = phi
        matrix = [[np.cos(phi / 2), 0, 0, -1j * np.sin(phi / 2)],
                  [0, np.cos(phi / 2), -1j * np.sin(phi / 2), 0],
                  [0, -1j * np.sin(phi / 2), np.cos(phi / 2), 0],
                  [-1j * np.sin(phi / 2), 0, 0, np.cos(phi / 2)]]
        target_qubits = [target_qubits_1, target_qubits_2] 
        target_qubits = sorted(target_qubits)
        super().__init__(name='RXX', matrix=matrix, target_qubits=target_qubits) 

#------------------------------------------------------------------------------------
class RYY(GateDoubleQubit):
    def __init__(self, phi, target_qubits_1=0, target_qubits_2=1):
        self.phi = phi
        matrix = [[np.cos(phi / 2), 0, 0, +1j * np.sin(phi / 2)],
                  [0, np.cos(phi / 2), -1j * np.sin(phi / 2), 0],
                  [0, -1j * np.sin(phi / 2), np.cos(phi / 2), 0],
                  [+1j * np.sin(phi / 2), 0, 0, np.cos(phi / 2)]]
        target_qubits = [target_qubits_1, target_qubits_2] 
        target_qubits = sorted(target_qubits)
        super().__init__(name='RYY', matrix=matrix, target_qubits=target_qubits)   

#------------------------------------------------------------------------------------
class RZZ(GateDoubleQubit):
    def __init__(self, phi, target_qubits_1=0, target_qubits_2=1):
        self.phi = phi
        matrix = [[np.exp(-1j * phi / 2), 0, 0, 0],
                  [0, np.exp(+1j * phi / 2), 0, 0],
                  [0, 0, np.exp(+1j * phi / 2), 0],
                  [0, 0, 0, np.exp(-1j * phi / 2)]]
        target_qubits = [target_qubits_1, target_qubits_2]
        target_qubits = sorted(target_qubits)
        super().__init__(name='RZZ', matrix=matrix, target_qubits=target_qubits) 
        
#------------------------------------------------------------------------------------
class RXY(GateDoubleQubit):
    def __init__(self, phi, target_qubits_1=0, target_qubits_2=1):
        self.phi = phi
        matrix = [[1, 0, 0, 0],
                  [0, np.cos(phi / 2), -1j * np.sin(phi / 2), 0],
                  [0, -1j * np.sin(phi / 2), np.cos(phi / 2), 0],
                  [0, 0, 0, 1]]
        target_qubits = [target_qubits_1, target_qubits_2] 
        target_qubits = sorted(target_qubits)
        super().__init__(name='RXY', matrix=matrix, target_qubits=target_qubits) 

#------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------
class Barenco(GateDoubleQubit):
    def __init__(self, alpha, phi, theta, target_qubits_1=0, target_qubits_2=1):
        self.alpha = alpha
        self.phi = phi
        self.theta = theta
        matrix = [[1, 0, 0, 0],
                  [0, 1, 0, 0],
                  [0, 0, np.exp(+1j * alpha) * np.cos(theta), -1j * np.exp(+1j * (alpha - phi)) * np.sin(theta)],
                  [0, 0, -1j * np.exp(+1j * (alpha + phi)) * np.sin(theta), np.exp(+1j * alpha) * np.cos(theta)]
                  ]
        target_qubits = [target_qubits_1, target_qubits_2] 
        target_qubits = sorted(target_qubits)
        super().__init__(name='Barenco', matrix=matrix, target_qubits=target_qubits) 

#------------------------------------------------------------------------------------
class Berkeley(GateDoubleQubit):
    def __init__(self, target_qubits_1=0, target_qubits_2=1):
        matrix = [[np.cos(np.pi / 8), 0, 0, +1j * np.sin(np.pi / 8)],
                  [0, np.cos(3 * np.pi / 8), +1j * np.sin(3 * np.pi / 8), 0],
                  [0, +1j * np.sin(np.pi / 8), np.cos(np.pi / 8), 0],
                  [+1j * np.sin(np.pi / 8), 0, 0, np.cos(np.pi / 8)]
                  ]
        target_qubits = [target_qubits_1, target_qubits_2] 
        target_qubits = sorted(target_qubits)
        super().__init__(name='Berkeley', matrix=matrix, target_qubits=target_qubits) 

#------------------------------------------------------------------------------------
class Canonical(GateDoubleQubit):
    def __init__(self, a, b, c, target_qubits_1=0, target_qubits_2=1):
        self.a = a
        self.b = b
        self.c = c
        matrix = [[np.exp(+1j * c) * np.cos(a - b), 0, 0, +1j * np.exp(+1j * c) * np.sin(a - b)],
                  [0, np.exp(-1j * c) * np.cos(a + b), +1j * np.exp(-1j * c) * np.sin(a + b), 0],
                  [0, +1j * np.exp(-1j * c) * np.sin(a + b), np.exp(-1j * c) * np.cos(a + b), 0],
                  [+1j * np.exp(+1j * c) * np.sin(a - b), 0, 0, np.exp(+1j * c) * np.cos(a - b)]
                  ]
        target_qubits = [target_qubits_1, target_qubits_2] 
        target_qubits = sorted(target_qubits)
        super().__init__(name='Canonical', matrix=matrix, target_qubits=target_qubits) 

#------------------------------------------------------------------------------------
class Givens(GateDoubleQubit):
    def __init__(self, theta, target_qubits_1=0, target_qubits_2=1):
        self.theta = theta
        matrix = [[1, 0, 0, 0],
                  [0, np.cos(theta), -np.sin(theta), 0],
                  [0, np.sin(theta), np.cos(theta), 0],
                  [0, 0, 0, 1]
                  ]   
        target_qubits = [target_qubits_1, target_qubits_2]
        target_qubits = sorted(target_qubits)
        super().__init__(name='Givens', matrix=matrix, target_qubits=target_qubits) 

#------------------------------------------------------------------------------------
class Magic(GateDoubleQubit):
    def __init__(self, target_qubits_1=0, target_qubits_2=1):
        array = np.array([[1, +1j, 0, 0],
                          [0, 0, +1j, 1],
                          [0, 0, +1j, -1],
                          [1, -1j, 0, 0]])
        matrix = 1 / np.sqrt(2) * array    
        target_qubits = [target_qubits_1, target_qubits_2]
        target_qubits = sorted(target_qubits)
        super().__init__(name='Magic', matrix=matrix, target_qubits=target_qubits)     

         