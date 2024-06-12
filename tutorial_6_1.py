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


from PySpice.Plot.BodeDiagram import bode_diagram

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
circuit = Circuit('Tutorial 6_1')

# # add components to the circuit
#circuit.V('input', 'n1', circuit.gnd, 10@u_V)
Vac = circuit.SinusoidalVoltageSource('input', 'n1', circuit.gnd, amplitude=1@u_V, frequency=100@u_Hz)
R = circuit.R(1, 'n1', 'n2', 1@u_kOhm)  # @u_kΩ is a unit of kOhms
C = circuit.C(1, 'n2', circuit.gnd, 1@u_uF)
circuit.Diode(1, 'n2', 'n3', model='MyDiode')  # using cutom defined diode
circuit.R(2, 'n3', circuit.gnd, 1@u_kOhm)  # @u_kΩ is a unit of kOhms


circuit.model('MyDiode', 'D', IS=4.352@u_nA, RS=0.6458@u_Ohm, BV=110@u_V, IBV=0.0001@u_V, N=1.906)  # Define the 1N4148PH (Signal Diode)
#

#

# # print the circuit:
print("The Circuit/Netlist:\n\n", circuit)

# # create a simulator object (with paramaters e.g temp)
simulator = circuit.simulator(temperature=25, nominal_temperature=25)

# # print the circuit + simulator details:
# print("The simulator:\n\n", simulator)

# # Run analysis # #



#""" ** DC **

analysis = simulator.dc(Vinput=slice(-3, 3, 0.1)) # slice = start:step:stop (inclusive)

# Plot
fig = plt.figure()
plt.plot(np.array(analysis["n1"]), np.array(analysis["n2"]), label='V(n2)')
plt.plot(np.array(analysis["n1"]), np.array(analysis["n3"]), label='V(n3)')
plt.legend()
plt.xlabel("Input Voltage (node 1)")
plt.ylabel("Output Voltage")
#"""

#

""" ** Trans **
analysis = simulator.transient(step_time=0.0001, end_time=0.1)
#analysis = simulator.transient(step_time=Vac.period/1000, end_time=Vac.period)

print("Node:", str(analysis["n1"]), "Values:", np.array(analysis["n1"]))
print("Node:", str(analysis["n2"]), "Values:", np.array(analysis["n2"]))
print("Time Values:", np.array(analysis.time))

# # Plot Tran Output
fig = plt.figure()
plt.plot(np.array(analysis.time), np.array(analysis["n1"]), label='V(n1)')
plt.plot(np.array(analysis.time), np.array(analysis["n2"]), label='V(n2)')
plt.plot(np.array(analysis.time), np.array(analysis["n3"]), label='V(n3)')
plt.legend()
plt.xlabel("Time")
plt.ylabel("Voltage")
#"""

#

""" ** Trans **
analysis = simulator.ac(start_frequency=1@u_Hz, stop_frequency=1@u_MHz, number_of_points=10,  variation='dec')

print("Node:", str(analysis["n1"]), "Values:", np.array(analysis["n1"]))
print("Node:", str(analysis["n2"]), "Values:", np.array(analysis["n2"]))
print("Frequency Values:", np.array(analysis.frequency))

break_frequency = 1 / (2 * math.pi * float(R.resistance * C.capacitance))
print("Break frequency = {:.1f} Hz".format(break_frequency))

# # Bode plot (imported function)
fig, axes = plt.subplots(2, figsize=(20, 10))
plt.title("Bode Diagram of a Low-Pass RC Filter")
bode_diagram(axes=axes,
             frequency=analysis.frequency,
             gain=20*np.log10(np.absolute(analysis.n2)),
             phase=np.angle(analysis.n2, deg=False),
             marker='.',
             color='blue',
             linestyle='-')
for ax in axes:
    ax.axvline(x=break_frequency, color='red')
plt.tight_layout()
#"""

#

# # Save to a file
fig.savefig("Sim_Output.png", dpi=300)
plt.close(fig)

#

# fin
