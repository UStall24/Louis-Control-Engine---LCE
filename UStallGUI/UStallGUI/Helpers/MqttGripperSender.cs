using System;
using System.Text.Json;
using System.Threading;
using System.Threading.Tasks;
using MQTTnet;
using MQTTnet.Client;
using MQTTnet.Protocol;
using UStallGUI.Model;

namespace UStallGUI.Helpers
{
    public class MqttGripperSender
    {
        private readonly IMqttClient _mqttClient;
        private readonly MqttClientOptions _mqttOptions;
        private readonly GripperModel _gripperModel;
        private readonly string _topic;
        public bool IsConnected { get => _mqttClient?.IsConnected == true;}

        public MqttGripperSender(string brokerAddress, int port, string topic, GripperModel gripperModel)
        {
            _gripperModel = gripperModel;
            _topic = topic;

            var factory = new MqttFactory();
            _mqttClient = factory.CreateMqttClient();

            _mqttOptions = new MqttClientOptionsBuilder()
                .WithClientId("GripperSenderClient")
                .WithTcpServer(brokerAddress, port)
                .WithCleanSession()
                .Build();
        }

        public async Task<bool> StartAsync()
        {
            try
            {
                if (!_mqttClient.IsConnected)
                {
                    await _mqttClient.ConnectAsync(_mqttOptions);
                }
                return _mqttClient.IsConnected;
            }
            catch(Exception)
            {
                return false;
            }
        }

        public async Task SendGripperValues()
        {
            if (!_mqttClient.IsConnected)
                return;

            byte[] gripperBytes = _gripperModel.GetGripperBytes();

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
    }
}
