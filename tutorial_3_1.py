# Top Matter
import numpy as np
import matplotlib.pyplot as plt
import sys

# Required for plotting in WSL
import matplotlib
matplotlib.use('Agg')

import PySpice
import PySpice.Logging.Logging as Logging
from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import *



logger = Logging.setup_logging()

# # change sim program location depending on system
if sys.platform == "linux" or sys.platform == "linux2":
    PySpice.Spice.Simulation.CircuitSimulator.DEFAULT_SIMULATOR = 'ngspice-subprocess'  # needed for linux
elif sys.platform == "win32":
    # You will get logging errors/warning, but is should work
    pass

#

#

# # Function


def format_output(analysis):
    '''
    Gets dictionary containing SPICE sim values.
    The dictionary is created by pairing each of the nodes to its corresponding
    output voltage value array.
    This provides a more managable format.
    '''

    sim_res_dict = {}  # create dictionary

    # loop though nodes
    for node in analysis.nodes.values():
        data_label = "%s" % str(node)  # extract node name
        sim_res_dict[data_label] = np.array(node)  # save node value/array of values

    return sim_res_dict






"""
###############################################################################
# # Make a Circuit with a diode # #
###############################################################################
"""

# # create the circuit
circuit = Circuit('Voltage Divider')


# # Define the 1N4148PH (Signal Diode)
circuit.model('MyDiode', 'D', IS=4.352@u_nA, RS=0.6458@u_Ohm, BV=110@u_V, IBV=0.0001@u_V, N=1.906)

# # add components to the circuit
circuit.V('input', 1, circuit.gnd, 10@u_V)
circuit.R(1, 1, 2, 9@u_kOhm)  # @u_kΩ is a unit of kOhms

circuit.Diode(1, 2, 3, model='MyDiode')

circuit.R(2, 3, circuit.gnd, 1@u_kOhm)
circuit.Diode(2, 3, circuit.gnd, model='MyDiode')
#circuit.Diode(2, 3, circuit.gnd, raw_spice='MyDiode')
#self.raw_spice = 'D2 2 3 MyDiode' + os.linesep


# # print the circuit:
print("The Circuit/Netlist:\n\n", circuit)


# # create a simulator object (with paramaters e.g temp)
simulator = circuit.simulator(temperature=25, nominal_temperature=25)


# # print the circuit + simulator details:
#print("The simulator:\n\n", simulator)

# # Run analysis
analysis = simulator.operating_point()

out_dict = format_output(analysis)


print(out_dict)








# fin
