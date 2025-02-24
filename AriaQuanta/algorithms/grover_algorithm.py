
import math
from AriaQuanta._utils import np
from AriaQuanta.aqc.circuit import Circuit
from AriaQuanta.aqc.gatelibrary import H, X, Z, CZ, CCX, CNZ
#from AriaQuanta.aqc.visualization import CircuitVisualizer

#------------------------------------------------------------------------------------
#def controlled_n_z(qc, controls, target):
#    """
#    Implements a Controlled-n Z Gate without ancilla qubits.
#    
#    Parameters:
#        circuit: QuantumCircuit object.
#        controls: List of control qubit indices.
#        target: Index of the target qubit.
#    """
#    n = len(controls)
#    
#    if n == 1:
#        # Base Case: CZ gate
#        qc | CZ([controls[0]], [target])
#
#    elif n == 2:
#        # Base Case: CCZ gate
#        qc | H(target)
#        qc | CCX([controls[0], controls[1], target])
#        qc | H(target)
#    else:
#        # Step 1: Apply Hadamard to the target
#        qc | H(target)
#        
#        # Step 2: Reduce to C^(n-1)X
#        # Apply Toffoli gates iteratively to reduce control
#        for i in range(n - 2):
#            qc | CCX([controls[i], controls[i + 1], controls[i + 2]])
#        
#        # Step 3: Apply CCX on the final control and target
#        qc | CCX([controls[-2], controls[-1], target])
#        
#        # Step 4: Undo the Toffoli gates
#        for i in reversed(range(n - 2)):
#            qc | CCX([controls[i], controls[i + 1], controls[i + 2]])
#        
#        # Step 5: Apply Hadamard to the target again
#        qc | H(target)

#------------------------------------------------------------------------------------
def oracle(qc, target_state):
    """
    Oracle for Grover's Algorithm.
    
    Parameters:
        circuit: QuantumCircuit object.
        target_state: Binary string of target state.
    """
    n = len(target_state)
    
    # Apply X gates on qubits where target_state is '0'
    for i, bit in enumerate(target_state):  #reversed(target_state)):
        if bit == '0':
            qc | X(i)
    
    # Apply multi-controlled Z gate
    if n == 1:
        qc | Z(0)
    elif n == 2:
        qc | CZ([0], [1])
    else:
        qc | CNZ(n, n-1)
    #    circuit.ccz(*range(n))

    #controls = list(range(n-1))
    #target = n
    #controlled_n_z(qc, controls, target)

    # Undo the X gates
    for i, bit in enumerate(target_state): #reversed(target_state)):
        if bit == '0':
            qc | X(i)


#------------------------------------------------------------------------------------
def diffusion_operator(qc, n):
    """
    Implements the Grover Diffusion Operator.
    
    Parameters:
        circuit: QuantumCircuit object.
        n: Number of qubits.
    """
    # Apply Hadamard gates to all qubits
    for i in range(n):
        qc | H(i)
    
    # Apply X gates to all qubits
    for i in range(n):
        qc | X(i)
    
    if n == 1:
        qc | Z(0)
    elif n == 2:
        qc | CZ([0], [1])
    else:
        qc | CNZ(n, n-1)

    # Apply multi-controlled Z gate
    #controls = list(range(n-1))
    #target = n
    #controlled_n_z(qc, controls, target)

    # Apply X gates to all qubits
    for i in range(n):
        qc | X(i)
    
    # Apply Hadamard gates to all qubits
    for i in range(n):
        qc | H(i)

#------------------------------------------------------------------------------------
def grover(n, target_state):
    """
    Implements Grover's Algorithm.
    
    Parameters:
        circuit: QuantumCircuit object.
        oracle: Function implementing the oracle.
        n: Number of qubits.
        target_state: String representing the target state (e.g., "101").
    """
    # Step 1: Initialization
    qc = Circuit(n)

    # Apply Hadamard to all qubits
    for i in range(n):
        qc | H(i)
    
    # Calculate the number of iterations (π/4 * √N)
    iterations = int(math.pi / 4 * math.sqrt(2**n))
    
    for _ in range(iterations):
        # Step 2: Oracle
        oracle(qc, target_state)
        
        # Step 3: Diffusion Operator
        diffusion_operator(qc, n)

    # Step 4: Measurement
    # qc.run()
    # measurement, measurement_index, probabilities = qc.measure_all()
    
    return qc #, measurement, measurement_index, probabilities