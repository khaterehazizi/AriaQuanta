
import math
from AriaQuanta.aqc.gatelibrary import H, CP, SWAP

def iqft(qc, qubits):
    """
    Apply the Inverse Quantum Fourier Transform (IQFT) on the specified qubits.
    :param qc: Quantum Circuit
    :param qubits: List of qubits to apply IQFT
    """
    n = len(qubits)
    
    # Reverse the order of qubits using SWAP gates
    qubits_reversed = qubits[::-1]
    for i in range(n // 2):
        qc | SWAP(qubits[i], qubits_reversed[i])

    # Apply IQFT
    for i in range(n):
        # Apply Hadamard gate to qubit i
        qc | H(qubits[i])
        
        # Apply Controlled Phase Gates
        for j in range(i + 1, n):
            angle = -math.pi / (2 ** (j - i))
            qc | CP(angle, qubits[j], qubits[i])  # Controlled phase gate
            
    return qc        
