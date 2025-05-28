using System.Threading;
using GalaSoft.MvvmLight;
using GalaSoft.MvvmLight.Command;
using UStallGUI.Helpers;
using UStallGUI.Model;

namespace UStallGUI.ViewModel
{
    public class MainWindowViewModel : ObservableObject
    {
        public static MainWindowViewModel Instance;

        private readonly Timer manualValueTimer;
        private string connectionStatusLCE;
        private string connectionStatusController = "Not Connected";

        private SerialPortHandler serialPortHelper;

        public MainWindowViewModel()
        {
            Instance = this;
            UpdateConnectionStatusLCE(0);
            manualValueTimer = new Timer(SendManualValues, null, 1000, 100);
        }

        private void SendManualValues(object? state)
        {
            //Console.WriteLine($"[Timer] SendManualValues() aufgerufen. SendManualSetValues = {SendManualSetValues}");

            if (SendManualSetValues)
            {
                var motorValues = GetManualMotorValues;
                //Console.WriteLine($"[Timer] Manuelle Werte: {string.Join(", ", motorValues)}");

                byte[] motorValuesBytes = LCECommunicationHelper.ConvertMotorValuesToBytes(motorValues);

                //Console.WriteLine($"[Timer] Bytes zum Senden: {BitConverter.ToString(motorValuesBytes)}");

                serialPortHelper?.WriteBytes(0x69, motorValuesBytes);
            }
        }


        private readonly string[] lce_connection_messages = { "No active connection", "Connecting...", "Connected", "Error Connecting", "Closing Successful", "Closing Failed" };

        private int lce_connection_index = 0;

        public void UpdateConnectionStatusLCE(int status)
        {
            if (status >= 0 && status < lce_connection_messages.Length && status != lce_connection_index)
            {
                lce_connection_index = status;
                ConnectionStatusLCE = lce_connection_messages[lce_connection_index];
                ControlBoxConsoleText = $"LCE Connection Status: {lce_connection_messages[lce_connection_index]}";
            }
        }

        public SetupHandlerViewModel SetupVM { get; } = new();

        private float[] GetManualMotorValues => new float[]
        {
            SetupVM.ManualControlValues.VM1,
            SetupVM.ManualControlValues.VM2,
            SetupVM.ManualControlValues.VM3,
            SetupVM.ManualControlValues.HM1,
            SetupVM.ManualControlValues.HM2,
            SetupVM.ManualControlValues.HM3
        };


        private float _motorV1 = 0;
        private float _motorV2 = 0;
        private float _motorV3 = 0;
        private float _motorH1 = 0;
        private float _motorH2 = 0;
        private float _motorH3 = 0;

        public float MotorV1
        {
            get => _motorV1;
            set => Set(ref _motorV1, LimitValue(value));
        }

        public float MotorV2
        {
            get => _motorV2;
            set => Set(ref _motorV2, LimitValue(value));
        }

        public float MotorV3
        {
            get => _motorV3;
            set => Set(ref _motorV3, LimitValue(value));
        }

        public float MotorH1
        {
            get => _motorH1;
            set => Set(ref _motorH1, LimitValue(value));
        }

        public float MotorH2
        {
            get => _motorH2;
            set => Set(ref _motorH2, LimitValue(value));
        }

        public float MotorH3
        {
            get => _motorH3;
            set => Set(ref _motorH3, LimitValue(value));
        }

        private float LimitValue(float value)
        {
            if (value < -1) return -1;
            if (value > 1) return 1;
            return value;
        }

        private float allMotorH = 0;
        private float allMotorV = 0;

        public float AllMotorH
        {
            get => allMotorH;
            set
            {
                allMotorH = LimitValue(value);
                MotorH1 = allMotorH;
                MotorH2 = allMotorH;
                MotorH3 = allMotorH;
            }
        }

        public float AllMotorV
        {
            get => allMotorV;
            set
            {
                allMotorV = LimitValue(value);
                MotorV1 = allMotorV;
                MotorV2 = allMotorV;
                MotorV3 = allMotorV;
            }
        }

        private int comValue = 15;

        public int ComValue
        {
            get => comValue;
            set => Set(ref comValue, value);
        }

        private readonly ConsoleLog controlBoxLog = new();
        private readonly ConsoleLog accessoryBoxLog = new();

        private string controlBoxConsoleText;
        public string ControlBoxConsoleText
        {
            get => controlBoxConsoleText;
            set
            {
                controlBoxLog.Add(value);
                Set(ref controlBoxConsoleText, controlBoxLog.CurrentText);
            }
        }

        private string accessoryBoxConsoleText;
        public string AccessoryBoxConsoleText
        {
            get => accessoryBoxConsoleText;
            set
            {
                accessoryBoxLog.Add(value);
                Set(ref accessoryBoxConsoleText, accessoryBoxLog.CurrentText);
            }
        }


        // Textfield for the Statusbar Bindings
        public string ConnectionStatusLCE
        {
            get => connectionStatusLCE;
            set => Set(ref connectionStatusLCE, value);
        }

        public string ConnectionStatusController
        {
            get => connectionStatusController;
            set => Set(ref connectionStatusController, value);
        }

        // Checkbox Bindings
        public bool SendManualSetValues { get; set; }

        public bool SendControllerValues { get; set; }

        // Relay Commands
        public RelayCommand ConnectToLouisControlEngine { get; set; }

        public RelayCommand DisconnectToLouisControlEngine { get; set; }
        public RelayCommand FindConnectedControllers { get; set; }
    }
}