
from AriaQuanta.aqc.circuit import Circuit
from AriaQuanta.aqc.gatelibrary import X, H, CX

def dj(n_qubits, is_constant=True):
    """
    Implements the Deutsch-Jozsa algorithm for a given number of qubits.
    :param n_qubits: Number of qubits in the input (not counting the oracle qubit)
    :param is_constant: Boolean flag to decide whether the oracle represents a constant or balanced function
    :return: Measurement result indicating if the function is constant or balanced
    """

    # Initialize circuit with n_qubits + 1 (oracle) qubit
    qc = Circuit(n_qubits + 1)
    
    # Set the last qubit (oracle qubit) to |1⟩
    # Apply X and Hadamard gates to oracle qubit
    qc | X(n_qubits) | H(n_qubits)
    
    # Apply Hadamard gate to all input qubits
    for qubit in range(n_qubits):
        qc | H(qubit)
    
    #----------------------------------------------------------
    #if oracleType == 0:#If the oracleType is "0", the oracle returns oracleValue for all input. 
    #    if oracleValue == 1:
    #        djCircuit.x(qr[n])
    #    else:
    #        djCircuit.id(qr[n])
    #else: # Otherwise, it returns the inner product of the input with a (non-zero bitstring) 
    #    for i in range(n):
    #        if (a & (1 << i)):
    #            djCircuit.cx(qr[i], qr[n])

    # Apply the Oracle (constant or balanced)
    # For simplicity, we'll assume the oracle applies X gates based on constant/balanced
    if is_constant:
        # Constant oracle does nothing for all inputs or flips all inputs
        pass  # Apply no gate or apply identity
    else:
        # Balanced oracle example: flip for a balanced outcome (e.g., a CNOT gate)
        for qubit in range(n_qubits):
            qc | CX(qubit, n_qubits)  # Control each input qubit to flip oracle qubit
    #----------------------------------------------------------

    # Apply Hadamard gate again to all input qubits
    for qubit in range(n_qubits):
        qc | H(qubit)
    
    # Run the circuit
    #result = qc.run()

    # Measure only the input qubits (ignore the oracle qubit)
    #measurement_all_qubits, _, _ = qc.measure_all()
    #measurement_n_qubits = measurement_all_qubits[1:n_qubits+1]
    #print(measurement_n_qubits)

    # Analyze the result
    # If result is all |0⟩, the function is constant; otherwise, it's balanced.
    #if measurement_n_qubits == '0' * n_qubits:
    #    output = "measurement = " + measurement_n_qubits + ", Function is constant"
    #else:
    #    output = "measurement = " + measurement_n_qubits + ", Function is balanced"

    # *** Note! Should change the plot for the circuit ***
    # It has a dummy qubit
    
    return qc
