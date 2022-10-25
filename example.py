#!/usr/bin/python
from time import sleep
from mcp3425 import MCP3425


# Create with default parameters
# MCP3425_DEFAULT_BUS = 0
# MCP3425_DEFAULT_ADDRESS = 0x68
# MCP3425_DEFAULT_VREF = 2.048
adc = MCP3425()

# specify bus, address, and voltage.
adc = MCP3425(bus=0, address=0x68, vref=2.048)

# Read the adc measurement
data = adc.read()
print("ADC Measurement:", data)

# Calibrate voltage divider reading using two known voltages and readings:
s1 = 1.3123525498214668, 9.0
s2 = 1.9201210974456007, 13.0
factor, offset = adc.calibrate(s1[0], s1[1], s2[0], s2[1])
print("Dataset 1:", s1)
print("Dataset 2:", s2)
print("Factor:", factor)
print("Offset:", offset)

# Apply additional scaling and offset to the reading if a voltage divider is in use
# this will override the calibration for this reading, but not update the settings provided with calibration
voltage = adc.read(factor=7.123, offset=0.324)
print("Voltage:", voltage)

print("")
print("Reading -> Voltage")
# Spew calibrated readings
while True:
    sleep(2)
    reading = adc.read(1,0) # pure reading
    voltage = adc.read() # using (saved) calibration data
    print(reading, "->", voltage)
