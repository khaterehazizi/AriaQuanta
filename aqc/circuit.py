
#import numpy as np
import matplotlib.pyplot as plt
from copy import deepcopy
#from collections import defaultdict

from AriaQuanta._utils import np
from AriaQuanta.aqc.qubit import MultiQubit
from AriaQuanta.aqc.gatelibrary import Custom
from AriaQuanta.aqc.measure import Measure
from AriaQuanta.aqc.operations import If_cbit


class Circuit:
    def __init__(self, num_of_qubits, num_of_clbits=0, num_of_ancilla=0, list_of_qubits=[]):

        # num_of_ancilla=0 - initial_state=None
        self.num_of_qubits = num_of_qubits
        self.num_of_clbits = num_of_clbits
        self.num_of_ancilla = num_of_ancilla

        # result of the measurement / measurement.qubit_values_dict
        self.measurequbit_values = {} 
        # measurement.qubit_values_dict = {'q0':0, 'q1':0}  # for the circuit and outputting
        # measurement.clbit_values_dict = {'c0':0, 'c1':0}  # 'c0' or any user-defined charachter for If_cbit condition

        self.gates = []
        #self.gatesinfo  # as a property

        self.width = num_of_qubits+num_of_clbits    # number of wires
        #self.size:   # as a property               # number of gates
        #self.depth:  # as a property               # number of operations (independent gates)

        #--- romovied -- self.data:   # as a property  # dictionary of everything
            

        #--------------------------------------------
        if list_of_qubits == []:
            multiqubit = MultiQubit(num_of_qubits)
            initial_state = multiqubit.multistate  
        else:
            multiqubit = MultiQubit(num_of_qubits, list_of_qubits)
            initial_state = multiqubit.multistate 

        self.initial_state = initial_state    
        self.statevector = initial_state
        #self.statevector_reorder       # as a property             # show statevector as in Qiskit

        #self.density_matrix = density_matrix   # as a property     # only for output
        #self.density_matrix_reorder = density_matrix_reorder # as a property

    #----------------------------------------------
    @property
    def statevector_reorder(self):
        num_of_states = np.shape(self.statevector)[0]
        num_of_qubits = int(np.log2(num_of_states)) 

        bin_format = '#0' + str(num_of_qubits + 2) + 'b' # #05b
        all_states = [format(x, bin_format)[2:] for x in range(num_of_states)]
        all_states = [x[::-1] for x in all_states]
        #print(all_states) # ['00', '10', '01', '11']
        #                    [q1=0 q0=0, q1=1 q0=0, q1=0 q0=1, q1=1 q0=1]  
        new_indices = [int(x, 2) for x in all_states]
        statevector_reorder = self.statevector[new_indices]
        return statevector_reorder  

    #----------------------------------------------
    @property
    def size(self):
        return len(self.gates)

    #----------------------------------------------
    @property
    def gatesinfo(self):
        gatesinfo_dict = {} #defaultdict(lambda: 0)
        for gate in self.gates:
            if gate.name in gatesinfo_dict:
                gatesinfo_dict[gate.name] += 1
            else:
                gatesinfo_dict[gate.name] = 1    
        return gatesinfo_dict

    #----------------------------------------------
    @property
    def density_matrix(self):
        this_state = self.statevector
        density_matrix = this_state @ this_state.T
        return density_matrix

    #----------------------------------------------
    @property
    def density_matrix_reorder(self):
        this_state = self.statevector_reorder
        density_matrix_reorder = this_state @ this_state.T
        return density_matrix_reorder
    
    #----------------------------------------------
    @property
    def depth(self):
        return self.get_depth()

    #----------------------------------------------
    def get_depth(self):

        depth = 0
        if len(self.gates) > 0:
            depth += 1
            gates = self.gates
            qubits_i = gates[0].qubits
            qubits_previous = []

            qubits_previous = qubits_i

            for i in range(1, len(gates)):
                qubits_i = gates[i].qubits
                flag = np.in1d(qubits_i,qubits_previous).any()

                if flag:
                    depth += 1
                    qubits_previous = qubits_i
                else:
                    qubits_previous = np.concatenate((qubits_previous, qubits_i))                        

        return depth     

    #----------------------------------------------
    def __or__(self, gate):
        if max(gate.qubits) > self.num_of_qubits:
            raise ValueError("{} is out-of-range for the qubit ID. The valid ID is between 0 and {}".format(max(gate.qubits),self.num_of_qubits-1))
        self.add_gate(gate)
        return self

    #----------------------------------------------
    def add_gate(self, gate):
        self.gates.append(gate)             
        
    #----------------------------------------------
    def run(self):
        #count=0
        measurequbit_values = {}
        for gate in self.gates:
            if isinstance(gate, Measure):
                state = gate.apply(self.num_of_qubits, self.statevector)
                clbit_values_dict = gate.clbit_values_dict
                qubit_values_dict = gate.qubit_values_dict
                
                measurequbit_values.update(qubit_values_dict)    # modifies z with keys and values of y
                #print(qubit_values_dict) # default: q0, q1, q2, ...
                #print(clbit_values_dict) # user-defined or default: c0, c1, c2, ...

            elif isinstance(gate, If_cbit):
                conditions = gate.conditions
                if clbit_values_dict[conditions[0]] == str(conditions[1]):
                    state = gate.apply(self.num_of_qubits, self.statevector)
            else:
                state = gate.apply(self.num_of_qubits, self.statevector)

            self.statevector = state

        #----------------------------------------------------
        # if the dictionary is empty. put all the qubits as the keys:
        if not measurequbit_values:
            for i in range(self.num_of_qubits):
                measurequbit_values['q'+str(i)] = ''
        # sort the dictionary
        measurequbit_values = dict(sorted(measurequbit_values.items()))
        # save as the circuit's property
        self.measurequbit_values = measurequbit_values

        return state
        
    #----------------------------------------------
    def measure_all(self):
        # only measurement - not changing the statevector

        num_of_qubits = self.num_of_qubits
        num_of_ancilla = self.num_of_ancilla
        num_of_remaining_qubits = num_of_qubits - num_of_ancilla
        num_of_remaining_states = 2**num_of_remaining_qubits

        bin_format = '#0' + str(num_of_remaining_qubits + 2) + 'b' # #05b
        all_states = [format(x, bin_format)[2:] for x in range(num_of_remaining_states)]
        #all_states = [x[::-1] for x in all_states]
        #print(all_states) # ['00', '10', '01', '11']
        #                    [q1=0 q0=0, q1=1 q0=0, q1=0 q0=1, q1=1 q0=1]

        #-------------------------------------------------

        state_reorder = sv_reorder_qubits(self.statevector)

        for i in range(num_of_ancilla):
            size_state_reorder = int(np.shape(state_reorder)[0]/2)
            state_reorder = state_reorder[:size_state_reorder]

        state_remaining = sv_reorder_qubits(state_reorder)

        probabilities = np.abs(state_remaining) ** 2
        probabilities = probabilities / np.sum(probabilities)  # Normalize probabilities to sum to 1
        probabilities = probabilities.flatten()

        #-------------------------------------------------
        measurement_index = np.random.choice(len(state_remaining), p=probabilities)
        measurement_state = all_states[measurement_index]
        measurement = '|' + measurement_state + '>'      

        return measurement #, measurement_index, probabilities 

    #----------------------------------------------
    def copy(self): 
        qc_copy = deepcopy(self)
        return qc_copy

