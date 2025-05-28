using GalaSoft.MvvmLight;
using GalaSoft.MvvmLight.Command;
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

        private string connectedControllersText = "None";

        public ControllerHandlerViewModel()
        {
            ScanForControllers = new RelayCommand(ScanConnectedControllers); // Default to controller index 0
            ConnectToController = new RelayCommand(() => SetController(0)); // Default to controller index 0
        }

        private void ScanConnectedControllers()
        {
            List<string> connectedControllers = new List<string>();

            for (int i = 0; i < 4; i++)
            {
                var controller = new Controller((UserIndex)i);
                if (controller.IsConnected)
                {
                    // Get the controller's capabilities to determine its type
                    var capabilities = controller.GetCapabilities(DeviceQueryType.Gamepad);
                    string controllerType = capabilities.SubType.ToString(); // e.g., Gamepad, Wheel, etc.

                    connectedControllers.Add($"Controller {i + 1} ({controllerType})");
                }
            }

            if (connectedControllers.Count > 0) ConnectedControllers = string.Join(", ", connectedControllers);
            else ConnectedControllers = "None";

            MainWindowViewModel.Instance.ConsoleText = "Scanning connected Controllers complete";
        }

        private void SetController(int index)
        {
            Controller controller = new Controller((UserIndex)index);
            CurrentControllerModel = new ControllerModel(controller);

            // Run the polling task in the background
            _ = Task.Run(ControllerTimerCallback);

            MainWindowViewModel.Instance.ConsoleText = "Controller with Index 0 is connected";
            MainWindowViewModel.Instance.ConnectionStatusController = "Connected";
        }

        private async Task ControllerTimerCallback()
        {
            keepPolling = true;
            int delayMs = (pollingFrequency > 0) ? (1000 / pollingFrequency) : 10; // Avoid division by zero
            int dividorCounter = 0;
            try
            {
                while (keepPolling)
                {
                    CurrentControllerModel.UpdateControllerValues();
                    if (dividorCounter == 0)
                    {
                        if (sendControllerValues) SerialPortHandler.Instance?.WriteBytes(LCE_CommandAddresses.ApplyControllerValues, CurrentControllerModel.GetMovementBytes());
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