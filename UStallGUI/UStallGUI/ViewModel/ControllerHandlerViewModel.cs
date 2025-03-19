using GalaSoft.MvvmLight;
using GalaSoft.MvvmLight.Command;
using SharpDX.XInput;
using System;
using System.Collections.Generic;
using System.Threading;
using UStallGUI.Helpers;
using UStallGUI.Model;

namespace UStallGUI.ViewModel
{
    public class ControllerHandlerViewModel : ObservableObject
    {
        private Controller controller;
        private readonly int pollingIntervalsms = 10;
        private Timer controllerTimer;

        // Properties for binding
        public ControllerToPwmModel ControllerModel { get; set; }

        private string connectedControllersText = "None";

        public ControllerHandlerViewModel()
        {
            ControllerModel = new ControllerToPwmModel(ConfigLoader.LoadControllerParameters());
            ScanForControllers = new RelayCommand(ScanConnectedControllers); // Default to controller index 0
            ConnectToController = new RelayCommand(() => SetController(0)); // Default to controller index 0
        }

        private void ScanConnectedControllers()
        {
            List<string> connectedControllers = new List<string>();

            // Check all possible controller indices (0 to 3)
            for (int i = 0; i < 4; i++)
            {
                var controller = new Controller((UserIndex)i);
                if (controller.IsConnected)
                {
                    // Get the controller's capabilities to determine its type
                    var capabilities = controller.GetCapabilities(DeviceQueryType.Gamepad);
                    string controllerType = capabilities.SubType.ToString(); // e.g., Gamepad, Wheel, etc.

                    // Add the controller name with its index and type
                    connectedControllers.Add($"Controller {i + 1} ({controllerType})");
                }
            }

            // Update the ConnectedControllers property
            if (connectedControllers.Count > 0)
            {
                ConnectedControllers = string.Join(", ", connectedControllers); // Display connected controllers
            }
            else
            {
                ConnectedControllers = "None"; // No controllers connected
            }
            MainWindowViewModel.Instance.ConsoleText = "Scanning connected Controllers complete";
        }

        private void SetController(int index)
        {
            controller = new Controller((UserIndex)index);
            if (controllerTimer != null)
            {
                controllerTimer.Dispose();
            }
            controllerTimer = new Timer(ControllerTimerCallback, null, 1000, pollingIntervalsms);
            MainWindowViewModel.Instance.ConsoleText = "Controller with Index 0 is connected";
            MainWindowViewModel.Instance.ConnectionStatusController = "Connected";
        }

        private void ControllerTimerCallback(object state)
        {
            if (controller != null)
            {
                try
                {
                    State controllerState = controller.GetState();
                    ControllerModel.UpdateControllerValues(controllerState);
                    float[] motorValues = ControllerModel.CalculateMotorValues();
                    MainWindowViewModel.Instance.WriteToLCE(LCECommunicationHelper.ConvertMotorValuesToBytes(motorValues));
                    Console.WriteLine(new MotorValues(motorValues));
                }
                catch (Exception e)
                {
                    MainWindowViewModel.Instance.ConsoleText = "Controller disconnected";
                    MainWindowViewModel.Instance.ConnectionStatusController = "Not connected";
                    controller = null;
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