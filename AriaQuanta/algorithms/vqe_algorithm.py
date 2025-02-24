

import numpy as np
from scipy.optimize import minimize
from AriaQuanta.aqc.gatelibrary import RY, CX, H, RX
from AriaQuanta.aqc.circuit import Circuit

from collections import Counter


#------------------------------------------------------------------------------------
class Ansatz:
    def __init__(self, num_qubits, params):
        self.num_qubits = num_qubits
        self.params = params  # List of parameters (angles for gates)
    
    def build_circuit(self):
        qc = Circuit(self.num_qubits)
        for i, param in enumerate(self.params):
            qc | RY(i, param)
            qc | CX((i, (i+1) % self.num_qubits))
        return qc


#------------------------------------------------------------------------------------
def measure_pauli(circuit, pauli_string):
    """
    Measures the expectation value of a Pauli string on a given quantum circuit.
    
    Args:
        circuit (QuantumCircuit): The quantum circuit prepared with the ansatz.
        pauli_string (str): A string like 'X0 Z1', representing Pauli operators on qubits.
    
    Returns:
        float: The expectation value of the given Pauli operator.
    """
    # Clone the circuit to avoid modifying the original
    measured_circuit = circuit.copy()
    
    # Apply basis transformation for each Pauli operator
    for term in pauli_string.split():
        op = term[0]  # Operator (X, Y, Z)
        qubit = int(term[1:])  # Qubit index
        
        if op == 'X':
            measured_circuit | H(qubit)  # Change to X basis with Hadamard
        elif op == 'Y':
            measured_circuit | RX(qubit, -np.pi / 2)  # Change to Y basis
        elif op == 'Z':
            pass  # Z basis is the default measurement basis
    
    # Perform measurement in the computational basis
    results = measured_circuit.measure_all()
    
    # Calculate expectation value
    shots = len(results)
    total = 0
    for outcome, count in results.items():
        # Parity: Check if the measurement outcome is +1 or -1
        parity = 1
        for term in pauli_string.split():
            op = term[0]
            qubit = int(term[1:])
            if op in 'XYZ' and outcome[qubit] == '1':  # Check qubit's measured state
                parity *= -1
        total += parity * count
    
    expectation_value = total / shots
    return expectation_value

#------------------------------------------------------------------------------------
class Hamiltonian:
    def __init__(self, terms):
        # terms is a list of tuples (coefficient, Pauli string)
        self.terms = terms  # Example: [(0.5, 'Z0'), (0.3, 'X1')]
    
    def expection_value(self, circuit):
        return 1

    #def expectation_value(self, circuit):
    #    total = 0
    #    for coeff, pauli_string in self.terms:
    #        total += coeff * measure_pauli(circuit, pauli_string)
        #return total


#------------------------------------------------------------------------------------
def VQE(num_qubits, hamiltonian, initial_params):
    def cost_function(params):
        ansatz = Ansatz(num_qubits, params)
        circuit = ansatz.build_circuit()
        return hamiltonian.expectation_value(circuit)
    
    result = minimize(cost_function, initial_params, method='COBYLA')
    return result


'''


# Example Generalized Hamiltonian
hamiltonian = [
    (-1.05, 'Z0'),       # Single qubit Z on qubit 0
    (0.39, 'Z1'),        # Single qubit Z on qubit 1
    (0.72, 'Z0Z1'),      # Two-qubit ZZ interaction
    (0.35, 'X0X1'),      # Two-qubit XX interaction
    (0.25, 'Y0Z1X2')     # Three-qubit mixed term
]

# Example Mock Measurement Results
measurement_data = {
    'Z': {'000': 30, '001': 20, '010': 25, '011': 25},
    'X': {'+++': 40, '++-': 30, '+-+': 20, '--+': 10},
    'Y': {'+++': 35, '++-': 25, '+-+': 25, '--+': 15},
    'Z_total': 100,
    'X_total': 100,
    'Y_total': 100
}

def expectation_from_counts(counts, observable, total_shots):
    """
    Calculate expectation value from measurement outcomes for an arbitrary observable.
    """
    expectation = 0
    
    for state, count in counts.items():
        eigenvalue = 1  # Start neutral
        
        for i, op in enumerate(observable):
            if op == 'Z':
                eigenvalue *= 1 if state[i] == '0' else -1
            elif op == 'X':
                eigenvalue *= 1 if state[i] == '+' else -1
            elif op == 'Y':
                eigenvalue *= 1 if state[i] == '+' else -1
        
        expectation += (count / total_shots) * eigenvalue
    
    return expectation

def calculate_total_expectation(hamiltonian, measurement_data, n_qubits):
    """
    Generalized expectation value calculation for an arbitrary Hamiltonian and n qubits.
    """
    total_expectation = 0
    
    for coeff, term in hamiltonian:
        # Determine measurement basis
        if 'X' in term:
            basis = 'X'
            counts = measurement_data['X']
            total_shots = measurement_data['X_total']
        elif 'Y' in term:
            basis = 'Y'
            counts = measurement_data['Y']
            total_shots = measurement_data['Y_total']
        else:
            basis = 'Z'
            counts = measurement_data['Z']
            total_shots = measurement_data['Z_total']
        
        # Build observable string
        observable = ['I'] * n_qubits  # Default to identity
        for i in range(len(term)):
            if term[i] in 'XYZ':
                qubit_index = int(term[i+1])  # Extract qubit index
                observable[qubit_index] = term[i]
        
        # Calculate expectation for this term
        exp_val = expectation_from_counts(counts, observable, total_shots)
        
        # Weighted sum
        total_expectation += coeff * exp_val
    
    return total_expectation

# Define number of qubits in your system
n_qubits = 3

# Calculate total expectation
total_expectation = calculate_total_expectation(hamiltonian, measurement_data, n_qubits)
print("Total Expectation Value:", total_expectation)


# Hamiltonian as a list of Pauli operators and coefficients
hamiltonian = [
    (1.0, 'Z0'),   # Z operator on qubit 0
    (-0.5, 'Z1'),  # Z operator on qubit 1
    (0.5, 'X0X1')  # XX operator between qubit 0 and 1
]

# Expectation value calculation
def expectation_value(circuit, hamiltonian, params):
    circuit.set_parameters(params)
    expectation = 0
    for coeff, operator in hamiltonian:
        expectation += coeff * circuit.measure_expectation(operator)
    return expectation

# Classical optimizer
def vqe(num_qubits, hamiltonian):
    circuit = QuantumCircuit(num_qubits)
    
    def objective(params):
        return expectation_value(circuit, hamiltonian, params)
    
    # Initial random parameters
    initial_params = np.random.rand(num_qubits)
    
    # Classical optimization
    result = minimize(objective, initial_params, method='COBYLA')
    
    print("Optimal Parameters:", result.x)
    print("Minimum Energy:", result.fun)
    return result.x, result.fun

# Run VQE for a simple 2-qubit example
optimal_params, min_energy = vqe(2, hamiltonian)
print(optimal_params, min_energy)
'''