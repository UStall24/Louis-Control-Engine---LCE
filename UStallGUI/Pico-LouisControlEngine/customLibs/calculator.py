class Calculator:
    def __init__(self, direction_values):
        # Motor PWM limits
        self.maxPWM = 1700
        self.minPWM = 1300
        self.deadZoneMin = 1464
        self.deadZoneMax = 1536
        self.deadZoneDefault = 1500
        
        self.direction_values = direction_values
        
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
        
        # Capping values between -1 and 1
        vmotor1, vmotor2, vmotor3 = map(lambda v: max(-1, min(1, v)), [vmotor1, vmotor2, vmotor3])
        hmotor1, hmotor2, hmotor3 = map(lambda v: max(-1, min(1, v)), [hmotor1, hmotor2, hmotor3])

        return [vmotor1, vmotor2, vmotor3, hmotor1, hmotor2, hmotor3]
