using System;

namespace UStallGUI.Helpers
{
    public class LCECommunicationHelper
    {
        public static byte[] ConvertMotorValuesToBytes(float[] motorValues)
        {
            if (motorValues == null)
            {
                throw new ArgumentNullException(nameof(motorValues));
            }

            byte[] byteArray = new byte[motorValues.Length];

            for (int i = 0; i < motorValues.Length; i++)
            {
                byte byteValue = 0x7F; // 127 dez -> 7F hex and 128 dez -> 80 dez the zero points for the ROV
                if (Math.Abs(motorValues[i]) > 1e-3)
                {
                    byteValue = (byte)((motorValues[i] + 1) * 127.5);
                }
                byteArray[i] = byteValue;
            }

            return byteArray;
        }

        public static float[] ConvertBytesToMotorValues(byte[] byteArray, bool roundUp = true)
        {
            if (byteArray == null)
            {
                throw new ArgumentNullException(nameof(byteArray));
            }

            float[] motorVals = new float[byteArray.Length];

            for (int i = 0; i < byteArray.Length; i++)
            {
                motorVals[i] = (float)(Math.Round((byteArray[i] / 127.5f) - 1, 2));
            }

            return motorVals;
        }

        public static byte[] GetStartBytes => new byte[] { 0xAA, 0xBB, 0xCC, 0xDD, 0xEE, 0xFF };
    }
}