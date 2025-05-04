using GalaSoft.MvvmLight;
using GalaSoft.MvvmLight.Command;
using System;
using System.Security.Cryptography;
using System.Threading.Tasks;
using System.Timers;
using UStallGUI.Helpers;
using UStallGUI.Model;

namespace UStallGUI.ViewModel
{
    public class SetupHandlerViewModel : ObservableObject
    {
        #region LCE Setup

        private int _comPort;

        public int ComPort
        {
            get
            {
                _comPort = currentConfig.ComPort;
                return _comPort;
            }
            set
            {
                Set(ref _comPort, value);
                currentConfig.ComPort = _comPort;
                UpdateConfig();
            }
        }

        private byte _updateInterval;

        public byte UpdateInterval // in ms
        {
            get => _updateInterval;
            set => Set(ref _updateInterval, value);
        }

        private int _controlType;

        public int ControlType
        {
            get => _controlType;
            set
            {
                Set(ref _controlType, value);
                ControllerHandlerViewModel.sendControllerValues = _controlType == 2;
            }
        }

        public RelayCommand ConnectToLCE_Command { get; set; }
        public RelayCommand InitThrusters_Command { get; set; }
        public RelayCommand DeinitThrusters_Command { get; set; }
        public RelayCommand ApplyUpdateInterval_Command { get; set; }
        public RelayCommand ResetErrorLCE_Command { get; set; }

        #endregion LCE Setup

        #region Manual Control

        private float _vm1;
        public float VM1
        {
            get => _vm1;
            set => Set(ref _vm1, value);
        }

        private float _vm2;
        public float VM2
        {
            get => _vm2;
            set => Set(ref _vm2, value);
        }

        private float _vm3;
        public float VM3
        {
            get => _vm3;
            set => Set(ref _vm3, value);
        }

        private float _hm1;
        public float HM1
        {
            get => _hm1;
            set => Set(ref _hm1, value);
        }

        private float _hm2;
        public float HM2
        {
            get => _hm2;
            set => Set(ref _hm2, value);
        }

        private float _hm3;
        public float HM3
        {
            get => _hm3;
            set => Set(ref _hm3, value);
        }

        private MotorValues _manualControlValues;

        public MotorValues ManualControlValues
        {
            get => _manualControlValues;
            set => Set(ref _manualControlValues, value);
        }

        private float _manualControlAllVertical;

        public float ManualControlAllVertical
        {
            get => _manualControlAllVertical;
            set
            {
                Set(ref _manualControlAllVertical, Math.Clamp(value, -1f, 1f));
                ManualControlValues.VM1 = value;
                ManualControlValues.VM2 = value;
                ManualControlValues.VM3 = value;
            }
        }

        private float _manualControlAllHorizontal;

        public float ManualControlAllHorizontal
        {
            get => _manualControlAllHorizontal;
            set
            {
                Set(ref _manualControlAllHorizontal, Math.Clamp(value, -1f, 1f));
                ManualControlValues.HM1 = value;
                ManualControlValues.HM2 = value;
                ManualControlValues.HM3 = value;
            }
        }

        private float _manualControlAll;

        public float ManualControlAll
        {
            get => _manualControlAll;
            set
            {
                Set(ref _manualControlAll, Math.Clamp(value, -1f, 1f));
                ManualControlAllVertical = value;
                ManualControlAllHorizontal = value;
            }
        }

        public RelayCommand ManualControlReset_Command { get; set; }

        #endregion Manual Control

        #region Gyro

        private bool _gyroEnabled;

        public bool GyroEnabled
        {
            get => _gyroEnabled;
            set
            {
                if (Set(ref _gyroEnabled, value))
                {
                    currentConfig.GyroEnabled = value;
                    UpdateConfig();
                }
            }
        }

        private float _gyroPValue;

        public float GyroPValue
        {
            get => _gyroPValue;
            set => Set(ref _gyroPValue, Clamp255Float(value));
        }

        private float _gyroDValue;

        public float GyroDValue
        {
            get => _gyroDValue;
            set => Set(ref _gyroDValue, Clamp255Float(value));
        }

        // Method to clamp the value between 0 and 2.55
        private static float Clamp255Float(float value)
        {
            if (value < 0)
                return 0;
            if (value > 2.55)
                return 2.55f;
            return value;
        }

        public RelayCommand PullGyroValues_Command { get; set; }
        public RelayCommand ApplyGyroValues_Command { get; set; }

        #endregion Gyro

        private ConfigGUI currentConfig;
        private SerialPortHandler sp;

        public SetupHandlerViewModel()
        {
            ManualControlValues = new MotorValues([0, 0, 0, 0, 0, 0]);
            ControlType = 2; // Default Controller
            currentConfig = ConfigLoader.LoadConfigGUI();

            ConnectToLCE_Command = new(ConnectToLCE);
            InitThrusters_Command = new(InitThrusters);
            DeinitThrusters_Command = new(DeinitThrusters);
            ApplyUpdateInterval_Command = new(ApplyUpdateInterval);
            ResetErrorLCE_Command = new(ResetErrorLCE);
            PullGyroValues_Command = new(PullGyroValues);
            ApplyGyroValues_Command = new(ApplyGyroValues);
            ManualControlReset_Command = new(ManualControlReset);
        }

        private void UpdateConfig() => ConfigLoader.UpdateConfigGUI(currentConfig);

