#import numpy as np

from AriaQuanta.config import Config, get_array_module

#------------------------------------------------------------------------------------
np = get_array_module(Config.use_gpu)

#------------------------------------------------------------------------------------
def is_unitary(matrix):
    return np.allclose(matrix @ matrix.conj().T, np.eye(matrix.shape[0]), atol=1e-10)

#------------------------------------------------------------------------------------
def swap_qubits(idx1_, idx2_, num_of_qubits, multistate):

    idx1 = min(idx1_, idx2_)
    idx2 = max(idx1_, idx2_)

    indices_swaped = []
    size = 2 ** num_of_qubits
    
    #---------------------------------
    for i in range(size):

        state_str = format(i, '0{}b'.format(num_of_qubits))
        #print('-----------')
        #print(state_str)

        new_state_str = state_str[:idx1] + state_str[idx2] + state_str[idx1+1:]
        new_state_str = new_state_str[:idx2] + state_str[idx1] + new_state_str[idx2+1:]

        #print(new_state_str)
        
        index_swaped = int(new_state_str, 2)

        #print(index_original, index_swaped)
        indices_swaped.append(index_swaped)

    multistate_swaped = multistate[indices_swaped]
    return multistate_swaped

#------------------------------------------------------------------------------------
def swap_qubits_density(idx1, idx2, num_of_qubits, density_matrix):

    indices_swaped = []
    size = 2 ** num_of_qubits
    
    #---------------------------------
    for i in range(size):

        state_str = format(i, '0{}b'.format(num_of_qubits))
        #print('-----------')
        #print(state_str)

        new_state_str = state_str[:idx1] + state_str[idx2] + state_str[idx1+1:]
        new_state_str = new_state_str[:idx2] + state_str[idx1] + new_state_str[idx2+1:]

        #print(new_state_str)
        
        index_swaped = int(new_state_str, 2)

        #print(index_original, index_swaped)
        indices_swaped.append(index_swaped)

    density_matrix_swaped = density_matrix
    density_matrix_swaped = density_matrix_swaped[:,indices_swaped]
    density_matrix_swaped = density_matrix_swaped[indices_swaped,:]

    return density_matrix_swaped

def reorder_state(state):
    num_of_states = np.shape(state)[0]
    num_of_qubits = int(np.log2(num_of_states)) 

    bin_format = '#0' + str(num_of_qubits + 2) + 'b' # #05b
    all_states = [format(x, bin_format)[2:] for x in range(num_of_states)]
    all_states = [x[::-1] for x in all_states]
    #print(all_states) # ['00', '10', '01', '11']
    #                    [q1=0 q0=0, q1=1 q0=0, q1=0 q0=1, q1=1 q0=1]  
    new_indices = [int(x, 2) for x in all_states]
    reordered_state = state[new_indices]
    return reordered_state