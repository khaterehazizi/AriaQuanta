
import math
import matplotlib.pyplot as plt
from AriaQuanta._utils import np
import pandas as pd
from collections import Counter
from AriaQuanta.aqc.circuit import Circuit, sv_reorder_qubits


#------------------------------------------------------------------------------------
class Result():
    def __init__(self, statevector_all, num_of_qubits, num_of_ancilla, measurequbit_values_all): #, output_all):
        self.statevector_all = statevector_all
        self.num_of_qubits = num_of_qubits
        self.num_of_ancilla = num_of_ancilla
        self.measurequbit_values_all = measurequbit_values_all

        # self.density_matrix_all

    #----------------------------------------------
    @property
    def statevector_all_no_ancilla(self):

        statevector_all = self.statevector_all

        num_of_qubits = self.num_of_qubits
        num_of_ancilla = self.num_of_ancilla
        num_of_remaining_qubits = num_of_qubits - num_of_ancilla
        num_of_remaining_states = 2**num_of_remaining_qubits

        num_of_iterations = len(statevector_all)

        state_remaining_all = []
        for i in range(num_of_iterations):
            statevector_i = statevector_all[i]
            state_reorder = sv_reorder_qubits(statevector_i)

            for i in range(num_of_ancilla):
                size_state_reorder = int(np.shape(state_reorder)[0]/2)
                state_reorder = state_reorder[:size_state_reorder]

            state_remaining = sv_reorder_qubits(state_reorder)
            state_remaining_all.append(state_remaining)
        return state_remaining_all

    #----------------------------------------------
    @property
    def density_matrix_all(self):
        density_matrix_all = [] 
        num_of_iterations = len(self.statevector_all) 

        for i in range(num_of_iterations):
            this_statevector = self.statevector_all[i]
            this_density_matrix = sv_to_density_matrix(this_statevector)
            density_matrix_all.append(this_density_matrix)

        return density_matrix_all

    #----------------------------------------------
    def statevector_all_measured(self):
        statevector_all = self.statevector_all
        measurequbit_values_all = self.measurequbit_values_all
        num_of_iterations = len(statevector_all)

        bin_format = '#0' + str(self.num_of_qubits + 2) + 'b' # #05b
        all_states = [format(x, bin_format)[2:] for x in range(2**self.num_of_qubits)] 

        output_statevector_all_reduce = []
        for i in range(num_of_iterations):
            measurequbit_values_i = measurequbit_values_all[i]
            statevector_i = statevector_all[i]
            # Find indices where all conditions are met
            result_indices = [i for i, s in enumerate(all_states) if all(s[int(k[1:])] == str(v) for k, v in measurequbit_values_i.items())]
            output_statevector_all_reduce.append(statevector_i[result_indices])

        return output_statevector_all_reduce    

    #----------------------------------------------
    def count(self, clbits=[]):

        #-----------------------------------
        # select indices based on measurement
        if clbits == []:
            measurequbit_values_all = self.measurequbit_values_all
            if all(x=='' for x in measurequbit_values_all[0].values()):
                keys = ['q' + str(i) for i in range(self.num_of_qubits)]
                #print(keys)
            else:
                keys = list(measurequbit_values_all[0].keys())
                #print(keys)

        else:
            keys = clbits 
            #print(keys)       

        select_idx = sorted([int(item[1:]) for item in keys])   # remove 'q'  

        statevector_all = self.statevector_all

        num_of_qubits = self.num_of_qubits
        # num_of_ancilla = self.num_of_ancilla
        num_of_remaining_qubits = num_of_qubits # - num_of_ancilla
        num_of_remaining_states = 2**num_of_remaining_qubits

        num_of_iterations = len(statevector_all)

        measurement_all = []
        for i in range(num_of_iterations):
            this_qc = Circuit(num_of_qubits=num_of_qubits) #, num_of_ancilla=num_of_ancilla)
            this_qc.statevector = statevector_all[i]
            measurement = this_qc.measure_all()        # e.g. |001>
            measurement = measurement[1:num_of_remaining_qubits+1]   # +1 is for '|' charachter in the measurement output
            #print(measurement)
            measurement_select = ''.join(measurement[n] for n in select_idx)
            measurement_select = '|' + measurement_select + '>'
            measurement_all.append(measurement_select) # append(measurement[1:-1])  # remove the braces

        counts = Counter(measurement_all) 

        #----------------------------------------------
        # Add missing keys with a count of 0
        measure_size_qubit = len(select_idx)
        measure_size_state = 2**measure_size_qubit
        bin_format = '#0' + str(measure_size_qubit + 2) + 'b' # #05b
        all_states = [format(x, bin_format)[2:] for x in range(measure_size_state)] 
        all_states = ["|"+item+">" for item in all_states] 

        #----------------------------------------------
        # Add missing keys with a count of 0
        for state_i in all_states:
            if state_i not in counts:
                counts[state_i] = 0

        # Sort the keys in the desired order
        counts = {key: counts[key] for key in sorted(all_states)}

        #----------------------------------------------
        # also find the probabilities:
        probability = {key: counts[key]/num_of_iterations for key in sorted(all_states)}

        return counts, probability    

#----------------------------------------------    
def sv_to_density_matrix(statevector):
    
    this_state = statevector
    this_density_matrix = this_state @ this_state.T
    
    return this_density_matrix

#---------------------------------------------- 
def plot_histogram(counter):

    plt.rc('font', family='sans-serif')
    plt.rcParams['font.size']= 14
    plt.rcParams['axes.linewidth']= 1.5

    fig, ax = plt.subplots()
    ax.bar(counter.keys(), counter.values())
    ax.set_xticks(ax.get_xticks())
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')

#------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------
class ResultDensity():
    def __init__(self, density_matrix_all):
        self.density_matrix_all = density_matrix_all


#------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------      

# count based on statevector_all
"""
#----------------------------------------------     
def count(self):

    statevector_all = self.statevector_all

    num_of_qubits = self.num_of_qubits
    num_of_ancilla = self.num_of_ancilla
    num_of_remaining_qubits = num_of_qubits - num_of_ancilla
    num_of_remaining_states = 2**num_of_remaining_qubits

    num_of_iterations = len(statevector_all)

    bin_format = '#0' + str(num_of_remaining_qubits + 2) + 'b' # #05b
    all_states = [format(x, bin_format)[2:] for x in range(num_of_remaining_states)] 
    all_states = ["|"+item+">" for item in all_states]       

    measurement_all = []
    for i in range(num_of_iterations):
        this_qc = Circuit(num_of_qubits=num_of_qubits, num_of_ancilla=num_of_ancilla)
        this_qc.statevector = statevector_all[i]
        measurement = this_qc.measure_all()        # e.g. |001>
        #measurement = measurement[1:num_of_remaining_qubits+1]   # +1 is for '|' charachter in the measurement output
        #measurement = '|' + measurement + '>'
        measurement_all.append(measurement) # append(measurement[1:-1])  # remove the braces

    counts = Counter(measurement_all) 

    #----------------------------------------------
    # Add missing keys with a count of 0
    for state_i in all_states:
        if state_i not in counts:
            counts[state_i] = 0

    # Sort the keys in the desired order
    counts = {key: counts[key] for key in sorted(all_states)}

    #----------------------------------------------
    # also find the probabilities:
    probability = {key: counts[key]/num_of_iterations for key in sorted(all_states)}

    return counts, probability

"""    