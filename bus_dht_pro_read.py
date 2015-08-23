#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Monkee Magic <magic.monkee.magic@gmail.com>'
__version__ = '1.0.0'

"""
i2c Thermistor and Humidity
The TH02 has an I2C serial interface with a 7-bit address of 0x40. The TH02 is a slave device supporting data
transfer rates up to 400 kHz

This means that the device is connected to the GrovePi i2c port (I am assuming i2c1)

The purpose of this script is to read the humidity and temperature from the TH02_v1.1

Specs and fun live here:
http://www.hoperf.cn/upload/sensor/TH02_V1.1.pdf

"""

import smbus
import time
import RPi.GPIO as GPIO

from bitstring import BitArray


class GrovePiDHTPro:
    # I2C Address of GrovePii Temp / Humidity Sensor
    address = 0x40
    start = 0x00
    config = 0x03
    temperature = 0x11
    humidity = 0x01
    rev = ""
    bus = ""
    data = {}
    results = {}

    def __init__(self):
        self.connect_bus()
        self.get_sensor_reading(0, self.temperature)
        self.convert_temperature(0)

        self.get_sensor_reading(1, self.humidity)
        self.convert_humidity(1)

    def returnResults(self):
        return self.results

    def connect_bus(self):
        """
        determine the bus here because it varies from device versions
        :return:
        """
        self.rev = GPIO.RPI_REVISION
        if self.rev == 2 or self.rev == 3:
            self.bus = smbus.SMBus(1)
        else:
            self.bus = smbus.SMBus(0)

    def get_sensor_reading(self, index, sensor):
        """
        Step 1
        Set START (D0) and TEMP (D4) in CONFIG (register 0x03) to begin a new conversion, i.e., write CONFIG with
        0x11
        :return:
        """
        try:
            self.bus.write_byte_data(self.address, self.config, sensor)
        except:
            exit("Could not write to Sensor, is it plugged in?")

        """
        You need 35ms for the sensor to stabilize for a decent reading
        Experimentation suggests the value should be much higher - at least for an initial read
        """
        time.sleep(.8)
        """
        #step 2
        # Poll RDY (D0) in STATUS (register 0) until it is low (=0)
        """
        while True:
            single = self.bus.read_byte(self.address)
            if single == 0:
                break
        """
        Step 3
        Read the data block from the sensor

        Remember the i2c Data block is 32 bytes wide.

        """
        while True:
            try:
                self.data[index] = self.bus.read_i2c_block_data(self.address, 1)
                break
                ##### never ever over read you will lock up the grove
            except:
                #sometimes it is not ready to read.
                pass

    def convert_temperature(self, index):
        """
        Temperature:
        Read the upper and lower bytes of the temperature value from DATAh and DATAl (registers 0x01 and 0x02),
        respectively. In DATAl only the first 6 bits are used, this means the reading requires only 14bits.

        Temp conversion is
            celsius = TRead/32 - 50
        :param index: - where to look in the data array:
        :return:
        """
        upperArray = BitArray(hex=hex(self.data[index][1]))
        lowerArray = BitArray(hex=hex(self.data[index][2]))
        upper = upperArray.bin
        lower = lowerArray.bin
        forteenBit = upper + "" + lower[:-2]
        temperatureHex = hex(int(forteenBit, 2))
        temperatureReading = int(temperatureHex, 16)
        """
        convert reading here
        """
        temperature = (temperatureReading / 32) - 50
        self.results.update({'temperature': temperature})

    def convert_humidity(self, index):
        """
        Humidity:
        Read the upper and lower bytes of the temperature value from DATAh and DATAl (registers 0x01 and 0x02),
        respectively. In DATAl only the first 4 bits are used, this means the reading requires only 12bits.

        Humidity conversion is
            humidity = HRead/16 - 24
        :param index: - where to look in the data array:
        :return:
        """
        upperArray = BitArray(hex=hex(self.data[index][1]))
        lowerArray = BitArray(hex=hex(self.data[index][2]))
        upper = upperArray.bin
        lower = lowerArray.bin
        twelveBit = upper + "" + lower[:-4]
        humidityHex = hex(int(twelveBit, 2))
        humidityReading = int(humidityHex, 16)
        """
        convert reading here
        """
        humidity = (humidityReading / 16) - 24
        self.results.update({'humidity': humidity})

if __name__ == '__main__':
    grover = GrovePiDHTPro()
    print("Results", grover.returnResults())