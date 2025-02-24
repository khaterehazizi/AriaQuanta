
#import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

from AriaQuanta._utils import np
import math

class CircuitVisualizer:
    gate_plotters = {}

    def __init__(self, circuit):
        self.circuit = circuit

    def visualize(self):
        circuit = self.circuit
        gates = circuit.gates
        size = circuit.size
        num_of_qubits = circuit.num_of_qubits

        fig, ax = plt.subplots(figsize=(size*1.4, num_of_qubits*0.9))

        for i in range(num_of_qubits):
            xx = np.arange(-0.5, size*1.1)
            qubit_i = np.ones(xx.shape) * i
            ax.plot(xx, qubit_i, 'k--')
            ax.text(-1.0, i, f'Q{i}:', fontsize=12, ha='center', va='center')

        for i in range(size):
            gate_i = gates[i]
            gate_i_name = gate_i.name
            #gate_i_qubits = gate_i.qubits
            if gate_i_name == 'If_cbit':
                gate_i = gate_i.operation_gate
            plot_func = self.gate_plotters.get(gate_i_name, plot_default)
            plot_func(ax, i, gate_i)

        #ax.set_xlim(-1.5, size + 1)
        #ax.set_ylim(-0.5, num_of_qubits)
        ax.invert_yaxis()
        plt.xlabel('Gate Sequence')
        plt.ylabel('Qubits')
        #plt.title('Quantum Circuit Visualization')
        plt.axis('off')
        ax.margins(x=0.15, y=0.15)
        plt.show()

        return fig, ax

#------------------------------------------------------------------------------------
#/////////////////////////////// General Plots ///////////////////////////////
#------------------------------------------------------------------------------------
def plot_default(ax, i, gate_i):
    for q in gate_i.qubits:
        ax.text(i, q, gate_i.name, fontsize=12, ha='center', va='center',
                bbox=dict(boxstyle='round,pad=0.5', edgecolor='black', facecolor='lightblue'))

@staticmethod
def register_gate_plotter(gate_name):
    def decorator(func):
        CircuitVisualizer.gate_plotters[gate_name] = func
        return func
    return decorator

#------------------------------------------------------------------------------------
#/////////////////////////////// GateSingleQubit ///////////////////////////////
#------------------------------------------------------------------------------------
# Default:
# I, X, Y, Z, H, S, T
# Others:
# Ph, Xsqrt, P, RX, RY, RZ, Rot

#------------------------------------------------------------------------------------
@register_gate_plotter('GPh')
def plot_gate(ax, i, gate_i):
    gate_i_name = gate_i.name
    gate_i_qubits = gate_i.qubits
    delta = gate_i.delta
    this_text = '{}({:0.2f})'.format(gate_i_name, delta)
    for q in gate_i_qubits:
        ax.text(i, q, this_text, fontsize=12, ha='center', va='center',
                bbox=dict(boxstyle='round,pad=0.5', edgecolor='black', facecolor='lightblue'))

#------------------------------------------------------------------------------------
@register_gate_plotter('Xsqrt')
def plot_gate(ax, i, gate_i):
    gate_i_name = gate_i.name
    gate_i_qubits = gate_i.qubits
    this_text = r'$\sqrt{X}$'
    for q in gate_i_qubits:
        ax.text(i, q, this_text, fontsize=12, ha='center', va='center',
                bbox=dict(boxstyle='round,pad=0.5', edgecolor='black', facecolor='lightblue'))

#------------------------------------------------------------------------------------
@register_gate_plotter('P')
def plot_gate(ax, i, gate_i):
    gate_i_name = gate_i.name
    gate_i_qubits = gate_i.qubits
    phi = gate_i.phi
    this_text = '{}({:0.2f})'.format(gate_i_name, phi)
    for q in gate_i_qubits:
        ax.text(i, q, this_text, fontsize=12, ha='center', va='center',
                bbox=dict(boxstyle='round,pad=0.5', edgecolor='black', facecolor='lightblue'))

#------------------------------------------------------------------------------------
@register_gate_plotter('RX')
@register_gate_plotter('RY')
@register_gate_plotter('RZ')
def plot_gate(ax, i, gate_i):
    gate_i_name = gate_i.name
    gate_i_qubits = gate_i.qubits
    theta = gate_i.theta

    gate_i_type = gate_i_name[1:]
    name = '$R_{%s}$' %(gate_i_type)
    this_text = '{}\n({:0.2f})'.format(name, theta)

    for q in gate_i_qubits:
        ax.text(i, q, this_text, fontsize=12, ha='center', va='center',
                bbox=dict(boxstyle='round,pad=0.5', edgecolor='black', facecolor='lightblue'))

