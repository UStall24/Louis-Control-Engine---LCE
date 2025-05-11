using System;
using GalaSoft.MvvmLight;

namespace UStallGUI.Model
{
    public class GripperModel() : ObservableObject
    {
        private double a1m1 = 0;
        public double A1M1 { get => a1m1; set => Set(ref a1m1, Math.Clamp(value, -70, 70)); }

        private double a1m2 = 0;
        public double A1M2 { get => a1m2; set => Set(ref a1m2, Math.Clamp(value, -70, 70)); }

        private double a2m1 = 0;
        public double A2M1 { get => a2m1; set => Set(ref a2m1, Math.Clamp(value, -70, 70)); }

        private double a2m2 = 0;
        public double A2M2 { get => a2m2; set => Set(ref a2m2, Math.Clamp(value, -70, 70)); }

        public byte[] GetGripperBytes()
        {
            byte[] value =
            {
                MapAngleToByte(A1M1),
                MapAngleToByte(A1M2),
                MapAngleToByte(A2M1),
                MapAngleToByte(A2M2),
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
    }
}
