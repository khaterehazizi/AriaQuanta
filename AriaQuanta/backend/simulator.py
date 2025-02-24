
# from functools import partial
import os
import timeit
import concurrent.futures

from AriaQuanta.backend.job import Job
from AriaQuanta.backend.result import Result, ResultDensity

from AriaQuanta._utils import np, Config

#------------------------------------------------------------------------------------
class Simulator():

    def __init__(self):
        self.circuit = 'None'
        self.iterations = 0

    def loop_run(self, job_id):
        this_job = Job(job_id)
        #state, output = this_job.job_run(self.circuit, self.density)
        state, measurequbit_values = this_job.job_run(self.circuit, self.density)
        return state, measurequbit_values

    def simulate(self, circuit, iterations, num_nodes=1, density=False):
        
        self.circuit = circuit
        self.iterations = iterations
        self.density = density

        #---------------------------------------

        statevector_all = [[]]*iterations
        output_all = [[]]*iterations
        list_iterations = [m for m in range(iterations)]

        hardware = Config.hardware
        if (hardware == 'Local'):
            #num_processors = os.cpu_count()
            #if(num_nodes != num_processors):
            #    print("The number of processors are: {}" .format(num_processors))
            #    print("For a better performance, set the number of nodes to the number of processors")      

            # Determine the optimal parallelization strategy
            #list_max_workers = [m for m in range(num_nodes)]
            #ExecutorClass, _ = choose_best_executor(self.loop_run, list_max_workers, max_workers=num_nodes)

            #print("ExecutorClass:", ExecutorClass)

            # Run the function with the chosen executor
            #with ExecutorClass(max_workers=num_nodes) as executor:
            #    statevector_all = list(executor.map(self.loop_run, list_iterations))

            with concurrent.futures.ThreadPoolExecutor(max_workers=num_nodes) as executor:
                # Map the function over the list of numbers
                state_all_measurequbit_values_all = list(executor.map(self.loop_run, list_iterations))
                statevector_all, measurequbit_values_all = zip(*state_all_measurequbit_values_all)
                
                #statevector_all = list(executor.map(self.loop_run, list_iterations))


            #with concurrent.futures.ProcessPoolExecutor(max_workers=num_nodes) as executor:
            #    # Map the function over the list of numbers
            #    statevector_all = list(executor.map(self.loop_run, list_iterations))
            #             
            #for i in range(iterations):
            #    job_id = str(i).zfill(6)
            #    this_job = Job(job_id)
            #    state = this_job.job_run(circuit)
            #    statevector_all[i] = state
        
        if self.density == False:
            result = Result(statevector_all, circuit.num_of_qubits, circuit.num_of_ancilla, measurequbit_values_all)
        elif self.density == True:
            result = ResultDensity(statevector_all)    

        return result           

#------------------------------------------------------------------------------------       
def profile_executor(executor_class, function, iterable, max_workers):
    with executor_class(max_workers=max_workers) as executor:
        start_time = timeit.default_timer()
        list(executor.map(function, iterable))
        elapsed = timeit.default_timer() - start_time
    return elapsed

#------------------------------------------------------------------------------------
def choose_best_executor(function, iterable, max_workers=None):
    if max_workers is None:
        max_workers = os.cpu_count()  # Use number of CPU cores as default

    # Profile using ThreadPoolExecutor
    thread_time = profile_executor(concurrent.futures.ThreadPoolExecutor, function, iterable, max_workers)

    # Profile using ProcessPoolExecutor
    process_time = profile_executor(concurrent.futures.ProcessPoolExecutor, function, iterable, max_workers)

    # Choose the best executor
    if thread_time < process_time:
        #print(f"ThreadPoolExecutor is faster ({thread_time:.4f} seconds).")
        return concurrent.futures.ThreadPoolExecutor, thread_time
    else:
        #print(f"ProcessPoolExecutor is faster ({process_time:.4f} seconds).")
        return concurrent.futures.ProcessPoolExecutor, process_time
