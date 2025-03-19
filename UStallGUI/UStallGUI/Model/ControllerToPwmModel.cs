using GalaSoft.MvvmLight;
using SharpDX.XInput;
using System;

namespace UStallGUI.Model
{
    public class ControllerToPwmModel : ObservableObject
    {
        public DirectionValues directionValues;

        public float leftJoystickX;
        public float leftJoystickY;
        public float rightJoystickX;
        public float rightJoystickY;
        public bool l1Trigger;
        public bool r1Trigger;
        public float l2Trigger;
        public float r2Trigger;
        public bool dPadUp;
        public bool dPadDown;
        public bool dPadLeft;
        public bool dPadRight;
        public bool buttonA;
        public bool buttonB;
        public bool buttonX;
        public bool buttonY;

        public ControllerToPwmModel(DirectionValues _directionValues)
        {
            directionValues = _directionValues;
        }

        public ControllerToPwmModel UpdateControllerValues(State controllerState)
        {
            LeftJoystickX = controllerState.Gamepad.LeftThumbX / (float)32768;
            LeftJoystickY = controllerState.Gamepad.LeftThumbY / (float)32768;
            RightJoystickX = controllerState.Gamepad.RightThumbX / (float)32768;
            RightJoystickY = controllerState.Gamepad.RightThumbY / (float)32768;
            L2Trigger = controllerState.Gamepad.LeftTrigger / (float)255;
            R2Trigger = controllerState.Gamepad.RightTrigger / (float)255;

            L1Trigger = (controllerState.Gamepad.Buttons & GamepadButtonFlags.LeftShoulder) != 0;
            R1Trigger = (controllerState.Gamepad.Buttons & GamepadButtonFlags.RightShoulder) != 0;
            // Update D-Pad values
            DPadUp = (controllerState.Gamepad.Buttons & GamepadButtonFlags.DPadUp) != 0;
            DPadDown = (controllerState.Gamepad.Buttons & GamepadButtonFlags.DPadDown) != 0;
            DPadLeft = (controllerState.Gamepad.Buttons & GamepadButtonFlags.DPadLeft) != 0;
            DPadRight = (controllerState.Gamepad.Buttons & GamepadButtonFlags.DPadRight) != 0;

            // Update button values
            ButtonA = (controllerState.Gamepad.Buttons & GamepadButtonFlags.A) != 0;
            ButtonB = (controllerState.Gamepad.Buttons & GamepadButtonFlags.B) != 0;
            ButtonX = (controllerState.Gamepad.Buttons & GamepadButtonFlags.X) != 0;
            ButtonY = (controllerState.Gamepad.Buttons & GamepadButtonFlags.Y) != 0;

            return this;
        }

        public float[] CalculateMotorValues()
        {
            float vmotor1 = directionValues.Translation.Z_Axis.VM1 * LeftJoystickY + directionValues.Translation.X_Axis.VM1 * LeftJoystickX - directionValues.Translation.Y_Axis.VM1 * L2Trigger + directionValues.Translation.Y_Axis.VM1 * R2Trigger;
            float vmotor2 = directionValues.Translation.Z_Axis.VM2 * LeftJoystickY + directionValues.Translation.X_Axis.VM2 * LeftJoystickX - directionValues.Translation.Y_Axis.VM2 * L2Trigger + directionValues.Translation.Y_Axis.VM2 * R2Trigger;
            float vmotor3 = directionValues.Translation.Z_Axis.VM3 * LeftJoystickY + directionValues.Translation.X_Axis.VM3 * LeftJoystickX - directionValues.Translation.Y_Axis.VM3 * L2Trigger + directionValues.Translation.Y_Axis.VM3 * R2Trigger;
            float hmotor1 = directionValues.Translation.Z_Axis.HM1 * LeftJoystickY + directionValues.Translation.X_Axis.HM1 * LeftJoystickX - directionValues.Translation.Y_Axis.HM1 * L2Trigger + directionValues.Translation.Y_Axis.HM1 * R2Trigger;
            float hmotor2 = directionValues.Translation.Z_Axis.HM2 * LeftJoystickY + directionValues.Translation.X_Axis.HM2 * LeftJoystickX - directionValues.Translation.Y_Axis.HM2 * L2Trigger + directionValues.Translation.Y_Axis.HM2 * R2Trigger;
            float hmotor3 = directionValues.Translation.Z_Axis.HM3 * LeftJoystickY + directionValues.Translation.X_Axis.HM3 * LeftJoystickX - directionValues.Translation.Y_Axis.HM3 * L2Trigger + directionValues.Translation.Y_Axis.HM3 * R2Trigger;
            //Rotation
            vmotor1 += directionValues.Rotation.Z_Axis.VM1 * RightJoystickY + directionValues.Rotation.X_Axis.VM1 * RightJoystickX - directionValues.Rotation.Y_Axis.VM1 * (L1Trigger ? 1 : 0) + directionValues.Rotation.Y_Axis.VM1 * (R1Trigger ? 1 : 0);
            vmotor2 += directionValues.Rotation.Z_Axis.VM2 * RightJoystickY + directionValues.Rotation.X_Axis.VM2 * RightJoystickX - directionValues.Rotation.Y_Axis.VM2 * (L1Trigger ? 1 : 0) + directionValues.Rotation.Y_Axis.VM2 * (R1Trigger ? 1 : 0);
            vmotor3 += directionValues.Rotation.Z_Axis.VM3 * RightJoystickY + directionValues.Rotation.X_Axis.VM3 * RightJoystickX - directionValues.Rotation.Y_Axis.VM3 * (L1Trigger ? 1 : 0) + directionValues.Rotation.Y_Axis.VM3 * (R1Trigger ? 1 : 0);
            hmotor1 += directionValues.Rotation.Z_Axis.HM1 * RightJoystickY + directionValues.Rotation.X_Axis.HM1 * RightJoystickX - directionValues.Rotation.Y_Axis.HM1 * (L1Trigger ? 1 : 0) + directionValues.Rotation.Y_Axis.HM1 * (R1Trigger ? 1 : 0);
            hmotor2 += directionValues.Rotation.Z_Axis.HM2 * RightJoystickY + directionValues.Rotation.X_Axis.HM2 * RightJoystickX - directionValues.Rotation.Y_Axis.HM2 * (L1Trigger ? 1 : 0) + directionValues.Rotation.Y_Axis.HM2 * (R1Trigger ? 1 : 0);
            hmotor3 += directionValues.Rotation.Z_Axis.HM3 * RightJoystickY + directionValues.Rotation.X_Axis.HM3 * RightJoystickX - directionValues.Rotation.Y_Axis.HM3 * (L1Trigger ? 1 : 0) + directionValues.Rotation.Y_Axis.HM3 * (R1Trigger ? 1 : 0);

            //// Scale values
            //ScaleValues(ref vmotor1, ref vmotor2, ref vmotor3);
            //ScaleValues(ref hmotor1, ref hmotor2, ref hmotor3);
            // Capping is more reasonable ??
            vmotor1 = Math.Min(Math.Max(vmotor1, -1f), 1f);
            vmotor2 = Math.Min(Math.Max(vmotor2, -1f), 1f);
            vmotor3 = Math.Min(Math.Max(vmotor3, -1f), 1f);
            hmotor1 = Math.Min(Math.Max(hmotor1, -1f), 1f);
            hmotor2 = Math.Min(Math.Max(hmotor2, -1f), 1f);
            hmotor3 = Math.Min(Math.Max(hmotor3, -1f), 1f);
            // Return motor values
            return new float[] { vmotor1, vmotor2, vmotor3, hmotor1, hmotor2, hmotor3 };
        }