#------------------------------------------------------------------------------------
@register_gate_plotter('Rot')
def plot_gate(ax, i, gate_i):
    gate_i_name = gate_i.name
    gate_i_qubits = gate_i.qubits
    theta = gate_i.theta
    phi = gate_i.phi 
    lambda_ = gate_i.lambda_
    this_text = '{}\n({:0.2f},{:0.2f},{:0.2f})'.format('U', theta, phi, lambda_)
    for q in gate_i_qubits:
        ax.text(i, q, this_text, fontsize=11, ha='center', va='center',
                bbox=dict(boxstyle='round,pad=0.5', edgecolor='black', facecolor='lightblue'))
                                        
#------------------------------------------------------------------------------------
#/////////////////////////////// GateDoubleQubit ///////////////////////////////
#   /////////////////////////////// SWAP Gates ///////////////////////////////
#------------------------------------------------------------------------------------
# SWAP, ISWAP, SWAPsqrt, ISWAPsqrt, SWAPalpha

#------------------------------------------------------------------------------------
@register_gate_plotter('SWAP')
def plot_gate(ax, i, gate_i): 
    gate_i_name = gate_i.name
    gate_i_qubits = gate_i.qubits
    ax.plot([i, i], gate_i_qubits, 'm')
    ax.plot(i, gate_i_qubits[0], 'mx', markersize=14)
    ax.plot(i, gate_i_qubits[1], 'mx', markerfacecolor='None', markersize=14)

#------------------------------------------------------------------------------------
@register_gate_plotter('ISWAP')
def plot_gate(ax, i, gate_i): 
    gate_i_name = gate_i.name
    gate_i_qubits = gate_i.qubits
    ax.plot([i, i], gate_i_qubits, 'm')
    ax.plot(i, gate_i_qubits[0], 'ms', markersize=14)
    ax.plot(i, gate_i_qubits[0], 'wx', markerfacecolor='None', markersize=14)    
    ax.plot(i, gate_i_qubits[1], 'ms', markersize=14)
    ax.plot(i, gate_i_qubits[1], 'wx', markerfacecolor='None', markersize=14)

#------------------------------------------------------------------------------------
@register_gate_plotter('SWAPsqrt')
def plot_gate(ax, i, gate_i): 
    gate_i_name = gate_i.name
    gate_i_qubits = gate_i.qubits
    ax.plot([i, i], gate_i_qubits, 'm')
    ax.plot(i, gate_i_qubits[0], 'mx', markersize=14)
    ax.plot(i, gate_i_qubits[1], 'mx', markerfacecolor='None', markersize=14)
    this_text = '1/2'
    ax.text(i, (gate_i_qubits[0]+gate_i_qubits[1])/2, this_text, fontsize=10, ha='center', va='center',
                bbox=dict(boxstyle=f"circle,pad=0.5", edgecolor='black', facecolor='#DDA0DD'))

#------------------------------------------------------------------------------------
@register_gate_plotter('ISWAPsqrt')
def plot_gate(ax, i, gate_i): 
    gate_i_name = gate_i.name
    gate_i_qubits = gate_i.qubits
    ax.plot([i, i], gate_i_qubits, 'm')
    ax.plot(i, gate_i_qubits[0], 'ms', markersize=14)
    ax.plot(i, gate_i_qubits[0], 'wx', markerfacecolor='None', markersize=14)    
    ax.plot(i, gate_i_qubits[1], 'ms', markersize=14)
    ax.plot(i, gate_i_qubits[1], 'wx', markerfacecolor='None', markersize=14)
    this_text = '1/2'
    ax.text(i, (gate_i_qubits[0]+gate_i_qubits[1])/2, this_text, fontsize=10, ha='center', va='center',
                bbox=dict(boxstyle=f"circle,pad=0.5", edgecolor='black', facecolor='#DDA0DD'))
        
#------------------------------------------------------------------------------------
@register_gate_plotter('SWAPalpha')
def plot_gate(ax, i, gate_i): 
    gate_i_name = gate_i.name
    gate_i_qubits = gate_i.qubits
    alpha = gate_i.alpha
    ax.plot([i, i], gate_i_qubits, 'm')
    ax.plot(i, gate_i_qubits[0], 'mx', markersize=14)
    ax.plot(i, gate_i_qubits[1], 'mx', markerfacecolor='None', markersize=14)
    this_text = '{:0.2f}'.format(alpha)
    #print(this_text)
    ax.text(i, (gate_i_qubits[0]+gate_i_qubits[1])/2, this_text, fontsize=10, ha='center', va='center',
                bbox=dict(boxstyle=f"circle,pad=0.5", edgecolor='black', facecolor='#DDA0DD'))

