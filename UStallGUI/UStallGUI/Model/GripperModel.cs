using System;
using GalaSoft.MvvmLight;
using UStallGUI.ViewModel;

namespace UStallGUI.Model
{
    public class GripperModel() : ObservableObject
    {
        private double a1m1 = 0;
        public double A1M1 { get => a1m1; set => Set(ref a1m1, Math.Clamp(value, -70, 70)); }

        private double a1m2 = 0;
        public double A1M2 { get => a1m2; set => Set(ref a1m2, Math.Clamp(value, -70, 70)); }

        private double a1m3 = 0;
        public double A1M3 { get => a1m3; set => Set(ref a1m3, Math.Clamp(value, -70, 70)); }

        public byte[] GetGripperBytes()
        {
            byte[] value =
            {
                MapAngleToByte(A1M1),
                MapAngleToByte(A1M2),
                MapAngleToByte(A1M3),
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

        private static byte MapAngleToByte(double angle)
        {
            // Begrenzung auf gültigen Bereich
            angle = Math.Clamp(angle, -70.0, 70.0);

            // Mapping von [-70, +70] → [0, 255]
            double normalized = (angle + 70.0) / 140.0;
            return (byte)(normalized * 255.0);
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