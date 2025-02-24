

class Operations:

    def __init__(self, name, conditions, operation_gate):
        
        self.name = name  
        self.conditions = conditions
        self.operation_gate = operation_gate
        self.qubits = operation_gate.qubits

    def apply(self, num_of_qubits, multistate):

        this_gate = self.operation_gate
        multistate = this_gate.apply(num_of_qubits, multistate)

        return multistate

#------------------------------------------------------------------------------------
class If_cbit(Operations):
    def __init__(self, conditions, operation_gate):
        super().__init__(name='If_cbit', conditions=conditions, operation_gate=operation_gate)
    
