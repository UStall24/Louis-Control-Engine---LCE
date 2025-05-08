using Greifer_GUI.Model;
using MQTTnet;
using MQTTnet.Client;
using MQTTnet.Protocol;
using System;
using System.Text;
using System.Text.Json;
using System.Threading;
using System.Threading.Tasks;
using UStallGUI.Model;

namespace UStallGUI.Helpers
{
    public class MqttGripperSender
    {
        private readonly IMqttClient _mqttClient;
        private readonly MqttClientOptions _mqttOptions;
        private readonly GripperModel _gripperModel;
        private readonly ControllerModel _controllerModel;
        private readonly string _topic;
        private Timer _sendTimer;

        public MqttGripperSender(string brokerAddress, int port, string topic, GripperModel gripperModel, ControllerModel controllerModel)
        {
            _gripperModel = gripperModel;
            _controllerModel = controllerModel;
            _topic = topic;

            var factory = new MqttFactory();
            _mqttClient = factory.CreateMqttClient();

            _mqttOptions = new MqttClientOptionsBuilder()
                .WithClientId("GripperSenderClient")
                .WithTcpServer(brokerAddress, port)
                .WithCleanSession()
                .Build();
        }

        public async Task StartAsync(int sendIntervalMs = 500)
        {
            if (!_mqttClient.IsConnected)
            {
                await _mqttClient.ConnectAsync(_mqttOptions);
            }

            _sendTimer = new Timer(SendGripperValues, null, 0, sendIntervalMs);
        }

        private async void SendGripperValues(object state)
        {
            if (!_mqttClient.IsConnected)
                return;

            byte[] gripperBytes = _gripperModel.GetGripperBytes(_controllerModel);

            var payload = new
            {
                Timestamp = DateTime.UtcNow,
                GripperValues = gripperBytes
            };

            string jsonPayload = JsonSerializer.Serialize(payload);

            var message = new MqttApplicationMessageBuilder()
                .WithTopic(_topic)
                .WithPayload(jsonPayload)
                .WithQualityOfServiceLevel(MqttQualityOfServiceLevel.AtLeastOnce)
                .WithRetainFlag(false)
                .Build();

            await _mqttClient.PublishAsync(message);
        }

        public async Task StopAsync()
        {
            _sendTimer?.Change(Timeout.Infinite, 0);
            _sendTimer?.Dispose();
            await _mqttClient.DisconnectAsync();
        }
    }
}
