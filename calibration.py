
DEFAULT_I2C_BUS = 0
DEFAULT_ADC_VREF = 2.048
DEFAULT_ADDRESS_MCP3425 = 0x68

adc = None
adc_address = None
adc_model = None

import mcp3425

adc = mcp3425.MCP3425(bus=DEFAULT_I2C_BUS,
                      address=DEFAULT_ADDRESS_MCP3425,
                      vref=DEFAULT_ADC_VREF)
test = adc.read(1, 0)  # will return 0 if not present

print("Starting calibration of {}".format(adc_model))
print("")
print("Set supply voltage, then enter your reading.")
supply_voltage_1 = float(input("Supply voltage 1: "))
adc_reading_1 = adc.read(1,0)

print("")
print("Now set a different supply voltage, then enter your reading.")
supply_voltage_2 = float(input("Supply voltage 2: "))
adc_reading_2 = adc.read(1,0)

factor, offset = adc.calibrate(adc_reading_1, supply_voltage_1, adc_reading_2, supply_voltage_2)
voltage = adc.read(factor, offset)

print("")
print("Calibration complete.")
print("ADC model: {} at {}".format(adc_model, adc_address))
print("Reference: {}V".format(DEFAULT_ADC_VREF))
print("Supply Voltage 1 {}V".format(supply_voltage_1))
print("Reading Voltage 1 {}V".format(adc_reading_1))
print("Supply Voltage 2 {}V".format(supply_voltage_2))
print("Reading Voltage 2 {}V".format(adc_reading_2))
print("Calibration parameters:")
print("Factor: {}".format(factor))
print("Offset: {}".format(offset))
print("Calibrated reading: {}V".format(voltage))
