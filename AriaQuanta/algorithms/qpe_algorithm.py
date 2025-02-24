
import numpy as np
from AriaQuanta.aqc.gatelibrary import H, CU
from AriaQuanta.aqc.circuit import Circuit
from AriaQuanta.algorithms import iqft

# Quantum Phase Estimation Algorithm
def qpe(unitary_matrix, t_counting_qubits, namedraw='CU'):
    """
    Implements the Quantum Phase Estimation algorithm.
    :param qc: Quantum Circuit
    :param unitary: The unitary operator (controlled version must be defined)
    :param n_counting_qubits: Number of counting qubits
    :param target_qubits: The qubit containing the eigenstate
    """

    qc = Circuit(t_counting_qubits + 1)
    target_qubits = t_counting_qubits

    # Step 1: Apply Hadamard gates to counting qubits
    for i in range(t_counting_qubits):
        qc | H(i)
    
    # Step 2: Apply controlled unitary gates

    powers = [2** i for i in range(t_counting_qubits-1, -1, -1)]

    for i in range(t_counting_qubits):
        myCU = CU(unitary_matrix, control_qubits=[i], target_qubits=[target_qubits])
        myCU.namedraw = namedraw
        for _ in range(powers[i]):
            #print(myCU.control_qubits, myCU.target_qubits)
            qc | myCU
    
    # Step 3: Apply Inverse Quantum Fourier Transform
    #qc.inverse_qft(range(t_counting_qubits))
    qc = iqft(qc, list(range(t_counting_qubits)))
    
    # Step 4: Measure counting qubits
    #qc.measure_all(range(t_counting_qubits), range(t_counting_qubits))

    return qc