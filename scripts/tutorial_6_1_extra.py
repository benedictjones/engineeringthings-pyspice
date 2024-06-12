# Top Matter
import numpy as np
import matplotlib.pyplot as plt
import sys
import os
import math

# Required for plotting in WSL
import matplotlib
matplotlib.use('Agg')

import PySpice
import PySpice.Logging.Logging as Logging
from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import *


# Import bode tool
from PySpice.Plot.BodeDiagram import bode_diagram


# logger
logger = Logging.setup_logging()

# # change sim program location depending on system
if sys.platform == "linux" or sys.platform == "linux2":
    PySpice.Spice.Simulation.CircuitSimulator.DEFAULT_SIMULATOR = 'ngspice-subprocess'  # needed for linux
elif sys.platform == "win32":
    pass

#

#

# # create the circuit
circuit = Circuit("Tutorial 6")

# # add components to the circuit

Vac = circuit.SinusoidalVoltageSource('input', 'n1', circuit.gnd, amplitude=1@u_V, frequency=100@u_Hz)
circuit.R(1, 'n1', 'n2', 1@u_kOhm)
circuit.C(1, 'n2', circuit.gnd, 1@u_uF)
circuit.Diode(1, 'n2', 'n3', model='MyDiode')
circuit.R(2, 'n3', circuit.gnd, 1@u_kOhm)

circuit.model('MyDiode', 'D', IS=4.352@u_nA, RS=0.6458@u_Ohm, BV=110@u_V, IBV=0.0001@u_V, N=1.906)

print(circuit)
# # Run analysis # #

simulator = circuit.simulator(temperature=25, nominal_temperature=25)

"""# # DC
analysis = simulator.dc(Vinput=slice(-3,3,0.1))
fig = plt.figure()
plt.plot(np.array(analysis["n1"]), np.array(analysis["n2"]), label='V(n2)')
plt.plot(np.array(analysis["n1"]), np.array(analysis["n3"]), label='V(n3)')
plt.legend()
plt.xlabel("Input Voltage (node 1)")
plt.ylabel("Output Voltage")"""


# # Trans
analysis = simulator.transient(step_time=Vac.period/1000, end_time=Vac.period)

print("Node:", str(analysis["n1"]), "Values:", np.array(analysis["n1"]))
print("Node:", str(analysis["n2"]), "Values:", np.array(analysis["n2"]))
print("Time Values:", np.array(analysis.time))

fig = plt.figure()
plt.plot(np.array(analysis.time), np.array(analysis["n1"]), label='V(n1)')
plt.plot(np.array(analysis.time), np.array(analysis["n2"]), label='V(n2)')
plt.plot(np.array(analysis.time), np.array(analysis["n3"]), label='V(n3)')
plt.legend()
plt.xlabel("Time")
plt.ylabel("Voltage")




# # Save to a file
fig.savefig("Sim_Output.png", dpi=300)
plt.close(fig)

#

# fin
