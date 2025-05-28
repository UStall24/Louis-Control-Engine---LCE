from libs.gyroscopeMPU6050 import gyroscope
from math import atan2, sqrt

class Calculator:
    def __init__(self, direction_values, gyro=None):
        # Motor PWM limits
        self.maxPWM = 1700
        self.minPWM = 1300
        self.deadZoneMin = 1464
        self.deadZoneMax = 1536
        self.deadZoneDefault = 1500
        
        self.direction_values = direction_values
        
        self.gyro = gyro
        self.gyro_enabled = False
        # PD Controller Gains
        self.Kp = 0.05    # Proportional gain
        self.Kd = 0.018    # Derivative gain
        
        # Angle tracking with complementary filter
        self.filtered_angle_x = 0  # Roll
        self.filtered_angle_y = 0  # Pitch
        self.alpha = 0.98          # Filter coefficient
        self.dt = 0.02             # 50Hz update rate
        
        # Dead zone settings (in radians - 5° ≈ 0.087 rad)
        self.ANGLE_DEADZONE = 0.175  # 5 degrees in radians
        self.GYRO_RATE_DEADZONE = 3.5  # °/s (complementary to angle deadzone)
            
    def update_pd_controller(self, gyro_x, gyro_y, accel_x, accel_y, accel_z):
       # Calculate angles from accelerometer (radians)
       accel_angle_x = atan2(accel_y, sqrt(accel_x**2 + accel_z**2))
       accel_angle_y = atan2(accel_x, sqrt(accel_y**2 + accel_z**2))
            # Update complementary filter
       self.filtered_angle_x = self.alpha * (self.filtered_angle_x + gyro_x * self.dt) + (1-self.alpha) * accel_angle_x
       self.filtered_angle_y = self.alpha * (self.filtered_angle_y + gyro_y * self.dt) + (1-self.alpha) * accel_angle_y
           # Apply dead zones
       if abs(self.filtered_angle_x) < self.ANGLE_DEADZONE and abs(gyro_x) < self.GYRO_RATE_DEADZONE:
          self.filtered_angle_x = 0  # Reset if within dead zone
          gyro_x = 0
       if abs(self.filtered_angle_y) < self.ANGLE_DEADZONE and abs(gyro_y) < self.GYRO_RATE_DEADZONE:
          self.filtered_angle_y = 0
          gyro_y = 0
          # Only apply corrections outside dead zone
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
           #-correction_y * 0.866 - correction_x * 0.5,
           - correction_x * 0.5,
           correction_y * 0.866 + correction_x * 0.5
       ]
    
    def byte_to_float(self, value):
        return (value / 127.5) - 1

    def calc_motor_pwm(self, throttle_value):
        """Convert throttle input to PWM signal."""
        reverse_range = self.deadZoneDefault - self.minPWM
        forward_range = self.maxPWM - self.deadZoneDefault

        if throttle_value <= 0:
            pwmVal = self.deadZoneDefault + throttle_value * reverse_range
        else:
            pwmVal = self.deadZoneDefault + throttle_value * forward_range

        return self.deadZoneDefault if self.deadZoneMin < pwmVal < self.deadZoneMax else pwmVal

    def calc_all_motor_pwm(self, throttle_values, byte_to_float_calculation):
        """Calculate PWM values for a list of throttle inputs."""
        pwm_values = []
        for value in throttle_values:
            if byte_to_float_calculation:
                # Note: This converts the value twice if calc_motor_pwm converts it again.
                pwm_value = self.calc_motor_pwm(self.byte_to_float(value))
            else:
                pwm_value = self.calc_motor_pwm(value)
            pwm_values.append(pwm_value)
        return pwm_values

    def calc_throttle_value2(self, controller_values):
        """Extract and pass controller values to `calc_throttle_value`."""
        left_joystick_x = (controller_values[0] - 128) / 255
        left_joystick_y = (controller_values[1] - 128) / 255
        right_joystick_x = (controller_values[2] - 128) / 255
        right_joystick_y = (controller_values[3] - 128) / 255
        l2_trigger = controller_values[4] / 255
        r2_trigger = controller_values[5] / 255
        l1_trigger = (controller_values[6] & 0x01) != 0 
        r1_trigger = (controller_values[6] & 0x02) != 0
        
        return self.calc_throttle_value(left_joystick_x, left_joystick_y, right_joystick_x, 
                                        right_joystick_y, l1_trigger, r1_trigger, 
                                        l2_trigger, r2_trigger)
    
    def calc_throttle_value(self, left_joystick_x, left_joystick_y,
                            right_joystick_x, right_joystick_y,
                            l1_trigger, r1_trigger, l2_trigger, r2_trigger):
        """Calculates motor values based on joystick and trigger inputs."""
        
        # ["Translation"]
        vmotor1 = (self.direction_values["Translation"]["Z_Axis"]["VM1"] * left_joystick_y + self.direction_values["Translation"]["X_Axis"]["VM1"] * left_joystick_x - self.direction_values["Translation"]["Y_Axis"]["VM1"] * l2_trigger + self.direction_values["Translation"]["Y_Axis"]["VM1"] * r2_trigger)
        vmotor2 = (self.direction_values["Translation"]["Z_Axis"]["VM2"] * left_joystick_y + self.direction_values["Translation"]["X_Axis"]["VM2"] * left_joystick_x - self.direction_values["Translation"]["Y_Axis"]["VM2"] * l2_trigger + self.direction_values["Translation"]["Y_Axis"]["VM2"] * r2_trigger)
        vmotor3 = (self.direction_values["Translation"]["Z_Axis"]["VM3"] * left_joystick_y + self.direction_values["Translation"]["X_Axis"]["VM3"] * left_joystick_x - self.direction_values["Translation"]["Y_Axis"]["VM3"] * l2_trigger + self.direction_values["Translation"]["Y_Axis"]["VM3"] * r2_trigger)     
        hmotor1 = (self.direction_values["Translation"]["Z_Axis"]["HM1"] * left_joystick_y + self.direction_values["Translation"]["X_Axis"]["HM1"] * left_joystick_x - self.direction_values["Translation"]["Y_Axis"]["HM1"] * l2_trigger + self.direction_values["Translation"]["Y_Axis"]["HM1"] * r2_trigger)     
        hmotor2 = (self.direction_values["Translation"]["Z_Axis"]["HM2"] * left_joystick_y + self.direction_values["Translation"]["X_Axis"]["HM2"] * left_joystick_x - self.direction_values["Translation"]["Y_Axis"]["HM2"] * l2_trigger + self.direction_values["Translation"]["Y_Axis"]["HM2"] * r2_trigger)  
        hmotor3 = (self.direction_values["Translation"]["Z_Axis"]["HM3"] * left_joystick_y + self.direction_values["Translation"]["X_Axis"]["HM3"] * left_joystick_x - self.direction_values["Translation"]["Y_Axis"]["HM3"] * l2_trigger + self.direction_values["Translation"]["Y_Axis"]["HM3"] * r2_trigger)

        # ["Rotation"]
        vmotor1 += (self.direction_values["Rotation"]["Z_Axis"]["VM1"] * right_joystick_y + self.direction_values["Rotation"]["X_Axis"]["VM1"] * right_joystick_x -  self.direction_values["Rotation"]["Y_Axis"]["VM1"] * (1 if l1_trigger else 0) +  self.direction_values["Rotation"]["Y_Axis"]["VM1"] * (1 if r1_trigger else 0))
        vmotor2 += (self.direction_values["Rotation"]["Z_Axis"]["VM2"] * right_joystick_y + self.direction_values["Rotation"]["X_Axis"]["VM2"] * right_joystick_x -  self.direction_values["Rotation"]["Y_Axis"]["VM2"] * (1 if l1_trigger else 0) +  self.direction_values["Rotation"]["Y_Axis"]["VM2"] * (1 if r1_trigger else 0))
        vmotor3 += (self.direction_values["Rotation"]["Z_Axis"]["VM3"] * right_joystick_y + self.direction_values["Rotation"]["X_Axis"]["VM3"] * right_joystick_x -  self.direction_values["Rotation"]["Y_Axis"]["VM3"] * (1 if l1_trigger else 0) +  self.direction_values["Rotation"]["Y_Axis"]["VM3"] * (1 if r1_trigger else 0))
        hmotor1 += (self.direction_values["Rotation"]["Z_Axis"]["HM1"] * right_joystick_y + self.direction_values["Rotation"]["X_Axis"]["HM1"] * right_joystick_x -  self.direction_values["Rotation"]["Y_Axis"]["HM1"] * (1 if l1_trigger else 0) +  self.direction_values["Rotation"]["Y_Axis"]["HM1"] * (1 if r1_trigger else 0))
        hmotor2 += (self.direction_values["Rotation"]["Z_Axis"]["HM2"] * right_joystick_y + self.direction_values["Rotation"]["X_Axis"]["HM2"] * right_joystick_x -  self.direction_values["Rotation"]["Y_Axis"]["HM2"] * (1 if l1_trigger else 0) +  self.direction_values["Rotation"]["Y_Axis"]["HM2"] * (1 if r1_trigger else 0))
        hmotor3 += (self.direction_values["Rotation"]["Z_Axis"]["HM3"] * right_joystick_y + self.direction_values["Rotation"]["X_Axis"]["HM3"] * right_joystick_x -  self.direction_values["Rotation"]["Y_Axis"]["HM3"] * (1 if l1_trigger else 0) +  self.direction_values["Rotation"]["Y_Axis"]["HM3"] * (1 if r1_trigger else 0))
        
        if self.gyro != None and gyro_enabled:
            # Get sensor data
            data = self.gyro.getData()
            gyro_x, gyro_y = data[0], data[1]          # Roll, Pitch rates
            accel_x, accel_y, accel_z = data[3], data[4], data[5]  # Accelerometer
            
            # Apply stabilization
            corrections = self.update_pd_controller(gyro_x, gyro_y, accel_x, accel_y, accel_z)
            vmotor1 += corrections[0]
            vmotor2 += corrections[1]
            vmotor3 += corrections[2]
         
        # Capping values between -1 and 1
        vmotor1, vmotor2, vmotor3 = map(lambda v: max(-1, min(1, v)), [vmotor1, vmotor2, vmotor3])
        hmotor1, hmotor2, hmotor3 = map(lambda v: max(-1, min(1, v)), [hmotor1, hmotor2, hmotor3])

        return [vmotor1, vmotor2, vmotor3, hmotor1, hmotor2, hmotor3]
