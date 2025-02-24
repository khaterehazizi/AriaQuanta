
import math
from AriaQuanta.aqc.gatelibrary import H, CP, SWAP

def qft(qc, qubits):
    """
    Implements the Quantum Fourier Transform on a set of qubits.
    
    Parameters:
        circuit: QuantumCircuit object
        qubits: List of qubit indices
    """
    n = len(qubits)
    
    for i in range(n):
        # Apply Hadamard gate to qubit i
        qc | H(qubits[i])
        
        # Apply controlled phase shifts
        for j in range(i+1, n):
            angle = math.pi / (2**(j-i))
            qc | CP(angle, qubits[j], qubits[i])  # Controlled phase gate
    
    # Reverse the order of qubits using SWAP gates
    qubits_reversed = qubits[::-1]
    for i in range(n // 2):
        qc | SWAP(qubits[i], qubits_reversed[i])

    return qc    
