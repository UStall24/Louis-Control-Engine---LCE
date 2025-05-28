from machine import Pin, I2C
import time
from math import atan2, sqrt

class gyroscope:
    def __init__(self):
        # MPU6050 I2C Address
        self.MPU6050_ADDR = 0x68
        # Register Addresses
        self.PWR_MGMT_1 = 0x6B
        self.ACCEL_XOUT_H = 0x3B
        self.ACCEL_YOUT_H = 0x3D
        self.ACCEL_ZOUT_H = 0x3F
        self.GYRO_XOUT_H = 0x43
        self.GYRO_YOUT_H = 0x45
        self.GYRO_ZOUT_H = 0x47
        
        # Initialize I2C
        self.i2c = I2C(0, scl=Pin(17), sda=Pin(16), freq=400000)
        
        self.i2c.writeto_mem(self.MPU6050_ADDR, self.PWR_MGMT_1, b'\x00')
        
        # Calibration offsets
        self.gyro_offsets = [0, 0, 0]
        self.calibrate()
        
    def read_raw_data(self, addr):
        high = self.i2c.readfrom_mem(self.MPU6050_ADDR, addr, 1)
        low = self.i2c.readfrom_mem(self.MPU6050_ADDR, addr + 1, 1)
        value = (high[0] << 8) | low[0]
        return value - 65536 if value > 32768 else value
        
    def calibrate(self, samples=500):
        """Measure and store gyro offsets when stationary"""
        print("Calibrating gyro...")
        offsets = [0, 0, 0]
        for _ in range(samples):
            offsets[0] += self.read_raw_data(self.GYRO_XOUT_H)
            offsets[1] += self.read_raw_data(self.GYRO_YOUT_H)
            offsets[2] += self.read_raw_data(self.GYRO_ZOUT_H)
            time.sleep(0.01)
        self.gyro_offsets = [x/samples for x in offsets]
        
    def getData(self):
        """Return raw sensor data without filtering"""
        # Gyro readings (°/s)
        gyro_x = (self.read_raw_data(self.GYRO_XOUT_H) - self.gyro_offsets[0]) / 131.0
        gyro_y = (self.read_raw_data(self.GYRO_YOUT_H) - self.gyro_offsets[1]) / 131.0
        gyro_z = (self.read_raw_data(self.GYRO_ZOUT_H) - self.gyro_offsets[2]) / 131.0
        
        # Accelerometer readings (g)
        accel_x = self.read_raw_data(self.ACCEL_XOUT_H) / 16384.0
        accel_y = self.read_raw_data(self.ACCEL_YOUT_H) / 16384.0
        accel_z = self.read_raw_data(self.ACCEL_ZOUT_H) / 16384.0
        
        return [gyro_x, gyro_y, gyro_z, accel_x, accel_y, accel_z]