        private async void ConnectToLCE()
        {
            DisconnectFromLCE();
            sp = new SerialPortHandler(ComPort);
            if (sp.Open())
            {
                MainWindowViewModel.Instance.UpdateConnectionStatusLCE(1);

                sp.WriteBytes(LCE_CommandAddresses.InitThrusters);
                await Task.Delay(100);
                byte[] response = sp.LookForMessage(LCE_ResponseAddresses.InitThrusters_Response);
                if (response.Length != 0)
                {
                    MainWindowViewModel.Instance.UpdateConnectionStatusLCE(2);
                    MainWindowViewModel.Instance.ConsoleText = LCECommunicationHelper.LCE_MessageAddresses[response[0]];
                    UpdateInterval = await PullUpdateInterval();
                }
                else
                {
                    MainWindowViewModel.Instance.UpdateConnectionStatusLCE(3);
                }
            }
            else
            {
                MainWindowViewModel.Instance.UpdateConnectionStatusLCE(3);
                await Task.Delay(3000);
                MainWindowViewModel.Instance.UpdateConnectionStatusLCE(0);
            }
        }

        public void DisconnectFromLCE()
        {
            if (sp != null && sp.IsOpen)
            {
                bool closingSuccessful = sp.Close();
                MainWindowViewModel.Instance.UpdateConnectionStatusLCE(closingSuccessful ? 4 : 5);
            }
            else
            {
                MainWindowViewModel.Instance.ConsoleText = "Serialport is currently closed";
            }
        }

        private async void InitThrusters()
        {
        }

        private async void DeinitThrusters()
        {
        }

        //private void InitManualControl()
        //{
        //    _manualControlTimer = new Timer(UpdateInterval * 2); // interval in milliseconds (e.g., 1000ms = 1s)
        //    _manualControlTimer.Elapsed += ApplyManualControl;
        //    _manualControlTimer.AutoReset = true; // repeat every interval
        //    _manualControlTimer.Enabled = true;
        //}

        private void ApplyManualControl(object sender, ElapsedEventArgs e)
        {
            sp.WriteBytes(LCE_CommandAddresses.ApplyManualControl, ManualControlValues.GetAsByte());
        }

        private async void ApplyUpdateInterval()
        {
            byte oldCycleInterval = await PullUpdateInterval();
            if (oldCycleInterval != 0)
            {
                sp.WriteBytes(LCE_CommandAddresses.UpdateCylceTime, [UpdateInterval]);
                await Task.Delay(100);
                byte[] response = sp.LookForMessage(LCE_ResponseAddresses.UpdateCycleTime_Response);
                if (response.Length > 0) MainWindowViewModel.Instance.ConsoleText = $"Updating Cycle Time from {oldCycleInterval} to {response[0]} {(oldCycleInterval == response[0] ? "Failed!" : "was Successful!")}";
            }
        }

        private async Task<Byte> PullUpdateInterval()
        {
            byte val = 0x00;
            if (sp != null)
            {
                sp.WriteBytes(LCE_CommandAddresses.UpdateCylceTime, [0x00]);
                await Task.Delay(100);
                byte[] response = sp.LookForMessage(LCE_ResponseAddresses.UpdateCycleTime_Response);
                if (response.Length > 0)
                {
                    val = response[0];
                }
            }
            return val;
        }

        private async void ResetErrorLCE()
        {
            if (sp != null)
            {
                sp.WriteBytes(LCE_CommandAddresses.ResetError);
                await Task.Delay(100);
                byte[] response = sp.LookForMessage(LCE_ResponseAddresses.ResetError_Response);
                if (response.Length != 0 && response[0] == 0x01) MainWindowViewModel.Instance.ConsoleText = "Resetting Error was successful";
            }
        }

        private async void PullGyroValues()
        {
            if (sp != null)
            {
                sp.WriteBytes(LCE_CommandAddresses.PullPidValues);
                await Task.Delay(100);
                byte[] response = sp.LookForMessage(LCE_ResponseAddresses.PullPidValues_Response);
                if (response.Length > 0)
                {
                    GyroPValue = LCECommunicationHelper.ConvertByteTo255Float(response[0]);
                    GyroDValue = LCECommunicationHelper.ConvertByteTo255Float(response[1]);
                    GyroEnabled = (response[2] == 1);
                    MainWindowViewModel.Instance.ConsoleText = "Pulling PID values was Successful!";
                }
                else MainWindowViewModel.Instance.ConsoleText = "Pulling PID values failed!";
            }
        }

        private async void ApplyGyroValues()
        {
            if (sp != null)
            {
                byte[] payload = [LCECommunicationHelper.Convert255FloatToByte(GyroPValue), LCECommunicationHelper.Convert255FloatToByte(GyroDValue), (byte)(GyroEnabled ? 0x01 : 0x00)];

                sp.WriteBytes(LCE_CommandAddresses.ApplyPidValues, payload);
                await Task.Delay(100);
                byte[] response = sp.LookForMessage(LCE_ResponseAddresses.ApplyPidValues_Response);
                if (response.Length > 0) MainWindowViewModel.Instance.ConsoleText = "Applying PID values was Successful!";
                else MainWindowViewModel.Instance.ConsoleText = "Applying PID values failed!";
            }
        }

        private void ManualControlReset() => ManualControlValues.UpdateAsArray([0, 0, 0, 0, 0, 0]);
    }
}