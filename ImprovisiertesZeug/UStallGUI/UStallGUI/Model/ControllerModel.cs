using GalaSoft.MvvmLight;
using SharpDX.XInput;

namespace UStallGUI.Model
{
    public class ControllerModel(Controller controller = null) : ObservableObject
    {
        // Variables used one time
        private readonly Controller controller = controller;

        // Variables to avoid excess declaring
        private State controllerState;

        /// Binding Variables
        // Movement
        public byte LeftJoystickX { get; set; } = 0;
        public byte LeftJoystickY { get; set; } = 0;
        public byte RightJoystickX { get; set; } = 0;
        
        public bool L1Trigger { get; set; } = false;
        public bool R1Trigger { get; set; } = false;
        public byte L2Trigger { get; set; } = 0;
        public byte R2Trigger { get; set; } = 0;

        // Gripper Variables
        public short RightJoystickY { get; set; } = 0;
        public bool ButtonA { get; set; } = false;
        public bool ButtonB { get; set; } = false;
        public bool ButtonX { get; set; } = false;
        public bool ButtonY { get; set; } = false;
        private bool LastA { get; set; } = false;
        private bool LastB { get; set; } = false;
        private bool LastX { get; set; } = false;
        private bool LastY { get; set; } = false;
        public byte SelectedButton { get; set; } = 0;
        public bool DPadLeft { get; set; } = false;
        public bool DPadRight { get; set; } = false;
        public byte SelectedDPad {  get; set; } = 0;
        // Free Variables
        public bool LeftJoystickDown { get; set; } = false;
        public bool RightJoystickDown { get; set; } = false;
        public bool DPadUp { get; set; } = false;
        public bool DPadDown { get; set; } = false;

        public bool ButtonStart { get; set; } = false;
        public bool ButtonBack { get; set; } = false;

 

        public void UpdateControllerValues()
        {
            if(controller != null)
            {
                controllerState = controller.GetState();
                // Movement Variables
                LeftJoystickX = (byte)((controllerState.Gamepad.LeftThumbX + 32768) / 256);
                LeftJoystickY = (byte)((controllerState.Gamepad.LeftThumbY + 32768) / 256);
                RightJoystickX = (byte)((controllerState.Gamepad.RightThumbX + 32768) / 256);
                RightJoystickY = controllerState.Gamepad.RightThumbY ;
                L2Trigger = controllerState.Gamepad.LeftTrigger;
                R2Trigger = controllerState.Gamepad.RightTrigger;

                L1Trigger = (controllerState.Gamepad.Buttons & GamepadButtonFlags.LeftShoulder) != 0;
                R1Trigger = (controllerState.Gamepad.Buttons & GamepadButtonFlags.RightShoulder) != 0;

                // Free Variables
                // Update D-Pad values
                DPadUp = (controllerState.Gamepad.Buttons & GamepadButtonFlags.DPadUp) != 0;
                DPadDown = (controllerState.Gamepad.Buttons & GamepadButtonFlags.DPadDown) != 0;
                DPadLeft = (controllerState.Gamepad.Buttons & GamepadButtonFlags.DPadLeft) != 0;
                DPadRight = (controllerState.Gamepad.Buttons & GamepadButtonFlags.DPadRight) != 0;
                updateDPad();

                // Update button values
                ButtonA = (controllerState.Gamepad.Buttons & GamepadButtonFlags.A) != 0;
                ButtonB = (controllerState.Gamepad.Buttons & GamepadButtonFlags.B) != 0;
                ButtonX = (controllerState.Gamepad.Buttons & GamepadButtonFlags.X) != 0;
                ButtonY = (controllerState.Gamepad.Buttons & GamepadButtonFlags.Y) != 0;
                updateButtons();

                // Update Start and Back buttons
                ButtonStart = (controllerState.Gamepad.Buttons & GamepadButtonFlags.Start) != 0;
                ButtonBack = (controllerState.Gamepad.Buttons & GamepadButtonFlags.Back) != 0;
                LeftJoystickDown = (controllerState.Gamepad.Buttons & GamepadButtonFlags.LeftThumb) != 0;
                RightJoystickDown = (controllerState.Gamepad.Buttons & GamepadButtonFlags.RightThumb) != 0;
                

            }
        }

        public byte[] GetMovementBytes()
        {
            byte l1r1Trigger = (byte)((L1Trigger ? 1 : 0) + (R1Trigger ? 2 : 0));
            byte[] value = { LeftJoystickX, LeftJoystickY, RightJoystickX, L2Trigger, R2Trigger, l1r1Trigger };
            return value;
        }


        private void updateButtons()
        {

            if (ButtonA && !LastA)
            {
                SelectedButton = (byte)((SelectedButton == 1) ? 0 : 1);
            }
            else if (ButtonB && !LastB)
            {
                SelectedButton = (byte)((SelectedButton == 2) ? 0 : 2);
            }
            else if (ButtonX && !LastX)
            {
                SelectedButton = (byte)((SelectedButton == 3) ? 0 : 3);
            }
            else if (ButtonY && !LastY)
            {
                SelectedButton = (byte)((SelectedButton == 4) ? 0 : 4);
            }
            LastA = ButtonA;
            LastB = ButtonB;
            LastX = ButtonX;
            LastY = ButtonY;
        }
        private void updateDPad()
        {
            if (DPadLeft)
            {
                SelectedDPad = 1;
            }
            else if (DPadRight)
            {
                SelectedDPad = 2;
            }
        }

        public string GetMovementBytesAsString()
        {
            byte[] movementBytes = GetMovementBytes();
            return string.Join(", ", movementBytes);
        }


        public override string ToString()
        {
            return $"LeftJoystickX: {LeftJoystickX}, LeftJoystickY: {LeftJoystickY}, RightJoystickX: {RightJoystickX}, RightJoystickY: {RightJoystickY}\n" +
                   $"L1Trigger: {L1Trigger}, R1Trigger: {R1Trigger}, L2Trigger: {L2Trigger}, R2Trigger: {R2Trigger}\n" +
                   $"DPadUp: {DPadUp}, DPadDown: {DPadDown}, DPadLeft: {DPadLeft}, DPadRight: {DPadRight}\n" +
                   $"ButtonA: {ButtonA}, ButtonB: {ButtonB}, ButtonX: {ButtonX}, ButtonY: {ButtonY}";
        }


    }
}