#------------------------------------------------------------------------------------
def sv_reorder_qubits(statevector):
    num_of_states = np.shape(statevector)[0]
    num_of_qubits = int(np.log2(num_of_states)) 

    bin_format = '#0' + str(num_of_qubits + 2) + 'b' # #05b
    all_states = [format(x, bin_format)[2:] for x in range(num_of_states)]
    all_states = [x[::-1] for x in all_states]
    #print(all_states) # ['00', '10', '01', '11']
    #                    [q1=0 q0=0, q1=1 q0=0, q1=0 q0=1, q1=1 q0=1]  
    new_indices = [int(x, 2) for x in all_states]
    statevector_reorder = statevector[new_indices]
    return statevector_reorder  

#------------------------------------------------------------------------------------
def sv_to_probabilty(statevector, plot=True):
    plt.rc('font', family='sans-serif')
    plt.rcParams['font.size']= 14
    plt.rcParams['axes.linewidth']= 1.5

    #--------------------------------
    num_of_qubits = int(np.log2(statevector.shape[0]))
    num_of_states = 2**num_of_qubits
    bin_format = '#0' + str(num_of_qubits + 2) + 'b'

    #
    probabilities = np.abs(statevector) ** 2
    probabilities /= np.sum(probabilities)  # Normalize probabilities to sum to 1
    probabilities = probabilities.flatten()

    bin_format = '#0' + str(num_of_qubits + 2) + 'b' # #05b
    all_states = [format(x, bin_format)[2:] for x in range(num_of_states)]
    
    #if reorder==True:
    #    all_states = [x[::-1] for x in all_states]   
    xtickes = all_states  

    probabilities_dict = {}
    for i in range(num_of_states):
        probabilities_dict[all_states[i]] = probabilities[i]   

    if plot==True:
        fig, ax = plt.subplots()
        xx = np.arange(np.shape(probabilities)[0])
        ax.bar(xx, probabilities)
        plt.xticks(xx, xtickes, rotation=45)
        ax.set_ylabel('Probability')

    return probabilities_dict