        public void ScaleValues(ref float vmotor1, ref float vmotor2, ref float vmotor3)
        {
            // Find the maximum absolute value among the three values
            float maxValue = Math.Max(Math.Abs(vmotor1), Math.Max(Math.Abs(vmotor2), Math.Abs(vmotor3)));

            // Check if maxValue is greater than 1
            if (maxValue > 1)
            {
                // Scale all values back by dividing them by maxValue
                vmotor1 /= maxValue;
                vmotor2 /= maxValue;
                vmotor3 /= maxValue;
            }
        }

        public override string ToString()
        {
            return $"LeftJoystickX: {LeftJoystickX}, LeftJoystickY: {LeftJoystickY}, RightJoystickX: {RightJoystickX}, RightJoystickY: {RightJoystickY}\n" +
                   $"L1Trigger: {L1Trigger}, R1Trigger: {R1Trigger}, L2Trigger: {L2Trigger}, R2Trigger: {R2Trigger}\n" +
                   $"DPadUp: {DPadUp}, DPadDown: {DPadDown}, DPadLeft: {DPadLeft}, DPadRight: {DPadRight}\n" +
                   $"ButtonA: {ButtonA}, ButtonB: {ButtonB}, ButtonX: {ButtonX}, ButtonY: {ButtonY}";
        }

        // Properties with notification
        public float LeftJoystickX
        {
            get { return leftJoystickX; }
            set { Set(ref leftJoystickX, value); }
        }

        public float LeftJoystickY
        {
            get { return leftJoystickY; }
            set { Set(ref leftJoystickY, value); }
        }

        public float RightJoystickX
        {
            get { return rightJoystickX; }
            set { Set(ref rightJoystickX, value); }
        }

        public float RightJoystickY
        {
            get { return rightJoystickY; }
            set { Set(ref rightJoystickY, value); }
        }

        public bool L1Trigger
        {
            get { return l1Trigger; }
            set { Set(ref l1Trigger, value); }
        }

        public bool R1Trigger
        {
            get { return r1Trigger; }
            set { Set(ref r1Trigger, value); }
        }

        public float L2Trigger
        {
            get { return l2Trigger; }
            set { Set(ref l2Trigger, value); }
        }

        public float R2Trigger
        {
            get { return r2Trigger; }
            set { Set(ref r2Trigger, value); }
        }

        public bool DPadUp
        {
            get { return dPadUp; }
            set { Set(ref dPadUp, value); }
        }

        public bool DPadDown
        {
            get { return dPadDown; }
            set { Set(ref dPadDown, value); }
        }

        public bool DPadLeft
        {
            get { return dPadLeft; }
            set { Set(ref dPadLeft, value); }
        }

        public bool DPadRight
        {
            get { return dPadRight; }
            set { Set(ref dPadRight, value); }
        }

        public bool ButtonA
        {
            get { return buttonA; }
            set { Set(ref buttonA, value); }
        }

        public bool ButtonB
        {
            get { return buttonB; }
            set { Set(ref buttonB, value); }
        }

        public bool ButtonX
        {
            get { return buttonX; }
            set { Set(ref buttonX, value); }
        }

        public bool ButtonY
        {
            get { return buttonY; }
            set { Set(ref buttonY, value); }
        }
    }
}