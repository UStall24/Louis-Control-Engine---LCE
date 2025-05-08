using GalaSoft.MvvmLight;
using GalaSoft.MvvmLight.Command;
using Greifer_GUI.Helpers;
using Microsoft.Win32;
using System.Collections.Generic;
using System.IO.Ports;
using System.Linq;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Documents;
using UStallGUI.Helpers;
using UStallGUI.Model;

namespace UStallGUI.ViewModel
{
    public class ControlGripperViewModel : ObservableObject
    {
        private string _a1m1_manuel;
        private string _a1m2_manuel;
        private string _a1m3_manuel;
        private string _a1m4_manuel;
        private string _a2m1_manuel;
        private string _a2m2_manuel;
        private string _a2m3_manuel;
        private string _a2m4_manuel;

        private string _a1m1_init;
        private string _a1m2_init;
        private string _a1m3_init;
        private string _a1m4_init;
        private string _a2m1_init;
        private string _a2m2_init;
        private string _a2m3_init;
        private string _a2m4_init;
        public string A1M1_Manuel
        {
            get => _a1m1_manuel;
            set => Set(ref _a1m1_manuel, value);
        }
        public string A1M2_Manuel
        {
            get => _a1m2_manuel;
            set => Set(ref _a1m2_manuel, value);
        }
        public string A1M3_Manuel
        {
            get => _a1m3_manuel;
            set => Set(ref _a1m3_manuel, value);
        }
        public string A1M4_Manuel
        {
            get => _a1m4_manuel;
            set => Set(ref _a1m4_manuel, value);
        }
        public string A2M1_Manuel
        {
            get => _a2m1_manuel;
            set => Set(ref _a2m1_manuel, value);
        }
        public string A2M2_Manuel
        {
            get => _a2m2_manuel;
            set => Set(ref _a2m2_manuel, value);
        }
        public string A2M3_Manuel
        {
            get => _a2m3_manuel;
            set => Set(ref _a2m3_manuel, value);
        }
        public string A2M4_Manuel
        {
            get => _a2m4_manuel;
            set => Set(ref _a2m4_manuel, value);
        }

        public string A1M1_Init
        {
            get => _a1m1_manuel;
            set => Set(ref _a1m1_manuel, value);
        }
        public string A1M2_Init
        {
            get => _a1m2_init;
            set => Set(ref _a1m2_init, value);
        }
        public string A1M3_Init
        {
            get => _a1m3_init;
            set => Set(ref _a1m3_init, value);
        }
        public string A1M4_Init
        {
            get => _a1m4_init;
            set => Set(ref _a1m4_init, value);
        }
        public string A2M1_Init
        {
            get => _a2m1_init;
            set => Set(ref _a2m1_init, value);
        }
        public string A2M2_Init
        {
            get => _a2m2_init;
            set => Set(ref _a2m2_init, value);
        }
        public string A2M3_Init
        {
            get => _a2m3_init;
            set => Set(ref _a2m3_init, value);
        }
        public string A2M4_Init
        {
            get => _a2m4_init;
            set => Set(ref _a2m4_init, value);
        }


        public RelayCommand GoToValuesCommand { get; }
        public RelayCommand GoToInitCommand { get; }

        public ControlGripperViewModel()
        {
            GoToValuesCommand = new RelayCommand(GoToValuesHandler);
            GoToInitCommand = new RelayCommand(GoToInitHandler);
        }

        private void GoToValuesHandler()
        {
            if (float.TryParse(A1M1_Manuel, out float wert1) &&
                float.TryParse(A1M2_Manuel, out float wert2) &&
                float.TryParse(A1M3_Manuel, out float wert3) &&
                float.TryParse(A1M4_Manuel, out float wert4) &&
                float.TryParse(A2M1_Manuel, out float wert5) &&
                float.TryParse(A2M2_Manuel, out float wert6) &&
                float.TryParse(A2M3_Manuel, out float wert7) &&
                float.TryParse(A2M4_Manuel, out float wert8))
            {
                byte b1 = GripperHelper.AngleToByte(wert1);
                byte b2 = GripperHelper.AngleToByte(wert2);
                byte b3 = GripperHelper.PercentToByte(wert3);
                byte b4 = GripperHelper.AngleToByte(wert4);
                byte b5 = GripperHelper.AngleToByte(wert5);
                byte b6 = GripperHelper.AngleToByte(wert6);
                byte b7 = GripperHelper.PercentToByte(wert7);
                byte b8 = GripperHelper.AngleToByte(wert8);

                byte[] manuelTargetValues = new byte[] { b1, b2, b3, b4, b5, b6, b7, b8};

                SerialPortHandler.Instance.WriteBytes(LCE_CommandAddresses.UpdateGripperValues, manuelTargetValues); // Adresse anpassen
            }
        }
        private void GoToInitHandler()
        {
            if (float.TryParse(A1M1_Init, out float wert1) &&
                float.TryParse(A1M2_Init, out float wert2) &&
                float.TryParse(A1M3_Init, out float wert3) &&
                float.TryParse(A1M4_Init, out float wert4) &&
                float.TryParse(A2M1_Init, out float wert5) &&
                float.TryParse(A2M2_Init, out float wert6) &&
                float.TryParse(A2M3_Init, out float wert7) &&
                float.TryParse(A2M4_Init, out float wert8))
            {
                byte b1 = GripperHelper.AngleToByte(wert1);
                byte b2 = GripperHelper.AngleToByte(wert2);
                byte b3 = GripperHelper.PercentToByte(wert3);
                byte b4 = GripperHelper.AngleToByte(wert4);
                byte b5 = GripperHelper.AngleToByte(wert5);
                byte b6 = GripperHelper.AngleToByte(wert6);
                byte b7 = GripperHelper.PercentToByte(wert7);
                byte b8 = GripperHelper.AngleToByte(wert8);

                byte[] initTargetValues = new byte[] { b1, b2, b3, b4, b5, b6, b7, b8 };

                SerialPortHandler.Instance.WriteBytes(LCE_CommandAddresses.UpdateGripperValues, initTargetValues); // Adresse anpassen
            }
        }

    }
}