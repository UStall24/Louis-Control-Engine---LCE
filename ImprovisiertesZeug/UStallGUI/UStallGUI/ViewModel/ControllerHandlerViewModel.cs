using GalaSoft.MvvmLight;
using GalaSoft.MvvmLight.Command;
using Greifer_GUI.Model;
using SharpDX.XInput;
using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using UStallGUI.Helpers;
using UStallGUI.Model;

namespace UStallGUI.ViewModel
{
    public class ControllerHandlerViewModel : ObservableObject
    {
        public static bool sendControllerValues = false;

        private readonly int pollingFrequency = 200;
        private readonly int sendingDividor = 10;
        private bool keepPolling = false;

        // Properties for binding
        public ControllerModel CurrentControllerModel { get; set; }
        public GripperModel CurrentGripperModel { get; set; }

        private string connectedControllersText = "None";

        // MQTT sender instance
        private MqttGripperSender _mqttSender;

        public ControllerHandlerViewModel()
        {
            CurrentGripperModel = new GripperModel();
            ScanForControllers = new RelayCommand(ScanConnectedControllers); // Default to controller index 0
            ConnectToController = new RelayCommand(async () => await SetControllerAsync(0)); // Default to controller index 0
        }

        private void ScanConnectedControllers()
        {
            List<string> connectedControllers = new List<string>();

            for (int i = 0; i < 4; i++)
            {
                var controller = new Controller((UserIndex)i);
                if (controller.IsConnected)
                {
                    var capabilities = controller.GetCapabilities(DeviceQueryType.Gamepad);
                    string controllerType = capabilities.SubType.ToString();
                    connectedControllers.Add($"Controller {i + 1} ({controllerType})");
                }
            }

            ConnectedControllers = connectedControllers.Count > 0 ? string.Join(", ", connectedControllers) : "None";
            MainWindowViewModel.Instance.ConsoleText = "Scanning connected Controllers complete";
        }

        private async Task SetControllerAsync(int index)
        {
            Controller controller = new Controller((UserIndex)index);
            CurrentControllerModel = new ControllerModel(controller);

            // MQTT initialisieren
            _mqttSender = new MqttGripperSender(
                brokerAddress: "192.168.0.3",
                port: 1883,
                topic: "greifer/values",
                gripperModel: CurrentGripperModel,
                controllerModel: CurrentControllerModel
            );

            await _mqttSender.StartAsync();

            _ = Task.Run(ControllerTimerCallback);

            MainWindowViewModel.Instance.ConsoleText = "Controller with Index 0 is connected";
            MainWindowViewModel.Instance.ConnectionStatusController = "Connected";
        }

        private async Task ControllerTimerCallback()
        {
            keepPolling = true;
            int delayMs = (pollingFrequency > 0) ? (1000 / pollingFrequency) : 10;
            int dividorCounter = 0;
            try
            {
                while (keepPolling)
                {
                    CurrentControllerModel.UpdateControllerValues();

                    if (dividorCounter == 0)
                    {
                        if (sendControllerValues)
                        {
                            SerialPortHandler.Instance?.WriteBytes(
                                LCE_CommandAddresses.ApplyControllerValues,
                                CurrentControllerModel.GetMovementBytes()
                            );
                        }

                        Console.WriteLine($"{sendControllerValues}: {CurrentControllerModel.GetMovementBytesAsString()}");

                        dividorCounter = sendingDividor;
                    }
                    else dividorCounter--;

                    RaisePropertyChanged(nameof(CurrentControllerModel));
                    await Task.Delay(delayMs);
                }
            }
            catch (Exception ex)
            {
                MainWindowViewModel.Instance.ConsoleText = $"Controller Exception: {ex}";
                keepPolling = false;
                if (_mqttSender != null)
                {
                    await _mqttSender.StopAsync();
                }
            }
        }

        public string ConnectedControllers
        {
            get => connectedControllersText;
            private set => Set(ref connectedControllersText, value);
        }

        public RelayCommand ConnectToController { get; set; }
        public RelayCommand ScanForControllers { get; set; }
    }
}
