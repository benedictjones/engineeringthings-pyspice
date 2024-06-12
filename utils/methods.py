import numpy as np
from typing import List, Dict, Optional
import PySpice



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