using GalaSoft.MvvmLight;
using SharpDX.XInput;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using UStallGUI.Model;

namespace Greifer_GUI.Model
{
    public class GripperModel() : ObservableObject
    {
        private double a1m1 = 0;
        public double A1M1
        {
            get => a1m1;
            set => Set(ref a1m1, value);
        }

        private double a1m2 = 0;
        public double A1M2
        {
            get => a1m2;
            set => Set(ref a1m2, value);
        }

        private byte a1m3 = 0;
        public byte A1M3
        {
            get => a1m3;
            set => Set(ref a1m3, value);
        }

        private double a1m4 = 0;
        public double A1M4
        {
            get => a1m4;
            set => Set(ref a1m4, value);
        }

        private double a2m1 = 0;
        public double A2M1
        {
            get => a2m1;
            set => Set(ref a2m1, value);
        }

        private double a2m2 = 0;
        public double A2M2
        {
            get => a2m2;
            set => Set(ref a2m2, value);
        }

        private byte a2m3 = 0;
        public byte A2M3
        {
            get => a2m3;
            set => Set(ref a2m3, value);
        }

        private double a2m4 = 0;
        public double A2M4
        {
            get => a2m4;
            set => Set(ref a2m4, value);
        }

        public double speedFactorAngle { get; set; } = 1/3000.0;

        DateTime lastCallTime = DateTime.Now;

        public byte[] GetGripperBytes(ControllerModel controllerModel)
        {
            DateTime now = DateTime.Now;
            double deltaT = (now - lastCallTime).TotalSeconds;
            lastCallTime = now;
            double deltaAngle = controllerModel.RightJoystickY * deltaT * speedFactorAngle;
            double velocity = (controllerModel.RightJoystickY + 32768) / 256;
            if (controllerModel.SelectedDPad == 1)
            {
                A1M1 = (controllerModel.SelectedButton == 1) ? A1M1 + deltaAngle : A1M1;
                A1M2 = (controllerModel.SelectedButton == 2) ? A1M2 + deltaAngle : A1M2;
                A1M3 = (byte)((controllerModel.SelectedButton == 3) ? velocity : A1M3);
                A1M4 = (controllerModel.SelectedButton == 4) ? A1M4 + deltaAngle : A1M4;
            }
            else if (controllerModel.SelectedDPad == 2)
            {
                A2M1 = (controllerModel.SelectedButton == 1) ? A2M1 + deltaAngle : A2M1;
                A2M2 = (controllerModel.SelectedButton == 2) ? A2M2 + deltaAngle : A2M2;
                A2M3 = (byte)((controllerModel.SelectedButton == 3) ? velocity : A2M3);
                A2M4 = (controllerModel.SelectedButton == 4) ? A2M4 + deltaAngle : A2M4;
            }
            byte[] value = {MapAngleToByte(A1M1), 
                            MapAngleToByte(A1M2),
                            A1M3,
                            MapAngleToByte(A1M4),
                            MapAngleToByte(A2M1),
                            MapAngleToByte(A2M2), 
                            A2M3, 
                            MapAngleToByte(A2M4) };
            return value;
        }
        public string GetGripperBytesAsString(ControllerModel controllerModel)
        {
            byte[] gripperBytes = GetGripperBytes(controllerModel);
            return string.Join(", ", gripperBytes);
        }
        private byte MapAngleToByte(double angle)
        {
            // Begrenzung auf gültigen Bereich
            angle = Math.Clamp(angle, -70.0, 70.0);

            // Mapping von [-70, +70] → [0, 255]
            double normalized = (angle + 70.0) / 140.0;
            return (byte)(normalized * 255.0);
        }
    }
}
