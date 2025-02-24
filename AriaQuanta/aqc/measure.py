
import numpy as np
#from AriaQuanta.config import PrintOptions

class Measure:
    def __init__(self, name, qubits, clbits, resize):
        
        self.name = name
        self.qubits = qubits
        self.clbits = clbits
        self.resize = resize

        #self.qc_values = []
        #self.c_values_dict = {}
        #self.q_values_dict = {}

        self.clbit_values_dict = {}
        self.qubit_values_dict = {}

    def apply(self, num_of_qubits, multistate):

        # example:
        # qc.measure_all([1, 2], [0, 1])
        # Measures qubit 1 into classical bit 0 and qubit 2 into classical bit 1          

        #---------------------------------------

        state = multistate
        num_of_states = np.shape(state)[0]
        num_of_qubits = int(np.log2(num_of_states)) 

        bin_format = '#0' + str(num_of_qubits + 2) + 'b' # #05b
        all_states = [format(x, bin_format)[2:] for x in range(num_of_states)] #  010: q0, q1, q2
        all_states_original = all_states

        #-------------------------------------------------
        probabilities = np.abs(state) ** 2
        probabilities /= np.sum(probabilities)  # Normalize probabilities to sum to 1
        probabilities = probabilities.flatten()

        #-------------------------------------------------
        measurement_index = np.random.choice(len(state), p=probabilities)
        measurement_state = all_states[measurement_index] 
        measurement = measurement_state # '|' + measurement_state + '>'      

        #---------------------------------------
        # save measurement outputs
        #if self.clbits == []:
        #    for i in self.qubits:
        #        self.clbits = ['c'+str(i)]
        #q_bits = self.qubits
        #clbits = self.clbits  

        #qc_values = []
        #c_values_dict = {}
        #q_values_dict = {}
        # qc_values: {'q_bit': value}
        # c_values_dict: {'c0': 1, 'c1': 1}
        #for i in range(len(q_bits)):
        #    q_bits_i = q_bits[i]
        #    meausrement_i = measurement_state[q_bits_i]
        #    c_value = int(meausrement_i)
        #    qc_values.append((q_bits_i, str(clbits[i]), c_value))
        #    q_values_dict[str(q_bits_i)] = c_value
        #    c_values_dict[str(clbits[i])] = c_value

        #self.qc_values = qc_values
        #self.c_values_dict = c_values_dict
        #self.q_values_dict = q_values_dict
        # print(qc_values, c_values_dict)

        #---------------------------------------
        # save measurement outputs

        qubits = self.qubits
        clbits = self.clbits

        if clbits == None:
            clbits = ['c' + str(item) for item in self.qubits]

        for i in range(len(qubits)):
            qubits_i = qubits[i]
            clbits_i = clbits[i]
            meausrement_i = measurement_state[qubits_i]
            self.qubit_values_dict['q' + str(qubits_i)] = meausrement_i
            self.clbit_values_dict[str(clbits_i)] = meausrement_i   

        #if PrintOptions.print_measure:
            #keys = ['q' + str(item) for item in self.qubits]
            #print("\nmeasurement on qubits {} are: {}".format(keys, self.clbit_values_dict)) 

        #---------------------------------------
        # find the remaining elements of statevector

        #select_indices = []
        #for i in range(len(qc_values)):
        #    indices = [index for index, string in enumerate(all_states) if string[qc_values[i][0]] == str(qc_values[i][2])]
        #    select_indices.append(indices)

        for i in range(len(qubits)):
            select_indices=[]
            for j in range(len(all_states)):
                if all_states[j][qubits[i]] == self.qubit_values_dict['q' + str(qubits[i])]:
                    select_indices.append(j)
            all_states=[all_states[x] for x in select_indices]  
        
        #if PrintOptions.print_measure:
        #    print("\nmeasurement output:", all_states)      

        last_indices=[]
        for item in all_states:
            index_item=all_states_original.index(item)
            last_indices.append(index_item)

        #---------------------------------------
        # update multistate

        probabilities_selected = probabilities[last_indices]
        scale_probabilities = 1 / np.sum(probabilities_selected)   
        scale_probabilities_sqrt = np.sqrt(scale_probabilities)

        if self.resize == True:
            multistate = multistate[last_indices]
            multistate *= scale_probabilities_sqrt

        else:
            remove_indices = [i for i in list(range(num_of_states)) if i not in last_indices]
            multistate[remove_indices] = 0    
            multistate *= scale_probabilities_sqrt     

        return multistate
        

#------------------------------------------------------------------------------------
class MeasureQubit(Measure):
    def __init__(self, qubits, clbits=None):    
        self.resize=False        
        super().__init__(name='MeasureQubit', qubits=qubits, clbits=clbits, resize=self.resize)

#------------------------------------------------------------------------------------
class MeasureQubitResize(Measure):
    def __init__(self, qubits, clbits=None):  
        self.resize=True          
        super().__init__(name='MeasureQubit', qubits=qubits, clbits=clbits, resize=self.resize)
        