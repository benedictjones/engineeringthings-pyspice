import numpy as np
import os
from typing import List, Dict, Optional

import PySpice
from PySpice.Spice.Netlist import Circuit


def format_analysis(
    analysis,
    cast:bool=True,
) -> Dict[str|int, np.ndarray|float|PySpice.Probe.WaveForm.WaveForm]:
    '''
    Extracts dictionary containing SPICE sim values.
    The typical waveform analysis result can be cast to a numpy array.

    Args:
        analysis (pysepice simulation run object):
            The run analysis
        cast (bool):
            Whether to convert waveform outputs to
            single float value or numpy array.

    Returns:
        dict: analysis results dictionary
    '''

    if hasattr(analysis, 'nodes') is False:
        raise ValueError('Must pass a completed analysis')

    res = {}
    for node, waveform in analysis.nodes.items():
        if cast:
            if len(waveform) == 1:
                res[node] = float(waveform[0])
            else:
                res[node] = np.array(waveform)

        else:
            res[node] = waveform

    return res


def write_line_to_netlist(
    circuit:Circuit,
    new_line:str
) -> Circuit:
    """
    Wite a string as a new line to a circuit's netlist.

    Args:
        cir (Circuit):
            PySpice Circuit object.
        new_line (str):
            String to become the new line.

    Returns:
        Circuit: PySpice circuit object with added Raw SPICE line
    """
    circuit.raw_spice += new_line + os.linesep
    return circuit