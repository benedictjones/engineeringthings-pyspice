# Top Matter
import numpy as np
import matplotlib.pyplot as plt
import sys
import os

# Required for plotting in WSL
import matplotlib
matplotlib.use('Agg')

import PySpice
import PySpice.Logging.Logging as Logging
from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import *

from PySpice.Spice.Library import SpiceLibrary


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
circuit = Circuit('Tutorial 5_1')

# # add components to the circuit
circuit.V('input', 1, circuit.gnd, 10@u_V)
circuit.R(1, 2, circuit.gnd, 1@u_kOhm)  # @u_kΩ is a unit of kOhms


''' # # # # Method 0 - Locally Defined # # # #
'''
"""
circuit.model('MyDiode', 'D', IS=4.352@u_nA, RS=0.6458@u_Ohm, BV=110@u_V, IBV=0.0001@u_V, N=1.906)  # Define the 1N4148PH (Signal Diode)
circuit.Diode(1, 1, 2, model='MyDiode')
#"""

#

''' # # # # Method 1 - Does not work?! # # # #
A library is a directory which is recursively scanned for ‘.lib’ file and
parsed for sub-circuit and models definitions.
    > spice_library = SpiceLibrary('/some/path/')
    > To retrieve the file path use: spice_library['device'] (where name is device.lib)
'''
"""
spice_library = SpiceLibrary('/lib/')
circuit.include(spice_library['1n4148'])
circuit.X('importDiode', '1N4148', 1, 2)
#"""

#

''' # # # # Method 2 # # # #
Use circuit.include() from the pyspice functions
'''
"""
pathh = "lib/1N4148.lib"
circuit.include(pathh)  # this adds the system path to the start!!
circuit.X('importDiode', '1N4148', 1, 2)
#"""

#

''' # # # # Method 3 # # # #
The best way is the normal netlist way!
'''
#"""
new_line = ".include lib/1n4148.lib"
circuit.raw_spice += new_line + os.linesep
circuit.X('importDiode', '1N4148', 1, 2)
#"""

#

#

# # print the circuit:
print("The Circuit/Netlist:\n\n", circuit)

# # create a simulator object (with paramaters e.g temp)
simulator = circuit.simulator(temperature=25, nominal_temperature=25)

# # print the circuit + simulator details:
# print("The simulator:\n\n", simulator)

# # Run analysis
# analysis = simulator.operating_point()
analysis = simulator.dc(Vinput=slice(-3, 3, 0.01)) # slice = start:step:stop (inclusive)


# # Print Outputs
# print("Node:", str(analysis["1"]), "Values:", np.array(analysis["1"]))
# print("Node:", str(analysis["2"]), "Values:", np.array(analysis["2"]))

# # Plot Output
fig = plt.figure()
plt.plot(np.array(analysis["1"]), np.array(analysis["2"]))
plt.xlabel("Input Voltage (node 1)")
plt.ylabel("Output Voltage (node 2)")

fig.savefig("Sim_Output.png", dpi=300)
plt.close(fig)

# plt.show()  # haven't set up on WSL



"""
Warning!! The path name must not have a gap in it.
I had this problem with oneDrive for bunisess which has a path:
    .../Onedrive - Business/folder/...
"""


# fin
