
"""
🥇 1	Deutsch-Jozsa	Function classification
🥈 2	Bernstein-Vazirani	Binary string extraction
🥉 3	Grover's Algorithm	Database search
🎓 4	Quantum Fourier Transform (QFT)	Basis for Shor's
📊 5	Variational Quantum Eigensolver (VQE)	Chemistry simulation
🔄 6	Quantum Approximate Optimization Algorithm (QAOA)	Optimization problems
🔑 7	Shor's Algorithm	Integer factorization
"""

"""
1. Deutsch-Jozsa - OK
2. Grover - OK
3. QFT - OK 
   & IQFT - OK 
4. Phase Estimation (QPE) - OK
5. VQE - 80%
6. QAOA
7. Shor - 50%
8. QSVM
"""

"""
tutorial: dj, grover, qft
pip:      dj, grover, qft, iqft
complete: dj, grover, qft, iqft, qpe
"""

# qc = dj(n_qubits, is_constant=True)
from .dj_algorithm import dj

# qc = grover(n, target_state)
from .grover_algorithm import grover

# qc = qft(qc, qubits)
from .qft_algorithm import qft 

# qc = iqft(qc, qubits)
from .iqft_algorithm import iqft

# qc = qpe(unitary_matrix, t_counting_qubits, namedraw='CU')
from .qpe_algorithm import qpe