#------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------   
def to_gate(qc):   # quantum circuit

    num_of_qubits = qc.num_of_qubits

    this_qc = Circuit(num_of_qubits)
    this_qc.gates = qc.gates

    # state_0
    state_0 = this_qc.statevector
    state_0_norm = state_0 / np.linalg.norm(state_0)
    #print(this_qc.data)
 
    # state_1
    state_1 = this_qc.run()
    #print(this_qc.data)
    state_1_norm = state_1 / np.linalg.norm(state_1)
    #print(this_qc.data)

    #------------
    # state_1 -> normalized last state
    # state_0 -> normalize initial state
    # v = state_1 - state_0
    # A = I - 2 (v v_dagger) / (v_dagger v)
    v = state_1_norm - state_0_norm
    v = np.reshape(v, (v.size, 1))
    v_dagger = np.reshape(v, (1, v.size))

    V_Vdagger = v @ v_dagger
    Vdagger_V = v_dagger @ v
    I = np.eye(2 ** num_of_qubits)

    A = I - 2 * V_Vdagger / Vdagger_V
    
    circuit_gate = Custom(matrix=A, target_qubits=list(range(0, num_of_qubits)))
    circuit_gate.matrix = A
    circuit_gate.name = 'Circuit_gate'

    return circuit_gate
    

    #----------------------------------------------
"""  
    def measure_qubit(self, quantum_bits, classical_bits):
 
        # example:
        # qc.measure_all([1, 2], [0, 1])
        # Measures qubit 1 into classical bit 0 and qubit 2 into classical bit 1

        qc_copy = self.copy()
        qc_copy.run()

        state = qc_copy.statevector
        #print("measure state = ", state)
        probabilities = np.abs(state) ** 2
        #print(probabilities)
        probabilities /= np.sum(probabilities)  # Normalize probabilities to sum to 1
        probabilities = probabilities.flatten()
        measurement_index = np.random.choice(len(state), p=probabilities)
        
        num_of_states = np.shape(state)[0]
        num_of_qubits = int(np.log2(num_of_states))
        bin_format = '#0' + str(num_of_qubits + 2) + 'b'
        measurement_state = format(measurement_index, bin_format)[2:]
        measurement = '|' + measurement_state + '>'
        #print(measurement)
        
        if len(quantum_bits) != len(classical_bits):
            raise("the measurement quantum and classincal inputs have to have the same length")
        
        classical_bits_values = {}
        for i in range(len(quantum_bits)):
            meausrement_i = measurement_state[quantum_bits[i]]
            classical_bits_values[str(classical_bits[i])] = int(meausrement_i)

        return classical_bits_values
"""    

    #----------------------------------------------
    # @property
    # def data(self):
    #    dict_data = {}

    #    dict_data['depth'] = self.depth
    #    dict_data['gates'] = self.gates
    #    dict_data['num_of_qubits'] = self.num_of_qubits
    #    dict_data['size'] = self.size
    #    dict_data['statevector'] = self.statevector
    #    dict_data['width'] = self.width
    #    dict_data['density_matrix'] = self.density_matrix

    #    return dict_data
