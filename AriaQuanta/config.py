
import numpy as npnumpy
try:
    import cupy as npcupy
    cupy_exist = True
except ImportError:
    cupy_exist = False
    npcupy = None

#-----------------------------------------------------------------------------
class Config:

    hardware = 'Local'   # ['Local','HPC','Cloud','QPU']
    use_gpu = False 

    def set_use_gpu(this_use_gpu):
        if this_use_gpu == False:
            print('use_gpu is set to False. Running on CPU.')
        else:
            if cupy_exist:
                this_use_gpu = True
                print('use_gpu is set to True. Running on GPU.')
            else:
                print('use_gpu is set to True, but the requirements are not satisfied. Running on CPU.')    

        Config.use_gpu = this_use_gpu
    
def get_array_module(this_use_gpu):
    if this_use_gpu and (npcupy is not None):
        #print('Using CuPy')
        return npcupy
    else: 
        #print('Using NumPy')
        return npnumpy

#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
# print options
#class PrintOptions():
#
#    def set_PrintOptions_defaults():
#        PrintOptions.print_noise = False
#        PrintOptions.print_measure = False
#
#PrintOptions.set_PrintOptions_defaults()  