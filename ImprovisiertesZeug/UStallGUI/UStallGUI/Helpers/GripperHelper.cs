using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Greifer_GUI.Helpers
{
    public static class GripperHelper
    {
        public static byte AngleToByte(float angle, float min = -70f, float max = 70f)
        {
            angle = Math.Max(min, Math.Min(max, angle));

            // Skaliere in den Bereich 0–255
            float normalized = (angle - min) / (max - min); // ergibt 0.0–1.0
            return (byte)(normalized * 255f);
        }
        public static byte PercentToByte(float percent, float min = -100f, float max = 100f)
        {
            percent = Math.Max(min, Math.Min(max, percent));
            float normalized = (percent - min) / (max - min);
            return (byte)(normalized * 255f);
        }
    }
}
