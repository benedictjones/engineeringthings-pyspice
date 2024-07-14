import numpy as np
import matplotlib.pyplot as plt
import time

from typing import List, Dict, Optional
from multiprocessing import Pool

import PySpice
import PySpice.Logging.Logging as Logging
from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import *


logger = Logging.setup_logging()

def cast_waveform(waveform) -> np.ndarray|float:
    """ From utils.methods """
    if len(waveform) == 1:
        return float(waveform[0])
    else:
        return np.array(waveform)

def format_analysis(
    analysis,
    cast:bool=True,
) -> Dict[str|int, np.ndarray|float]:
    """ From utils.methods """

    if hasattr(analysis, 'nodes') is False:
        raise ValueError('Must pass a completed analysis')

    res = {}

    # Include node voltagess
    for node, waveform in analysis.nodes.items():
        res[node] = cast_waveform(waveform) if cast else waveform

    # Include time if it exists
    if hasattr(analysis, 'time'):
        res['time'] = cast_waveform(analysis.time) if cast else analysis.time

    # Include time if it exists
    if hasattr(analysis, 'frequency'):
        res['frequency'] = cast_waveform(analysis.frequency) if cast else analysis.frequency

    return res

def perform_simulation(simulator):
    analysis = simulator.transient(step_time=0.0001, end_time=0.1)
    return analysis

def perform_simulation_to_dict(simulator) -> dict:
    """ Perform the simulation, and convert results to a dict to return """
    analysis = simulator.transient(step_time=0.0001, end_time=0.1)
    return format_analysis(analysis)

def create_and_perform_simulation(r:float) -> dict:
    """ Create circuit, perform simulation and convert results to dict to return """
    # # create the circuit
    circuit = Circuit(f"Tutorial 7: R={r} Ohm")

    # # add components to the circuit
    # circuit.V('input', 'n1', circuit.gnd, 10@u_V) # DC voltage comonent
    Vac = circuit.SinusoidalVoltageSource('input', 'n1', circuit.gnd, amplitude=1@u_V, frequency=100@u_Hz)
    R = circuit.R(1, 'n1', 'n2', r@u_kOhm)  # @u_kΩ is a unit of kOhms
    C = circuit.C(1, 'n2', circuit.gnd, 1@u_uF)
    circuit.Diode(1, 'n2', 'n3', model='MyDiode')  # using cutom defined diode
    circuit.R(2, 'n3', circuit.gnd, 1@u_kOhm)  # @u_kΩ is a unit of kOhms

    # add our diode
    circuit.model('MyDiode', 'D', IS=4.352@u_nA, RS=0.6458@u_Ohm, BV=110@u_V, IBV=0.0001@u_V, N=1.906)  # Define the 1N4148PH (Signal Diode)

    # Print the netlist
    simulator = circuit.simulator(temperature=25, nominal_temperature=25)

    analysis = simulator.transient(step_time=0.0001, end_time=0.1)

    return format_analysis(analysis)



"""
Make several simualtions, then solve using MP.
"""

sweep_resistors = np.arange(500, 100000, 500)
sweep_sims = []
for r in sweep_resistors:

    # # create the circuit
    circuit = Circuit(f"Tutorial 7: R={r} Ohm")

    # # add components to the circuit
    # circuit.V('input', 'n1', circuit.gnd, 10@u_V) # DC voltage comonent
    Vac = circuit.SinusoidalVoltageSource('input', 'n1', circuit.gnd, amplitude=1@u_V, frequency=100@u_Hz)
    R = circuit.R(1, 'n1', 'n2', r@u_kOhm)  # @u_kΩ is a unit of kOhms
    C = circuit.C(1, 'n2', circuit.gnd, 1@u_uF)
    circuit.Diode(1, 'n2', 'n3', model='MyDiode')  # using cutom defined diode
    circuit.R(2, 'n3', circuit.gnd, 1@u_kOhm)  # @u_kΩ is a unit of kOhms

    # add our diode
    circuit.model('MyDiode', 'D', IS=4.352@u_nA, RS=0.6458@u_Ohm, BV=110@u_V, IBV=0.0001@u_V, N=1.906)  # Define the 1N4148PH (Signal Diode)

    # Print the netlist
    simulator = circuit.simulator(temperature=25, nominal_temperature=25)

    sweep_sims.append(simulator)



# Solve in a loop (i.e., serially)
tic = time.time()
results = [perform_simulation(sim) for sim in sweep_sims]
toc = time.time()
print(f"Serial Total time = {toc-tic}")



if __name__ ==  '__main__': 
    
    # See if we can multiprocess (i.e., MP)
    try:
        with Pool() as p:
            results_mp = p.map(perform_simulation, sweep_sims)
    except Exception as e:
        print('Failed to MP with passed sims')

    # See if we can multiprocess (i.e., MP) using a formatted output
    try:
        with Pool() as p:
            results_mp = p.map(perform_simulation_to_dict, sweep_sims)
    except Exception as e:
        print('Failed to MP with passed sims with a formatted output')

    # Try and do MP where we create the circuit, running the simulation, 
    # and extracting the desired results which can be returned without an error.
    tic = time.time()
    with Pool() as p:
        results_mp = p.map(create_and_perform_simulation, sweep_resistors)
    toc = time.time()
    mp_time = toc-tic
    print(f"MP Total time = {mp_time}")

    # Compare by repeating the exact same thing put serially
    tic = time.time()
    results_serial = [create_and_perform_simulation(r) for r in sweep_resistors]
    toc = time.time()
    serial_time = toc-tic
    print(f"Serially run total time = {serial_time}")

    speed_up = serial_time/mp_time
    print(f"Speed up is: {speed_up:.2f} times")

    # Check they are exactly equal
    for i, res_serial in enumerate(results_serial):
        for k, v in res_serial.items():
            are_they_equal = (results_mp[i][k] == v).all()
            if are_they_equal is False:
                raise ValueError('Serial and Multiprocessed results are not the same')