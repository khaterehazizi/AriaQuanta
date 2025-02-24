
#import numpy as np
from AriaQuanta._utils import np, swap_qubits, is_unitary
import math

#////////////////////////////////////////////////////////////////////////////////////

class GateSingleQubit:
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

        if target_qubits[0] > 0:
            dim = 2 ** target_qubits[0]
            I1 = np.identity(dim, dtype=complex)
        else:
            I1 = 1
        if (num_of_qubits - target_qubits[0] - 1) > 0:
            dim = 2 ** (num_of_qubits - target_qubits[0] - 1)
            I2 = np.identity(dim, dtype=complex)
        else:
            I2 = 1         
    
        full_matrix = np.kron(I1, self.matrix)
        full_matrix = np.kron(full_matrix, I2)

        # reversed ordering as used in Qiskit
        #full_matrix = np.kron(self.matrix, I1)
        #full_matrix = np.kron(I2, full_matrix)
        #         
        multistate = np.dot(full_matrix, multistate)

        return multistate
    
    #----------------------------------------------
    def apply_density(self, num_of_qubits, density_matrix):
        
        target_qubits = self.target_qubits

        if target_qubits[0] > 0:
            dim = 2 ** target_qubits[0]
            I1 = np.identity(dim, dtype=complex)
        else:
            I1 = 1
        if (num_of_qubits - target_qubits[0] - 1) > 0:
            dim = 2 ** (num_of_qubits - target_qubits[0] - 1)
            I2 = np.identity(dim, dtype=complex)
        else:
            I2 = 1         
    
        full_matrix = np.kron(I1, self.matrix)
        full_matrix = np.kron(full_matrix, I2)
        
        density_matrix = full_matrix @ density_matrix @ np.conj(full_matrix.T)

        return density_matrix

#////////////////////////////////////////////////////////////////////////////////////
#///////// 1-Qubit Gates /////////
#------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------
class I(GateSingleQubit):
    def __init__(self, target_qubits=0):
        matrix = np.eye(2)
        super().__init__(name='I', matrix=matrix, target_qubits=target_qubits)

#------------------------------------------------------------------------------------
class GlobalPhase(GateSingleQubit):
    def __init__(self, delta, target_qubits=0):
        self.delta = delta
        matrix = np.exp(+1j * delta) * np.eye(2)
        super().__init__(name='GPh', matrix=matrix, target_qubits=target_qubits)

#------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------
class X(GateSingleQubit):
    def __init__(self, target_qubits=0):
        matrix = np.array([[0, 1], [1, 0]])
        super().__init__(name='X', matrix=matrix, target_qubits=target_qubits)

#------------------------------------------------------------------------------------
class Y(GateSingleQubit):
    def __init__(self, target_qubits=0):
        matrix = np.array([[0, -1j], [1j, 0]])
        super().__init__(name='Y', matrix=matrix, target_qubits=target_qubits)

#------------------------------------------------------------------------------------
class Z(GateSingleQubit):
    def __init__(self, target_qubits=0):
        matrix = np.array([[1, 0], [0, -1]])
        super().__init__(name='Z', matrix=matrix, target_qubits=target_qubits)

#------------------------------------------------------------------------------------
class S(GateSingleQubit):
    def __init__(self, target_qubits=0):
        matrix = np.array([[1, 0], [0, 1j]])
        super().__init__(name='S', matrix=matrix, target_qubits=target_qubits)

#------------------------------------------------------------------------------------
class Xsqrt(GateSingleQubit):
    def __init__(self, target_qubits=0):
        matrix = 1/2 * np.array([[1+1j, 1-1j], [1-1j, 1+1j]])
        super().__init__(name='Xsqrt', matrix=matrix, target_qubits=target_qubits)

#------------------------------------------------------------------------------------
class H(GateSingleQubit):
    def __init__(self, target_qubits=0):
        matrix = (1 / np.sqrt(2)) * np.array([[1, 1], [1, -1]])
        super().__init__(name='H', matrix=matrix, target_qubits=target_qubits)  

#------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------
class P(GateSingleQubit):
    def __init__(self, phi, target_qubits=0):
        self.phi = phi
        matrix = np.array([[1, 0], [0, np.exp(1j * phi)]])
        super().__init__(name='P', matrix=matrix, target_qubits=target_qubits)

#------------------------------------------------------------------------------------
class T(GateSingleQubit):
    def __init__(self, target_qubits=0):
        matrix = np.array([[1, 0], [0, np.exp(1j * np.pi / 4)]])
        super().__init__(name='T', matrix=matrix, target_qubits=target_qubits)

#------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------
class RX(GateSingleQubit):
    def __init__(self, theta, target_qubits=0):
        self.theta = theta
        matrix = np.array([
            [np.cos(self.theta / 2), -1j * np.sin(self.theta / 2)],
            [-1j * np.sin(self.theta / 2), np.cos(self.theta / 2)]
        ])
        super().__init__(name='RX', matrix=matrix, target_qubits=target_qubits)

#------------------------------------------------------------------------------------
class RY(GateSingleQubit):
    def __init__(self, theta, target_qubits=0):
        self.theta = theta
        matrix = np.array([
            [np.cos(self.theta / 2), -np.sin(self.theta / 2)],
            [np.sin(self.theta / 2), np.cos(self.theta / 2)]
        ])
        super().__init__(name='RY', matrix=matrix, target_qubits=target_qubits)

#------------------------------------------------------------------------------------
class RZ(GateSingleQubit):
    def __init__(self, theta, target_qubits=0):
        self.theta = theta
        matrix = np.array([
            [np.exp(-1j * self.theta / 2), 0.0],
            [0.0, np.exp(1j * self.theta / 2)]
        ])
        super().__init__(name='RZ', matrix=matrix, target_qubits=target_qubits)  

#------------------------------------------------------------------------------------ 
class Rot(GateSingleQubit):
    def __init__(self, theta, phi, lambda_, target_qubits=0):
        self.theta = theta
        self.phi = phi
        self.lambda_ = lambda_
        matrix = np.array([
            [np.cos(self.theta / 2), -np.exp(1j * self.lambda_) * np.sin(self.theta / 2)],
            [np.exp(1j * self.phi) * np.sin(self.theta / 2), np.exp(1j * (self.lambda_ + self.phi)) * np.cos(self.theta / 2)]
        ])
        super().__init__(name='Rot', matrix=matrix, target_qubits=target_qubits)   







    
     
   
