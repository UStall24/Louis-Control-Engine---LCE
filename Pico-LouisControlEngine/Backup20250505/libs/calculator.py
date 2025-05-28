from math import atan2, sqrt

class Calculator:
    def __init__(self, direction_values, gyro=None):
        self.maxPWM = 1700
        self.minPWM = 1300
        self.deadZoneMin = 1464
        self.deadZoneMax = 1536
        self.deadZoneDefault = 1500

        self.direction_values = direction_values

        self.gyro = gyro
        self.gyro_enabled = False

        self.Kp = 0.05
        self.Kd = 0.018

        self.filtered_angle_x = 0
        self.filtered_angle_y = 0
        self.alpha = 0.98
        self.dt = 0.02

        self.ANGLE_DEADZONE = 0.175
        self.GYRO_RATE_DEADZONE = 3.5

    def update_pd_controller(self, gyro_x, gyro_y, accel_x, accel_y, accel_z):
        accel_angle_x = atan2(accel_y, sqrt(accel_x**2 + accel_z**2))
        accel_angle_y = atan2(accel_x, sqrt(accel_y**2 + accel_z**2))

        self.filtered_angle_x = self.alpha * (self.filtered_angle_x + gyro_x * self.dt) + (1 - self.alpha) * accel_angle_x
        self.filtered_angle_y = self.alpha * (self.filtered_angle_y + gyro_y * self.dt) + (1 - self.alpha) * accel_angle_y

        if abs(self.filtered_angle_x) < self.ANGLE_DEADZONE and abs(gyro_x) < self.GYRO_RATE_DEADZONE:
            self.filtered_angle_x = 0
            gyro_x = 0
        if abs(self.filtered_angle_y) < self.ANGLE_DEADZONE and abs(gyro_y) < self.GYRO_RATE_DEADZONE:
            self.filtered_angle_y = 0
            gyro_y = 0

        if abs(self.filtered_angle_x) > self.ANGLE_DEADZONE or abs(gyro_x) > self.GYRO_RATE_DEADZONE:
            correction_x = -self.Kp * self.filtered_angle_x - self.Kd * gyro_x
        else:
            correction_x = 0

        if abs(self.filtered_angle_y) > self.ANGLE_DEADZONE or abs(gyro_y) > self.GYRO_RATE_DEADZONE:
            correction_y = -self.Kp * self.filtered_angle_y - self.Kd * gyro_y
        else:
            correction_y = 0

        return [
            correction_y * 0.866 - correction_x * 0.5,
            -correction_x * 0.5,
            correction_y * 0.866 + correction_x * 0.5
        ]

    def byte_to_float(self, value):
        return (value / 127.5) - 1

    def calc_motor_pwm(self, throttle_value):
        reverse_range = self.deadZoneDefault - self.minPWM
        forward_range = self.maxPWM - self.deadZoneDefault

        if throttle_value <= 0:
            pwmVal = self.deadZoneDefault + throttle_value * reverse_range
        else:
            pwmVal = self.deadZoneDefault + throttle_value * forward_range

        if self.deadZoneMin < pwmVal < self.deadZoneMax:
            return self.deadZoneDefault
        return pwmVal

    def calc_all_motor_pwm(self, throttle_values, byte_to_float_calculation):
        pwm_values = []
        for value in throttle_values:
            if byte_to_float_calculation:
                pwm_value = self.calc_motor_pwm(self.byte_to_float(value))
            else:
                pwm_value = self.calc_motor_pwm(value)
            pwm_values.append(pwm_value)
        return pwm_values

    def calc_throttle_value2(self, controller_values):
        left_joystick_x = (controller_values[0] - 128) / 255
        left_joystick_y = (controller_values[1] - 128) / 255
        right_joystick_x = (controller_values[2] - 128) / 255
        right_joystick_y = (controller_values[3] - 128) / 255
        l2_trigger = controller_values[4] / 255
        r2_trigger = controller_values[5] / 255
        l1_trigger = (controller_values[6] & 0x01) != 0 
        r1_trigger = (controller_values[6] & 0x02) != 0

        return self.calc_throttle_value(
            left_joystick_x, left_joystick_y,
            right_joystick_x, right_joystick_y,
            l1_trigger, r1_trigger,
            l2_trigger, r2_trigger
        )

    def calc_throttle_value(self, lx, ly, rx, ry, l1, r1, l2, r2):
        dv = self.direction_values
        vm1 = (dv["Translation"]["Z_Axis"]["VM1"] * ly + dv["Translation"]["X_Axis"]["VM1"] * lx - dv["Translation"]["Y_Axis"]["VM1"] * l2 + dv["Translation"]["Y_Axis"]["VM1"] * r2)
        vm2 = (dv["Translation"]["Z_Axis"]["VM2"] * ly + dv["Translation"]["X_Axis"]["VM2"] * lx - dv["Translation"]["Y_Axis"]["VM2"] * l2 + dv["Translation"]["Y_Axis"]["VM2"] * r2)
        vm3 = (dv["Translation"]["Z_Axis"]["VM3"] * ly + dv["Translation"]["X_Axis"]["VM3"] * lx - dv["Translation"]["Y_Axis"]["VM3"] * l2 + dv["Translation"]["Y_Axis"]["VM3"] * r2)
        hm1 = (dv["Translation"]["Z_Axis"]["HM1"] * ly + dv["Translation"]["X_Axis"]["HM1"] * lx - dv["Translation"]["Y_Axis"]["HM1"] * l2 + dv["Translation"]["Y_Axis"]["HM1"] * r2)
        hm2 = (dv["Translation"]["Z_Axis"]["HM2"] * ly + dv["Translation"]["X_Axis"]["HM2"] * lx - dv["Translation"]["Y_Axis"]["HM2"] * l2 + dv["Translation"]["Y_Axis"]["HM2"] * r2)
        hm3 = (dv["Translation"]["Z_Axis"]["HM3"] * ly + dv["Translation"]["X_Axis"]["HM3"] * lx - dv["Translation"]["Y_Axis"]["HM3"] * l2 + dv["Translation"]["Y_Axis"]["HM3"] * r2)

        vm1 += (dv["Rotation"]["Z_Axis"]["VM1"] * ry + dv["Rotation"]["X_Axis"]["VM1"] * rx - dv["Rotation"]["Y_Axis"]["VM1"] * int(l1) + dv["Rotation"]["Y_Axis"]["VM1"] * int(r1))
        vm2 += (dv["Rotation"]["Z_Axis"]["VM2"] * ry + dv["Rotation"]["X_Axis"]["VM2"] * rx - dv["Rotation"]["Y_Axis"]["VM2"] * int(l1) + dv["Rotation"]["Y_Axis"]["VM2"] * int(r1))
        vm3 += (dv["Rotation"]["Z_Axis"]["VM3"] * ry + dv["Rotation"]["X_Axis"]["VM3"] * rx - dv["Rotation"]["Y_Axis"]["VM3"] * int(l1) + dv["Rotation"]["Y_Axis"]["VM3"] * int(r1))
        hm1 += (dv["Rotation"]["Z_Axis"]["HM1"] * ry + dv["Rotation"]["X_Axis"]["HM1"] * rx - dv["Rotation"]["Y_Axis"]["HM1"] * int(l1) + dv["Rotation"]["Y_Axis"]["HM1"] * int(r1))
        hm2 += (dv["Rotation"]["Z_Axis"]["HM2"] * ry + dv["Rotation"]["X_Axis"]["HM2"] * rx - dv["Rotation"]["Y_Axis"]["HM2"] * int(l1) + dv["Rotation"]["Y_Axis"]["HM2"] * int(r1))
        hm3 += (dv["Rotation"]["Z_Axis"]["HM3"] * ry + dv["Rotation"]["X_Axis"]["HM3"] * rx - dv["Rotation"]["Y_Axis"]["HM3"] * int(l1) + dv["Rotation"]["Y_Axis"]["HM3"] * int(r1))

        if self.gyro is not None and self.gyro_enabled:
            data = self.gyro.getData()
            gyro_x, gyro_y = data[0], data[1]
            accel_x, accel_y, accel_z = data[3], data[4], data[5]
            corrections = self.update_pd_controller(gyro_x, gyro_y, accel_x, accel_y, accel_z)
            vm1 += corrections[0]
            vm2 += corrections[1]
            vm3 += corrections[2]

        vm1, vm2, vm3 = map(lambda v: max(-1, min(1, v)), [vm1, vm2, vm3])
        hm1, hm2, hm3 = map(lambda v: max(-1, min(1, v)), [hm1, hm2, hm3])

        return [vm1, vm2, vm3, hm1, hm2, hm3]
