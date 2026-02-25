import time

import board

import adafruit_bme680
import csv

import board

from adafruit_pm25.uart import PM25_UART

import serial


#ARGUMENTS - 1: name of file to save to (without .csv) - will not save if not given
#            2: runtime in seconds (optional, default is 10 seconds)   


reset_pin = None
uart = serial.Serial("/dev/ttyS0", baudrate=9600, timeout=0.25)
pm25 = PM25_UART(uart, reset_pin)
print("Found PM2.5 sensor, reading data...")

i2c = board.I2C() 
bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c, debug=False)

bme680.sea_level_pressure = 1013.25

temperature_offset = -5

start = time.time()

hasfile = False


import sys

arguments = sys.argv

try:
    runtime = int(arguments[2])
except Exception as e:
    print("Unable to parse runtime argument")
    print("----------------------")
    print(e)
else:
    runtime = 10



try:
    file = open(f"data/{arguments[1]}.csv","w",newline=None)
except Exception as e:
    print("Unable to read file (remove the .csv from the name)")
    print("----------------------")
    print(e)
else:
    hasfile = True
    csvwriter = csv.writer(file,delimiter=',')
    csvwriter.writerow(["time","temperature","gas","humidity","pressure","altitude","pm10standard", "pm25standard", "pm100standard","pm10env","pm25env","pm100 env","p03um","p05um","p10um","p25um","p50um","p100um"])


while (time.time() < start + runtime):
    time.sleep(1)

    try:
        aqdata = pm25.read()
        # print(aqdata)
    except RuntimeError:
        print("Unable to read from sensor, retrying...")
        continue

    print(f"""\n          Time: {time.ctime()}s 
          Temperature: {bme680.temperature + temperature_offset:.1f} C 
          Gas: {bme680.gas}d ohm 
          Humidity: {bme680.relative_humidity:.1f} % 
          Pressure: {bme680.pressure:.3f} hPa 
          Altitude = {bme680.altitude:.2f} meters
          \n""")
    
    print("Concentration Units (standard)")
    print("---------------------------------------")
    print(
        "PM 1.0: %d\tPM2.5: %d\tPM10: %d"
        % (aqdata["pm10 standard"], aqdata["pm25 standard"], aqdata["pm100 standard"])
    )
    print("Concentration Units (environmental)")
    print("---------------------------------------")
    print(
        "PM 1.0: %d\tPM2.5: %d\tPM10: %d"
        % (aqdata["pm10 env"], aqdata["pm25 env"], aqdata["pm100 env"])
    )
    print("---------------------------------------")
    print("Particles > 0.3um / 0.1L air:", aqdata["particles 03um"])
    print("Particles > 0.5um / 0.1L air:", aqdata["particles 05um"])
    print("Particles > 1.0um / 0.1L air:", aqdata["particles 10um"])
    print("Particles > 2.5um / 0.1L air:", aqdata["particles 25um"])
    print("Particles > 5.0um / 0.1L air:", aqdata["particles 50um"])
    print("Particles > 10 um / 0.1L air:", aqdata["particles 100um"])
    print("---------------------------------------")

    if(hasfile):
        csvwriter.writerow([time.ctime(),
                            (bme680.temperature + temperature_offset),
                            bme680.gas,
                            bme680.relative_humidity,
                            bme680.pressure,
                            bme680.altitude, 
                            aqdata["pm10 standard"], 
                            aqdata["pm25 standard"], 
                            aqdata["pm100 standard"],
                            aqdata["pm10 env"], 
                            aqdata["pm25 env"], 
                            aqdata["pm100 env"],
                            aqdata["particles 03um"],
                            aqdata["particles 05um"],
                            aqdata["particles 10um"],
                            aqdata["particles 25um"],
                            aqdata["particles 50um"],
                            aqdata["particles 100um"]
                            ])






    