#------------------------------------------------------------------------------------
#/////////////////////////////// GateDoubleQubit ///////////////////////////////
#////////////////////////////// Rotational Gates ///////////////////////////////
#------------------------------------------------------------------------------------
# RXX, RYY, RZZ, RXY

#------------------------------------------------------------------------------------
@register_gate_plotter('RXX')
@register_gate_plotter('RYY')
@register_gate_plotter('RZZ')
@register_gate_plotter('RXY')
def plot_gate(ax, i, gate_i):
    gate_i_name = gate_i.name
    gate_i_qubits = gate_i.qubits
    phi = gate_i.phi

    gate_i_type = gate_i_name[1:]
    name = '$R_{%s}$' %(gate_i_type)
    
    angle_phi = round(phi / np.pi)

    this_text_1 = '%s'%(name)
    
    this_text_2 = r'(%.2f$\pi$)'%(angle_phi)    

    
    q_min = min(gate_i_qubits)
    q_max = max(gate_i_qubits)
    height = abs(gate_i_qubits[1]- gate_i_qubits[0]) + 0.8
    width = 0.8
    rect = Rectangle((i-0.4, q_min - 0.4), width, height, facecolor='#DDA0DD', zorder=2, edgecolor='k')
    ax.add_patch(rect)

    ax.text(i-0.4 + 0.5*width, q_min-0.1, str(q_min),
        horizontalalignment='center',
        verticalalignment='top',
        fontsize=12, color='k')

    ax.text(i-0.4 + 0.5*width, (q_min + q_max)/2, this_text_1,
        horizontalalignment='center',
        verticalalignment='center',
        fontsize=12, color='k')

    ax.text(i-0.4 + 0.5*width, (q_min + q_max)/2 + 0.3, this_text_2,
        horizontalalignment='center',
        verticalalignment='center',
        fontsize=12, color='k')
            
    ax.text(i-0.4 + 0.5*width, q_max+0.1, str(q_max),
        horizontalalignment='center',
        verticalalignment='bottom',
        fontsize=12, color='k')

#------------------------------------------------------------------------------------
#/////////////////////////////// GateDoubleQubit ////////////////////////////////
#//////////////////////////////  Other 2-qubit Gates ////////////////////////////
#------------------------------------------------------------------------------------
# Barenco, Berkeley, Canonical, Givens, Magic

#------------------------------------------------------------------------------------
@register_gate_plotter('Barenco')
@register_gate_plotter('Berkeley')
@register_gate_plotter('Canonical')
@register_gate_plotter('Givens')
@register_gate_plotter('Magic')
def plot_gate(ax, i, gate_i):
    gate_i_name = gate_i.name
    gate_i_qubits = gate_i.qubits

    gate_i_name_abbr = {'Barenco':'Brn', 'Berkeley':'Brk', 'Canonical':'Can',
                        'Givens':'Gvn', 'Magic':'Mgc'}
    
    this_text = gate_i_name_abbr[gate_i_name]

    q_min = min(gate_i_qubits)
    q_max = max(gate_i_qubits)
    height = abs(gate_i_qubits[1]- gate_i_qubits[0]) + 0.8
    width = 0.8
    rect = Rectangle((i-0.4, q_min - 0.4), width, height, facecolor='#DDA0DD', zorder=2, edgecolor='k')
    ax.add_patch(rect)

    ax.text(i-0.4 + 0.5*width, q_min-0.1, str(q_min),
        horizontalalignment='center',
        verticalalignment='top',
        fontsize=12, color='k')

    ax.text(i-0.4 + 0.5*width, (q_min + q_max)/2, this_text,
        horizontalalignment='center',
        verticalalignment='center',
        fontsize=12, color='k')
    
    ax.text(i-0.4 + 0.5*width, q_max+0.1, str(q_max),
        horizontalalignment='center',
        verticalalignment='bottom',
        fontsize=12, color='k')


#------------------------------------------------------------------------------------
#/////////////////////////////// GateTripleQubit ///////////////////////////////
#------------------------------------------------------------------------------------
# CCX (Toffoli), RCCX (Margolus), CSWAP(Fredkin) 

#------------------------------------------------------------------------------------
@register_gate_plotter('CCX')
def plot_gate(ax, i, gate_i):
    gate_i_name = gate_i.name
    gate_i_qubits = gate_i.qubits
    ax.plot(i, gate_i_qubits[0], 'ko', markersize=14)
    ax.plot(i, gate_i_qubits[1], 'ko', markersize=14)
    ax.plot(i, gate_i_qubits[2], 'ko', markerfacecolor='None', markersize=20)
    ax.plot(i, gate_i_qubits[2], 'k+', markerfacecolor='None', markersize=20)
    ax.plot([i, i, i], gate_i_qubits, 'k')

