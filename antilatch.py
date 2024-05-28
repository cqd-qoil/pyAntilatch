from __future__ import absolute_import, division, print_function
from builtins import *  # @UnusedWildImport

from ctypes import cast, POINTER, c_ushort
import numpy as np
from time import sleep

from mcculw import ul
from mcculw.enums import ScanOptions, FunctionType, Status, ULRange
from mcculw.device_info import DaqDeviceInfo

from config import device_id_list, bias_voltage_list

def restart_boxes(device_id_list, bias_voltage_list):
    """
    Restart and reset the bias voltages for a list of devices.
    Intended for Measurement Computing Data Acquisition Devices.

    This function iterates through a list of device IDs, setting each device's
    bias voltage channels to zero and then resetting them to their preconfigured
    values. These values are loaded from a configuration file called `config.py`.
    Optionally, it can print the bias voltage configuration if device detection
    is enabled.

    Parameters:
    ----------
    device_id_list : list of int
        A list of device IDs to be restarted.

    bias_voltage_list : dict
        A dictionary where the keys are device IDs (matching those in device_id_list)
        and the values are dictionaries mapping channel numbers to bias voltages.

    Returns:
    -------
    bias_voltage_list : dict
        The input bias_voltage_list, potentially modified if any updates were made.

    Example:
    -------
    >>> device_ids = [0, 1]
    >>> bias_voltages = {
    ...     0: {0: 5.0, 1: 3.3, 2: 1.2},
    ...     1: {0: 2.5, 1: 0.0}
    ... }
    >>> restart_boxes(device_ids, bias_voltages)
    {0: {0: 5.0, 1: 3.3, 2: 1.2}, 1: {0: 2.5, 1: 0.0}}

    """
    memhandle = None  # Not used
    use_device_detection = False  # Flag to determine if device detection should be used

    if use_device_detection:
        # If device detection is enabled, print out the bias voltage configuration for the first device
        board_bv = bias_voltage_list[0]
        for channel, channel_bv in list(board_bv.items()):
            print(channel, type(channel), channel_bv, type(channel_bv))
        return device_id_list, bias_voltage_list

    # Iterate over each device in the device ID list
    for board in device_id_list:
        try:
            # Get bias voltages
            board_bv = bias_voltage_list[board]
            num_chans = 8
            low_chan = 0
            high_chan = num_chans - 1
            assert len(board_bv) <= num_chans

            # UL range is unipolar 10V
            ao_range = ULRange.UNI10VOLTS

            for channel, channel_bv in list(board_bv.keys()):
                # Set all the analog output voltage to 0
                ul.a_out(board_num=int(board),
                         channel=int(channel),
                         ul_range=ao_range,
                         data_value=0)
                sleep(0.05)
                # Voltage units are converted from engineering units (normal people units) to an integer
                # from 0 to 2^64-1, depending on the UL range.
                value = ul.from_eng_units(board_num=int(board),
                                          ul_range=ao_range,
                                          eng_units_value=float(channel_bv))
                # Then reset to preconfigured values
                ul.a_out(board_num=int(board),
                         channel=int(channel),
                         ul_range=ao_range,
                         data_value=int(value))
        except Exception as e:
            print('\n', e)
        finally:
            if memhandle:
                # Free the buffer in a finally block to prevent a memory leak.
                ul.win_buf_free(memhandle)
            if use_device_detection:
                ul.release_daq_device(board)
    return bias_voltage_list

if __name__ == '__main__':
    restart_boxes(device_id_list=device_id_list,
                  bias_voltage_list=bias_voltage_list)
