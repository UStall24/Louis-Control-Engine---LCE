using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace UStallGUI.Model
{
    public class DirectionValues
    {
        public AxisValues Translation { get; set; }
        public AxisValues Rotation { get; set; }

        public void UpdateSingleAxis(Direction dir, Axis axis, float[] values)
        {
            if (dir == Direction.Translation)
            {
                Translation.UpdateAxis(values, axis);
            }
            else
            {
                Rotation.UpdateAxis(values, axis);
            }
        }

        public void SwitchMotors(int m1, int m2)
        {
            Translation.SwitchMotors(m1, m2);
            Rotation.SwitchMotors(m1, m2);
        }

        public static DirectionValues GetDefaultDirectionValues()
        {
            var value = new DirectionValues();
            value.Translation = AxisValues.GetDefaultAxisValues();
            value.Rotation = AxisValues.GetDefaultAxisValues();
            return value;
        }
    }

    public enum Axis
    {
        Z_Axis,
        X_Axis,
        Y_Axis
    }

    public enum Direction
    {
        Translation,
        Rotation
    }

    public class MotorValues
    {
        public float VM1 { get; set; }
        public float VM2 { get; set; }
        public float VM3 { get; set; }
        public float HM1 { get; set; }
        public float HM2 { get; set; }
        public float HM3 { get; set; }

        public MotorValues()
        { }

        public MotorValues(float[] array)
        {
            UpdateAsArray(array);
        }

        public float[] GetAsArray()
        {
            float[] array = { VM1, VM2, VM3, HM1, HM2, HM3 };
            return array;
        }

        public void UpdateAsArray(float[] array)
        {
            VM1 = array[0];
            VM2 = array[1];
            VM3 = array[2];
            HM1 = array[3];
            HM2 = array[4];
            HM3 = array[5];
        }

        public void SwitchMotors(int m1, int m2)
        {
            float[] array = GetAsArray();
            float temp = array[m1 - 1];
            array[m1 - 1] = array[m2 - 1];
            array[m2 - 1] = temp;
            UpdateAsArray(array);
        }

        public static MotorValues GetDefaultMotorValues()
        {
            var motorValues = new MotorValues();
            motorValues.VM1 = 0;
            motorValues.VM2 = 0;
            motorValues.VM3 = 0;
            motorValues.HM1 = 0;
            motorValues.HM2 = 0;
            motorValues.HM3 = 0;
            return motorValues;
        }

        public override string ToString()
        {
            return $"VM1: {VM1}, VM2: {VM2}, VM3: {VM3}, HM1: {HM1}, HM2: {HM2}, HM3: {HM3}";
        }
    }

    public class AxisValues
    {
        public MotorValues Z_Axis { get; set; }
        public MotorValues X_Axis { get; set; }
        public MotorValues Y_Axis { get; set; }

        public void UpdateAxis(float[] array, Axis axis)
        {
            if (axis == Axis.Z_Axis)
            {
                Z_Axis.UpdateAsArray(array);
            }
            else if (axis == Axis.Y_Axis)
            {
                Y_Axis.UpdateAsArray(array);
            }
            else if (axis == Axis.X_Axis)
            {
                X_Axis.UpdateAsArray(array);
            }
        }

        public void SwitchMotors(int m1, int m2)
        {
            Z_Axis.SwitchMotors(m1, m2);
            Y_Axis.SwitchMotors(m1, m2);
            X_Axis.SwitchMotors(m1, m2);
        }

        public static AxisValues GetDefaultAxisValues()
        {
            var value = new AxisValues();
            value.X_Axis = MotorValues.GetDefaultMotorValues();
            value.Y_Axis = MotorValues.GetDefaultMotorValues();
            value.Z_Axis = MotorValues.GetDefaultMotorValues();
            return value;
        }
    }
}