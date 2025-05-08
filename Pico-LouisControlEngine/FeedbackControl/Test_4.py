from machine import I2C, Pin
from imu import IMU
import time

# I2C-Setup
i2c0 = I2C(0, scl=Pin(17), sda=Pin(16))  # LSM6DSM
print(i2c0.scan())
i2c1 = I2C(1, scl=Pin(19), sda=Pin(18))  # HMC5883L
print(i2c1.scan())

imu = IMU(i2c0, i2c1)
imu.calibrate()

while True:
    data = imu.update()
    print("Roll: {:.1f}°, Pitch: {:.1f}°, Yaw: {:.1f}°".format(data["roll"], data["pitch"], data["yaw"]))
    print("Mag: ({:.1f}, {:.1f}, {:.1f})".format(*data["mag"]))
    time.sleep(0.5)
