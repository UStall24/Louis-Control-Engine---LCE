using GalaSoft.MvvmLight;
using GalaSoft.MvvmLight.Command;
using System;
using System.Collections.Generic;
using System.IO.Ports;
using System.Threading;
using System.Threading.Tasks;
using System.Windows.Input;
using System.Windows.Threading;
using UStallGUI.Helpers;
using UStallGUI.Model;

namespace UStallGUI.ViewModel
{
    public class MainWindowViewModel : ObservableObject
    {
        public static MainWindowViewModel Instance;

        private readonly Timer manualValueTimer;

        private string consoleText = "";
        private string connectionStatusLCE;
        private string connectionStatusController = "Not Connected";

        private List<string> messages = new List<string>();
        private SerialPortHelper serialPortHelper;

        public MainWindowViewModel()
        {
            Instance = this;
            ConnectToLouisControlEngine = new RelayCommand(TaskConnectToLouisControlEngine);
            DisconnectToLouisControlEngine = new RelayCommand(TaskDisconnectToLouisControlEngine);
            //FindConnectedControllers = new RelayCommand();
            _UpdateConnectionStatusLCE(0);
            manualValueTimer = new Timer(SendManualValues, null, 1000, 100);
        }

        private void SendManualValues(object? state)
        {
            if (SendManualSetValues)
            {
                byte[] motorValuesBytes = LCECommunicationHelper.ConvertMotorValuesToBytes(GetManualMotorValues);

                serialPortHelper.WriteBytes(0x69, motorValuesBytes);
            }
        }

        public void TaskConnectToLouisControlEngine()
        {
            TaskDisconnectToLouisControlEngine();
            serialPortHelper = new SerialPortHelper(comValue);
            bool wasSuccessful = serialPortHelper.Open();
            if (!wasSuccessful)
            {
                ConsoleText = "Error connecting";
                return;
            }
            ConsoleText = "Connection Buildup Successful";
            serialPortHelper.serialPort.DataReceived += SerialPort_DataReceived;
            serialPortHelper.WriteBytes(0x99, LCECommunicationHelper.GetStartBytes);
            ConsoleText = "LCE Startup Successful";
        }

        private async void _UpdateConnectionStatusLCE(int status)
        {
            switch (status)
            {
                case 0:
                    ConnectionStatusLCE = "No active connection";
                    break;

                case 1:
                    ConnectionStatusLCE = "Connecting...";
                    break;

                case 2:
                    ConnectionStatusLCE = "Connected";
                    break;

                case 3:
                    ConnectionStatusLCE = "Error Connecting";
                    await Task.Delay(1000);
                    _UpdateConnectionStatusLCE(0);
                    break;
            }
        }

        private void SerialPort_DataReceived(object sender, SerialDataReceivedEventArgs e)
        {
            string message = serialPortHelper.ReadBytesString();
            ConsoleText = message;
        }

        public void WriteToLCE(byte[] bytes)
        {
            if (SendControllerValues)
            {
                serialPortHelper.WriteBytes(0x69, bytes);
            }
        }

        public void TaskDisconnectToLouisControlEngine()
        {
            if (serialPortHelper != null && serialPortHelper.IsOpen)
            {
                bool closingSuccessful = serialPortHelper.Close();
                serialPortHelper.serialPort.DataReceived -= SerialPort_DataReceived;
                ConsoleText = closingSuccessful ? "Closing successful" : "Closing failed";
            }
            else
            {
                ConsoleText = "Serialport is currently closed";
            }
        }

        private float[] GetManualMotorValues
        {
            get => new float[] { MotorV1, MotorV2, MotorV3, MotorH1, MotorH2, MotorH3 };
        }

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

        private int comValue = 6;

        public int ComValue
        {
            get => comValue;
            set => Set(ref comValue, value);
        }

        private readonly Queue<string> consoleHistory = new Queue<string>(10); // Queue to store the last 10 values

        private int counter = 1; // Counter to track the number of values

        public string ConsoleText
        {
            get => consoleText;
            set
            {
                // Prepend the counter to the new value
                string newValue = $"[{counter}] - {value}";

                // Add the new value to the queue
                consoleHistory.Enqueue(newValue);

                // Ensure the queue never exceeds 10 items
                if (consoleHistory.Count > 10)
                {
                    consoleHistory.Dequeue(); // Remove the oldest value
                }

                // Join the values in the queue to form the console text
                var newConsoleText = string.Join(Environment.NewLine, consoleHistory);

                // Update the property
                Set(ref consoleText, newConsoleText);

                // Increment the counter
                counter++;
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