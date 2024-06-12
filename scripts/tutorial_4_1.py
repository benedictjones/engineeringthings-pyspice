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

"""
###############################################################################
# # Make a Circuit with a diode # #
###############################################################################
"""

# # create the circuit
circuit = Circuit('Tutorial 4_1')


# # Define the 1N4148PH (Signal Diode)
circuit.model('MyDiode', 'D', IS=4.352@u_nA, RS=0.6458@u_Ohm, BV=110@u_V, IBV=0.0001@u_V, N=1.906)

# # add components to the circuit
circuit.V('input', 1, circuit.gnd, 10@u_V)
circuit.Diode(1, 1, 2, model='MyDiode')
circuit.R(1, 2, circuit.gnd, 1@u_kOhm)  # @u_kΩ is a unit of kOhms


# # print the circuit:
print("The Circuit/Netlist:\n\n", circuit)


# # create a simulator object (with paramaters e.g temp)
simulator = circuit.simulator(temperature=25, nominal_temperature=25)


# # print the circuit + simulator details:
#print("The simulator:\n\n", simulator)

# # Run analysis
analysis = simulator.operating_point()

# slice = start:step:stop (inclusive)
analysis = simulator.dc(Vinput=slice(0, 5, 0.1))


# # Print Outputs
print("Node:", str(analysis["1"]), "Values:", np.array(analysis["1"]))
print("Node:", str(analysis["2"]), "Values:", np.array(analysis["2"]))


fig = plt.figure()

plt.plot(np.array(analysis["1"]), np.array(analysis["2"]))
plt.xlabel("Input Voltage (node 1)")
plt.ylabel("Output Voltage (node 2)")


fig.savefig("Sim_Output.png", dpi=300)
plt.close(fig)

plt.show()  # haven't set up on WSL




# fin
