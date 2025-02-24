
from AriaQuanta._utils import np

#------------------------------------------------------------------------------------
class Job():
    def __init__(self, job_id):
        self.job_id = job_id
        self.status = 'Job %s not yet started'.format(self.job_id)
        
        #self.q_values = {}   # {'0': 1, '1': 1}
        #self.c_values = {}   # {'c0': 1, 'c1': 1}
        #self.qc_values = []  # list of tuples

    def job_run(self, qc, density):

        self.status = 'Job {} started'.format(self.job_id)
        
        #if self.job_id % 50 == 0:
        #    print(self.status)

        this_qc = qc.copy()
        this_qc.run()

        """
        num_of_qubits = circuit.num_of_qubits
        this_qc = Circuit(num_of_qubits)
        this_qc.gates = circuit.gates
        state = this_qc.statevector
        this_qc.density_matrix = circuit.density_matrix


        if density == False:
            c_values_dict_whole_run = {}
            q_values_dict_whole_run = {}
            qc_values_tuple_whole_run = []

            for gate in this_qc.gates:
                # print(gate)
                if isinstance(gate, MeasureQubit):
                    state = gate.apply(this_qc.num_of_qubits, this_qc.statevector)

                    # c_values_dict: {'c0': 1, 'c1': 1}
                    c_values_dict = gate.c_values_dict
                    c_values_dict_whole_run = {**c_values_dict_whole_run, **c_values_dict}

                    # q_values_dict: {'0': 1, '1': 1}
                    q_values_dict = gate.q_values_dict
                    q_values_dict_whole_run = {**q_values_dict_whole_run, **q_values_dict}

                    # qc_values: [(q_bit, 'c_bit', value)]
                    qc_values = gate.qc_values
                    qc_values_tuple_whole_run.append(qc_values)

                elif isinstance(gate, If_cbit):
                    # print(dir(gate))
                    condition = gate.condition
                    # print(c_values_dict[condition[0]], condition[1])
                    if c_values_dict[condition[0]] == condition[1]:
                        # print('yes')
                        state = gate.apply(this_qc.num_of_qubits, this_qc.statevector)

                else:
                    state = gate.apply(this_qc.num_of_qubits, this_qc.statevector)
        
                # Apply noise
                #if this_qc.noise_type:
                #    state = this_qc.noise_type.apply_noise(this_qc.num_of_qubits, this_qc.statevector, density)

                this_qc.statevector = state

            # print(qc_values_tuple_whole_run)
            # print(c_values_dict_whole_run)
            # print(q_values_dict_whole_run)

            self.q_values = q_values_dict_whole_run
            self.c_values = c_values_dict_whole_run
            self.qc_values = qc_values_tuple_whole_run
        
        elif density == True:
            for gate in this_qc.gates:
                state = gate.apply_density(this_qc.num_of_qubits, this_qc.density_matrix)

                this_qc.density_matrix = state
        """

        self.status = 'Job {} completed'.format(self.job_id)

        #if self.job_id % 50 == 0:
        #    print(self.status) 
                   
        return this_qc.statevector, this_qc.measurequbit_values
        
        
        
