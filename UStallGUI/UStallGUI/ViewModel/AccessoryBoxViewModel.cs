using System;
using System.Windows.Input;
using GalaSoft.MvvmLight;
using GalaSoft.MvvmLight.Command;
using UStallGUI.Helpers;
using UStallGUI.Model;

namespace UStallGUI.ViewModel
{
    public class AccessoryBoxViewModel : ObservableObject
    {
        public GripperModel GripperModel { get; set; } = new();

        private int _mqtt_port;
        public int MqttPort
        {
            get
            {
                _mqtt_port = ConfigLoader.CurrentConfig.MqttPort;
                return _mqtt_port;
            }
            set
            {
                Set(ref _mqtt_port, value);
                ConfigLoader.CurrentConfig.MqttPort = _mqtt_port;
                ConfigLoader.UpdateConfigGUI();
            }
        }
        private string _mqtt_ip_addr;
        public string MqttIpAddr
        {
            get
            {
                _mqtt_ip_addr = ConfigLoader.CurrentConfig.MqttIpAddr;
                return _mqtt_ip_addr;
            }
            set
            {
                Set(ref _mqtt_ip_addr, value);
                ConfigLoader.CurrentConfig.MqttIpAddr = _mqtt_ip_addr;
                ConfigLoader.UpdateConfigGUI();
            }
        }

        MqttGripperSender _mqttSender;
        public AccessoryBoxViewModel()
        {
            GripperCommand = new RelayCommand<GripperAssignment>(ExecuteGripperCommand);
            ConnectMqtt_Command = new RelayCommand(ConnectMqtt);
        }

        public RelayCommand<GripperAssignment> GripperCommand { get; set; }
        private void ExecuteGripperCommand(GripperAssignment assignment)
        {
            if (_mqttSender != null && _mqttSender.IsConnected)
            {
                switch (assignment)
                {
                    case GripperAssignment.Gripper1_Servo1Plus:
                        GripperModel.A1M1 += 10;
                        break;
                    case GripperAssignment.Gripper1_Servo1Minus:
                        GripperModel.A1M1 -= 10;
                        break;
                    case GripperAssignment.Gripper1_Servo2Plus:
                        GripperModel.A1M2 += 10;
                        break;
                    case GripperAssignment.Gripper1_Servo2Minus:
                        GripperModel.A1M2 -= 10;
                        break;
                    case GripperAssignment.Gripper2_Servo1Plus:
                        GripperModel.A2M1 += 10;
                        break;
                    case GripperAssignment.Gripper2_Servo1Minus:
                        GripperModel.A2M1 -= 10;
                        break;
                    case GripperAssignment.Gripper2_Servo2Plus:
                        GripperModel.A2M2 += 10;
                        break;
                    case GripperAssignment.Gripper2_Servo2Minus:
                        GripperModel.A2M2 -= 10;
                        break;
                }
                 _ = _mqttSender.SendGripperValues();

            }
            else MainWindowViewModel.Instance.AccessoryBoxConsoleText = "Connect to Accessory Box first";
        }


        public RelayCommand ConnectMqtt_Command { get; set; }

        private async void ConnectMqtt()
        {
            if (ControllerHandlerViewModel.Instance.CurrentControllerModel != null)
            {
                MainWindowViewModel.Instance.AccessoryBoxConsoleText = "Trying to connect";

                _mqttSender = new MqttGripperSender(
                brokerAddress: "192.168.0.3",
                port: 1883,
                topic: "greifer/values",
                gripperModel: GripperModel
                );

                bool connected = await _mqttSender.StartAsync();
                if( connected )
                {
                    MainWindowViewModel.Instance.AccessoryBoxConsoleText = "Connected to Accessory Box RPi";
                    AssignControllerToGripperAction();
                }
                else MainWindowViewModel.Instance.AccessoryBoxConsoleText= "Connection to Accessory Box failed";
            }
            else MainWindowViewModel.Instance.AccessoryBoxConsoleText = "Connect Controller First";

        }
        int _selectedGripper = 0;
        public int SelectedGripper { get => _selectedGripper; set => Set(ref _selectedGripper, value); }
        private void AssignControllerToGripperAction()
        {
            ControllerHandlerViewModel.Instance.CurrentControllerModel.ButtonAPressed += () =>
            {
                SelectedGripper += 1;
                if (SelectedGripper > 2) SelectedGripper = 0;
            };

            ControllerHandlerViewModel.Instance.CurrentControllerModel.DPadUpPressed += () =>
            {
                if (SelectedGripper == 1) ExecuteGripperCommand(GripperAssignment.Gripper1_Servo1Plus);
                if (SelectedGripper == 2) ExecuteGripperCommand(GripperAssignment.Gripper2_Servo1Plus);
            };
            ControllerHandlerViewModel.Instance.CurrentControllerModel.DPadDownPressed += () =>
            {
                if (SelectedGripper == 1) ExecuteGripperCommand(GripperAssignment.Gripper1_Servo1Minus);
                if (SelectedGripper == 2) ExecuteGripperCommand(GripperAssignment.Gripper2_Servo1Minus);
            };
            ControllerHandlerViewModel.Instance.CurrentControllerModel.DPadRightPressed += () =>
            {
                if (SelectedGripper == 1) ExecuteGripperCommand(GripperAssignment.Gripper1_Servo2Plus);
                if (SelectedGripper == 2) ExecuteGripperCommand(GripperAssignment.Gripper2_Servo2Plus);
            };
            ControllerHandlerViewModel.Instance.CurrentControllerModel.DPadLeftPressed += () =>
            {
                if (SelectedGripper == 1) ExecuteGripperCommand(GripperAssignment.Gripper1_Servo2Minus);
                if (SelectedGripper == 2) ExecuteGripperCommand(GripperAssignment.Gripper2_Servo2Minus);
            };
        }

    }

    public enum GripperAssignment
    {
        Gripper1_Servo1Plus,
        Gripper1_Servo1Minus,
        Gripper1_Servo2Plus,
        Gripper1_Servo2Minus,
        Gripper2_Servo1Plus,
        Gripper2_Servo1Minus,
        Gripper2_Servo2Plus,
        Gripper2_Servo2Minus
    }
}
