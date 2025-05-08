import struct

class LSM6DSM:
    def __init__(self, i2c, addr=0x6B):
        self.i2c = i2c
        self.addr = addr

        # WHO_AM_I Register prüfen (optional)
        who_am_i = self.i2c.readfrom_mem(self.addr, 0x0F, 1)[0]
        #if who_am_i != 0x6B:
         #   raise RuntimeError("LSM6DSM nicht gefunden!")

        # CTRL1_XL (Odr_XL = 104Hz, FS_XL = ±2g)
        self.i2c.writeto_mem(self.addr, 0x10, bytes([0x40]))
        # CTRL2_G (Odr_G = 104Hz, FS_G = 250 dps)
        self.i2c.writeto_mem(self.addr, 0x11, bytes([0x40]))

    def read_accel(self):
        data = self.i2c.readfrom_mem(self.addr, 0x28, 6)
        x, y, z = struct.unpack('<hhh', data)
        # ±2g = 0.061 mg/LSB
        return (x * 0.061 / 1000, y * 0.061 / 1000, z * 0.061 / 1000)

    def read_gyro(self):
        data = self.i2c.readfrom_mem(self.addr, 0x22, 6)
        x, y, z = struct.unpack('<hhh', data)
        # 250 dps = 8.75 mdps/LSB
        return (x * 8.75 / 1000, y * 8.75 / 1000, z * 8.75 / 1000)
