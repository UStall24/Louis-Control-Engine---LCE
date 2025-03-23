using GalaSoft.MvvmLight;
using GalaSoft.MvvmLight.Command;
using System;
using System.Collections.Generic;
using System.IO.Ports;
using System.Linq;
using System.Threading;
using System.Threading.Tasks;
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

        private SerialPortHandler serialPortHelper;

        public MainWindowViewModel()
        {
            Instance = this;
            ConnectToLouisControlEngine = new RelayCommand(TaskConnectToLouisControlEngine);
            DisconnectToLouisControlEngine = new RelayCommand(TaskDisconnectToLouisControlEngine);
            UpdateConnectionStatusLCE(0);
            manualValueTimer = new Timer(SendManualValues, null, 1000, 100);
        }

        #region Connecting and Disconnecting

        public async void TaskConnectToLouisControlEngine()
        {
            TaskDisconnectToLouisControlEngine();
            serialPortHelper = new SerialPortHandler(comValue);
            bool wasSuccessful = serialPortHelper.Open();
            if (wasSuccessful)
            {
                wasSuccessful = false;
                UpdateConnectionStatusLCE(1);
                serialPortHelper.WriteBytes(0x99, LCECommunicationHelper.GetStartBytes);
                await Task.Delay(100);
                foreach (var address in lce_state_messages_addresses)
                {
                    byte[] response = serialPortHelper.LookForMessage(address);
                    if (response.Length != 0)
                    {
                        wasSuccessful = true;
                        UpdateConnectionStatusLCE(2);
                        ConsoleText = lce_state_messages[response[0]];
                        break;
                    }
                }
            }

            if (!wasSuccessful)
            {
                UpdateConnectionStatusLCE(3);
                await Task.Delay(3000);
                UpdateConnectionStatusLCE(0);
            }
        }

        public void TaskDisconnectToLouisControlEngine()
        {
            if (serialPortHelper != null && serialPortHelper.IsOpen)
            {
                bool closingSuccessful = serialPortHelper.Close();
                UpdateConnectionStatusLCE(closingSuccessful ? 4 : 5);
            }
            else
            {
                ConsoleText = "Serialport is currently closed";
            }
        }

        #endregion Connecting and Disconnecting

        private void SendManualValues(object? state)
        {
            if (SendManualSetValues)
            {
                byte[] motorValuesBytes = LCECommunicationHelper.ConvertMotorValuesToBytes(GetManualMotorValues);

                serialPortHelper.WriteBytes(0x69, motorValuesBytes);
            }
        }

        private readonly string[] lce_connection_messages = { "No active connection", "Connecting...", "Connected", "Error Connecting", "Closing Successful", "Closing Failed" };
        private readonly byte[] lce_state_messages_addresses = { 0x00, 0x01, 0x02, 0x03 };
        private readonly string[] lce_state_messages = { "Error", "Motor initialization successful", "Recieving Control Data Successful", "Warning: Cycle Time exceeded!" };

        private int lce_connection_index = 0;
        private int lce_state_index = 0;

        private void UpdateConnectionStatusLCE(int status)
        {
            if (status >= 0 && status < lce_connection_messages.Length && status != lce_connection_index)
            {
                lce_connection_index = status;
                ConnectionStatusLCE = lce_connection_messages[lce_connection_index];
                ConsoleText = $"LCE Connection Status: {lce_connection_messages[lce_connection_index]}";
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

        private int comValue = 15;

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