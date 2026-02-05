# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time

import board

import adafruit_bme680

# Create sensor object, communicating over the board's default I2C bus
i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c, debug=False)

# change this to match the location's pressure (hPa) at sea level
bme680.sea_level_pressure = 1013.25

# You will usually have to add an offset to account for the temperature of
# the sensor. This is usually around 5 degrees but varies by use. Use a
# separate temperature sensor to calibrate this one.
temperature_offset = -5

#set time to zero when woken up
start = time.time()

while (time.time() < start + 10):

    print(f"""\n          Time: {time.ctime()}s 
          Temperature: {bme680.temperature + temperature_offset:.1f} C 
          Gas: {bme680.gas}d ohm 
          Humidity: {bme680.relative_humidity:.1f} % 
          Pressure: {bme680.pressure:.3f} hPa 
          Altitude = {bme680.altitude:.2f} meters
          """)
    
    #save data in csv file
    with open("/sd/bme680_data.csv", "a") as f:
        f.write(
            f"{time.ctime()},{bme680.temperature + temperature_offset:.1f},{bme680.gas},{bme680.relative_humidity:.1f},{bme680.pressure:.3f},{bme680.altitude:.2f}\n"
        )

    time.sleep(1)   
    



