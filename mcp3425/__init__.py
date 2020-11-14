from smbus2 import SMBus

# MCP3424, MCP3427 & MCP3428 addresses are controlled by address lines A0 and A1
# each address line can be low (GND), high (VCC) or floating (FLT)
MCP3425_DEFAULT_ADDRESS = 0x68
MCP3425_CONF_A0GND_A1GND = 0x68
MCP3425_CONF_A0GND_A1FLT = 0x69
MCP3425_CONF_A0GND_A1VCC = 0x6A
MCP3425_CONF_A0FLT_A1GND = 0x6B
MCP3425_CONF_A0VCC_A1GND = 0x6C
MCP3425_CONF_A0VCC_A1FLT = 0x6D
MCP3425_CONF_A0VCC_A1VCC = 0x6E
MCP3425_CONF_A0FLT_A1VCC = 0x6F

MCP3425_BITS_RESOLUTION = 16

# /RDY bit definition
MCP3425_CONF_NO_EFFECT = 0x00
MCP3425_CONF_RDY = 0x80

# Conversion mode definitions
MCP3425_CONF_MODE_ONESHOT = 0x00
MCP3425_CONF_MODE_CONTINUOUS = 0x10

# Channel definitions
# MCP3425 have only the one channel
# MCP3426 & MCP3427 have two channels and treat 3 & 4 as repeats of 1 & 2 respectively
# MCP3428 have all four channels
MCP3425_CONF_CHANNEL_1 = 0x00
'''MCP342X_CHANNEL_2			= 0x20
   MCP342X_CHANNEL_3			= 0x40
   MCP342X_CHANNEL_4			= 0x60
'''

# Sample size definitions - these also affect the sampling rate
# 12-bit has a max sample rate of 240sps
# 14-bit has a max sample rate of  60sps
# 16-bit has a max sample rate of  15sps
MCP3425_CONF_SIZE_12BIT = 0x00
MCP3425_CONF_SIZE_14BIT = 0x04
MCP3425_CONF_SIZE_16BIT = 0x08
# MCP342X_CONF_SIZE_18BIT		= 0x0C

# Programmable Gain definitions
MCP3425_CONF_GAIN_1X = 0x00
MCP3425_CONF_GAIN_2X = 0x01
MCP3425_CONF_GAIN_4X = 0x02
MCP3425_CONF_GAIN_8X = 0x03


class MCP3425:

    def __init__(self, bus=1,
                 ready=MCP3425_CONF_RDY,
                 channel=MCP3425_CONF_CHANNEL_1,
                 mode=MCP3425_CONF_MODE_CONTINUOUS,
                 rate=MCP3425_CONF_SIZE_12BIT,
                 gain=MCP3425_CONF_GAIN_1X,
                 resolution=MCP3425_BITS_RESOLUTION,
                 vref=2.048):
        try:
            self._bus = SMBus(bus)
        except:
            print("Bus %d is not available." % bus)
            print("Available busses are listed as /dev/i2c*")
            self._bus = None

        self._ready = ready
        self._channel = channel
        self._mode = mode
        self._rate = rate
        self._gain = gain
        self._resolution = resolution
        self._vref = vref

    def init(self):

        if self._bus is None:
            print("No bus!")
            return False

        self.setReady(self._ready)
        self.setChannel(self._channel)
        self.setMode(self._mode)
        self.setSampleRate(self._rate)
        self.setGain(self._gain)

        return True

    def setReady(self, ready):
        """
        Set Ready Bit
        In read mode, it indicates the output register has been updated with a new conversion.
        In one-shot Conversion mode, writing initiates a new conversion.
        """
        if self._bus:
            self._bus.write_byte(MCP3425_DEFAULT_ADDRESS, ready)

    def setChannel(self, channel):
        """
        Set Channel Selection for MCP3426, MCP3427, MCP3428
        Channels are not used for MCP3425
        """
        if self._bus:
            self._bus.write_byte(MCP3425_DEFAULT_ADDRESS, channel)

    def setMode(self, mode):
        """
        Set Conversion Mode
        1 = Continous Conversion Mode
        0 = One-shot Conversion Mode
        """
        if self._bus:
            self._bus.write_byte(MCP3425_DEFAULT_ADDRESS, mode)

    def setSampleRate(self, rate):
        """
        Set Sample rate selection bit
        00 : 240 SPS-12 bits
        01 : 60 SPS 14 bits
        10 : 15 SPS 16 bits
        """
        if self._bus:
            self._bus.write_byte(MCP3425_DEFAULT_ADDRESS, rate)

    def setGain(self, gain):
        """
        # Set the PGA gain
        00 : 1 V/V
        01 : 2 V/V
        10 : 4 V/V
        11 : 8 V/V
        """
        if self._bus:
            self._bus.write_byte(MCP3425_DEFAULT_ADDRESS, gain)

    def read(self):
        """
        Get the measurement for the ADC values  from the register using the General Calling method
        """
        if self._bus:
            data = self._bus.read_i2c_block_data(MCP3425_DEFAULT_ADDRESS, 0x00, 2)
            value = ((data[0] << 8) | data[1])
            if (value >= 32768):
                value = 65536 - value
            return value
        else:
            return 0

    def convert(self, factor=1.0, offset=0.0):
        """
        Shows the output codes of input level using 16-bit conversion mode
        The output code is proportional to the voltage difference b/w two analog points
        """
        code = self.read()
        voltage = offset + (2 * self._vref * code) / (2 ** self._resolution) * factor
        return voltage