#------------------------------------------------------------------------------------
@register_gate_plotter('RCCX')
def plot_gate(ax, i, gate_i):
    gate_i_name = gate_i.name
    gate_i_qubits = gate_i.qubits

    this_text = gate_i_name
    gate_i_qubits_sort = sorted(gate_i_qubits)


    q_min = gate_i_qubits_sort[0]
    q_max = gate_i_qubits_sort[2]
    height = abs(q_max - q_min) + 0.8
    width = 0.8
    rect = Rectangle((i-0.4, q_min - 0.4), width, height, facecolor='#d4d2d2', zorder=2, edgecolor='k')
    ax.add_patch(rect)

    ax.text(i-0.4 + 0.1*width, gate_i_qubits_sort[0]-0.1, str(gate_i_qubits_sort[0]),
        horizontalalignment='left',
        verticalalignment='top',
        fontsize=12, color='k')
    
    ax.text(i-0.4 + 0.1*width, gate_i_qubits_sort[1], str(gate_i_qubits_sort[1]),
        horizontalalignment='left',
        verticalalignment='center',
        fontsize=12, color='k')
    
    ax.text(i-0.4 + 0.1*width, gate_i_qubits_sort[2]+0.1, str(gate_i_qubits_sort[2]),
        horizontalalignment='left',
        verticalalignment='bottom',
        fontsize=12, color='k')
    
    ax.text(i-0.4 + 0.6*width, (q_min + q_max)/2, this_text,
        horizontalalignment='center',
        verticalalignment='center',
        fontsize=12, color='k', rotation=90)

#------------------------------------------------------------------------------------
@register_gate_plotter('CSWAP')
def plot_gate(ax, i, gate_i):
    gate_i_name = gate_i.name
    gate_i_qubits = gate_i.qubits
    ax.plot(i, gate_i_qubits[0], 'ko', markersize=14)
    ax.plot(i, gate_i_qubits[1], 'kx', markersize=14)
    ax.plot(i, gate_i_qubits[2], 'kx', markersize=14)
    ax.plot([i, i, i], gate_i_qubits, 'k')


#------------------------------------------------------------------------------------
#/////////////////////////////// GateControlQubit ///////////////////////////////
#------------------------------------------------------------------------------------
# CX, CZ, CP,
# CS, CSX, CU

#------------------------------------------------------------------------------------
@register_gate_plotter('CX')  # o---+o
def plot_gate(ax, i, gate_i):
    gate_i_name = gate_i.name
    gate_i_qubits = gate_i.qubits
    mycolor = '#407a28'

    ax.plot(i, gate_i_qubits[0], 'o', color=mycolor, markersize=12)
    ax.plot(i, gate_i_qubits[1], 'o', color=mycolor, markerfacecolor='None', markersize=20)
    ax.plot(i, gate_i_qubits[1], '+', color=mycolor, markerfacecolor='None', markersize=20)
    ax.plot([i, i], gate_i_qubits, color=mycolor)      

#------------------------------------------------------------------------------------
@register_gate_plotter('CZ')    # o----o
def plot_gate(ax, i, gate_i):
    gate_i_name = gate_i.name
    gate_i_qubits = gate_i.qubits
    mycolor = '#407a28'

    ax.plot(i, gate_i_qubits[0], 'o', color=mycolor, markersize=12)
    ax.plot(i, gate_i_qubits[1], 'o', color=mycolor, markersize=12)
    ax.plot([i, i], gate_i_qubits, color=mycolor)  

#------------------------------------------------------------------------------------
@register_gate_plotter('CP')    # o----P(phi)
def plot_gate(ax, i, gate_i):
    gate_i_name = gate_i.name
    gate_i_qubits = gate_i.qubits
    phi = gate_i.phi
    mycolor = '#407a28'

    ax.plot(i, gate_i_qubits[0], 'o', color=mycolor, markersize=12)
    ax.plot([i, i], gate_i_qubits, color=mycolor)  

    this_text = 'P\n({:0.2f})'.format(phi)
    ax.text(i, gate_i_qubits[1], this_text, fontsize=12, ha='center', va='center',
        bbox=dict(boxstyle='round,pad=0.4', edgecolor=mycolor, facecolor='white'))

