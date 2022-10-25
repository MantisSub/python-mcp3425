#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""library for the MCP3421 ADC"""

__author__ = "Axel Busch"
__copyright__ = "Copyright 2022, Xlvisuals Limited"
__license__ = "MIT"
__version__ = "1.0.1"

from smbus2 import SMBus
from time import sleep

MCP3425_ADDRESS_POOL = [0x68, 0x69, 0x6a, 0x6b, 0x6c, 0x6d, 0x6e, 0x6f]
MCP3425_DEFAULT_BUS = 0
MCP3425_DEFAULT_ADDRESS = 0x68
MCP3425_DEFAULT_VREF = 2.048

class MCP3425:

    """
    Initialize, supplying optional I2C Bus number, device address, and reference voltage.
    """

    def __init__(self,
                 bus=MCP3425_DEFAULT_BUS,
                 address=MCP3425_DEFAULT_ADDRESS,
                 vref=MCP3425_DEFAULT_VREF):
        self._address = address or MCP3425_DEFAULT_ADDRESS
        self._vref = vref or MCP3425_DEFAULT_VREF
        self._bus = SMBus(bus)
        self._calibration_factor = 1
        self._calibration_offset = 0

    def read(self, factor=None, offset=None):
        """
        Read voltage. Applies calibration data from calibration() call, or override with parameters.
        """
        result = 0
        try:
            if factor is None:
                factor = self._calibration_factor
            if offset is None:
                offset = self._calibration_offset
            if self._bus:
                self._bus.write_i2c_block_data(self._address, 0b10001000, [0x00])
                sleep(0.25)
                data = self._bus.read_i2c_block_data(self._address, 0x00, 2)
                if data:
                    raw = data[0] << 8 | data[1]
                    if raw > 32767:
                        raw -= 65535
                    result = offset + raw * self._vref / 32767 * factor
        except Exception as e:
            print("Exception reading MCP3425: ", e)
        return result

    def calibrate(self, reading_1, voltage_1, reading_2, voltage_2):
        """
        Calibrate factor and offset for voltage divider by supplying two readings and their corresponding voltages.
        m = (y2 - y1)/(x2 - x1)
        b = y2 - x2 * m
        """
        self._calibration_factor = (voltage_2 - voltage_1) / (reading_2 - reading_1)
        self._calibration_offset = voltage_1 - reading_1 * self._calibration_factor
        return self._calibration_factor, self._calibration_offset

    def reset(self):
        """
        Reset calibration data.
        """
        self._calibration_factor = 1
        self._calibration_offset = 0
