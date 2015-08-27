# GrovePi_TH02_v1.1
The purpose of this script is to read the humidity and temperature from the TH02_v1.1

## i2c Thermistor and Humidity
The TH02 has an I2C serial interface with a 7-bit address of 0x40. The TH02 is a slave device supporting data
transfer rates up to 400 kHz

This means that the device is connected to the GrovePi i2c port (I am assuming i2c1)

    Specs and fun live here:
    http://www.hoperf.cn/upload/sensor/TH02_V1.1.pdf

## Reads
You need 35ms for the sensor to stabilize for a decent reading
Experimentation suggests the value should be much higher - at least for an initial read


## Temperature:
Read the upper and lower bytes of the temperature value from DATAh and DATAl (registers 0x01 and 0x02),
respectively. In DATAl only the first 6 bits are used, this means the reading requires only 14bits.

        Temp conversion is
            celsius = TRead/32 - 50
            
## Humidity:
Read the upper and lower bytes of the temperature value from DATAh and DATAl (registers 0x01 and 0x02),
respectively. In DATAl only the first 4 bits are used, this means the reading requires only 12bits.

        Humidity conversion is
            humidity = HRead/16 - 24
                     
### Steps
 - Step 1
   Set START (D0) and TEMP (D4) in CONFIG (register 0x03) to begin a new conversion, i.e., write CONFIG with 0x11
        
 - Step 2
   Poll RDY (D0) in STATUS (register 0) until it is low (=0)
               
 - Step 3
   Read the data block from the sensor
   Remember the i2c Data block is 32 bytes wide.
      
## Note
This is just my attempt to make this work - I may have made some mistakes but at least my results seem normal, unlike
the supplied module - Lyndon


[![Bitdeli Badge](https://d2weczhvl823v0.cloudfront.net/monk-ee/grovepi_th02_v1.1/trend.png)](https://bitdeli.com/free "Bitdeli Badge")