#------------------------------------------------------------------------------------
@register_gate_plotter('CS')   # o----S, o----sqrt(X)
@register_gate_plotter('CSX')
def plot_gate(ax, i, gate_i):
    gate_i_name = gate_i.name
    gate_i_qubits = gate_i.qubits
    mycolor = '#407a28'

    ax.plot(i, gate_i_qubits[0], 'o', color=mycolor, markersize=12)
    ax.plot([i, i], gate_i_qubits, color=mycolor) 

    text_sqrt_X = r'$\sqrt{X}$'
    this_text = {'CS':'S', 'CSX':text_sqrt_X}
    ax.text(i, gate_i_qubits[1], this_text[gate_i_name], fontsize=12, ha='center', va='center',
        bbox=dict(boxstyle='round,pad=0.4', edgecolor=mycolor, facecolor='white'))

#------------------------------------------------------------------------------------
@register_gate_plotter('CU')
def plot_gate(ax, i, gate_i):
    gate_i_qubits = gate_i.qubits
    gate_i_controls = gate_i.control_qubits
    gate_i_targets = gate_i.target_qubits

    #this_text = 'c-U\n(c: Q%d)' % gate_i.control_qubits
    this_text = gate_i.namedraw  #gate_i.name
    
    mycolor= '#ffa621' #'#ebe2c7'   # green: '#aee6a8'

    ax.plot(i, gate_i_controls, 'o', color=mycolor, markersize=12)
    ax.plot([i, i], gate_i_qubits, color=mycolor) 


    q_min = gate_i_qubits[1]
    q_max = max(gate_i_qubits)

    #print(gate_i_controls, gate_i_targets)
    height = abs(q_max - q_min) + 0.8
    width = 0.8
    rect = Rectangle((i-0.4, q_min - 0.4), width, height, facecolor=mycolor, zorder=2, edgecolor='k')
    ax.add_patch(rect)
    
    ax.text(i-0.4 + 0.5*width, (q_min + q_max)/2, this_text,
        horizontalalignment='center',
        verticalalignment='center',
        fontsize=12) #, rotation=90)
    
#------------------------------------------------------------------------------------
#/////////////////////////////// GateCustom ///////////////////////////////
#------------------------------------------------------------------------------------
# Custom, CNZ
#------------------------------------------------------------------------------------
@register_gate_plotter('Custom')
def plot_gate(ax, i, gate_i):
    gate_i_name = gate_i.name
    gate_i_qubits = gate_i.qubits

    this_text = 'U'

    mycolor= '#ebe2c7'   # green: '#aee6a8'
    q_min = min(gate_i_qubits)
    q_max = max(gate_i_qubits)
    height = abs(q_max - q_min) + 0.8
    width = 0.8
    rect = Rectangle((i-0.4, q_min - 0.4), width, height, facecolor=mycolor, zorder=2, edgecolor='k')
    ax.add_patch(rect)
    
    ax.text(i-0.4 + 0.5*width, (q_min + q_max)/2, this_text,
        horizontalalignment='center',
        verticalalignment='center',
        fontsize=12)

#------------------------------------------------------------------------------------
@register_gate_plotter('CNZ')    # o----o----o----o
def plot_gate(ax, i, gate_i):
    gate_i_name = gate_i.name
    gate_i_qubits = gate_i.qubits
    mycolor = '#407a28'
    
    for j in range((max(gate_i_qubits)+1)):
        ax.plot(i, j, 'o', color=mycolor, markersize=12)
    ax.plot([i, i], [0, j], color=mycolor)  

# Example usage
# Assuming you have a Circuit class and an instance of it
# circuit = Circuit(...)
# visualizer = CircuitVisualizer(circuit)
# visualizer.visualize()

#------------------------------------------------------------------------------------
@register_gate_plotter('MeasureQubit')
def plot_gate(ax, i, gate_i):
    mycolor = "#ededed"


    t = np.linspace(0, 2*math.pi, 100)
    for q in gate_i.qubits:
        ax.text(i, q, u"\u2197", fontsize=27, ha='center', va='center')
        #ax.text(i, q+0.1, u"\u25e0", fontsize=20, ha='center', va='center')

        height = 0.8
        width = 0.8
        rect = Rectangle((i-0.4, q-0.4), width, height, facecolor='white', zorder=2, edgecolor='k')
        ax.add_patch(rect)

        u=i       #x-position of the center
        v=q+0.25        #y-position of the center
        a=0.32     #radius on the x-axis
        b=0.22      #radius on the y-axis
        xx = u+a*np.cos(t)
        yy = v+b*np.sin(t)
        idx = yy < v
        ax.plot( xx[idx] , yy[idx], color = 'black' )
