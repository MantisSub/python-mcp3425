#!/usr/bin/python
from time import sleep
from mcp3425 import MCP3425

adc = MCP3425()  # Default I2C bus is 1 (Raspberry Pi 3)
#adc = mcp3425.MCP3425(0)  # Specify I2C bus

# We must initialize the adc before reading it
if not adc.init():
    print("ADC could not be initialized")
    exit(1)

# Read the adc measurement
data = adc.read()
print("ADC Measurement:", data)

# Read the adc measurement and convert
voltage = adc.convert()
print("Voltage:", voltage)

# Apply additional offset and scaling
voltage = adc.convert(offset=0.1, factor=7.32)
print("Voltage:", voltage)

sleep(5)

# Spew readings
while True:
    voltage = adc.convert()
    print("Voltage:", voltage)
    sleep(2)
