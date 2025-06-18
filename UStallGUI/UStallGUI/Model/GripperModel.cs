using System;
using GalaSoft.MvvmLight;
using UStallGUI.ViewModel;

namespace UStallGUI.Model
{
    public class GripperModel() : ObservableObject
    {
        private double a1m1 = 50;
        public double A1M1 { get => a1m1; set => Set(ref a1m1, Math.Clamp(value, 0, 100)); }

        private double a1m2 = 50;
        public double A1M2 { get => a1m2; set => Set(ref a1m2, Math.Clamp(value, 0, 100)); }

        private double a1m3 = 50;
        public double A1M3 { get => a1m3; set => Set(ref a1m3, Math.Clamp(value, 0, 100)); }

        public byte[] GetGripperBytes()
        {
            byte[] value =
            {
                MapAngleToByte(A1M1, 0, 255),
                MapAngleToByte(A1M2, 0, 255),
                MapAngleToByte(A1M3, 0, 90),
                0,
                0,
                0,
                0,
                0
            };
            return value;
        }

        public string GetGripperBytesAsString()
        {
            byte[] gripperBytes = GetGripperBytes();
            return string.Join(", ", gripperBytes);
        }

        private static byte MapAngleToByte(double angle, double minRange, double maxRange)
        {
            // Begrenzung auf gültigen Bereich
            angle = Math.Clamp(angle, 0, 100);

            byte value = (byte)((angle / 100) * (maxRange - minRange) + minRange);
            return value;
        }

        public string MechproGripperExecuteMessage(GripperAssignment assignment)
        {
            string msg = "";
            switch (assignment)
            {
                case GripperAssignment.Gripper2_Servo1Plus:
                    msg = "hg";
                    break;

                case GripperAssignment.Gripper2_Servo1Minus:
                    msg = "rg";
                    break;

                case GripperAssignment.Gripper2_Servo2Plus:
                    msg = "afg";
                    break;

                case GripperAssignment.Gripper2_Servo2Minus:
                    msg = "efg";
                    break;

                case GripperAssignment.Gripper2_PumpOn:
                    msg = "P_ein_G";
                    break;

                case GripperAssignment.Gripper2_DefaultPosition:
                    msg = "GS_G";
                    break;
            }

            return msg;
        }
    }
}