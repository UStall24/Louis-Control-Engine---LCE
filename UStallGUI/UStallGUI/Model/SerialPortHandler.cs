using System;
using System.Collections.Generic;
using System.IO.Ports;
using System.Linq;
using System.Threading.Tasks;
using UStallGUI.Helpers;
using UStallGUI.ViewModel;

namespace UStallGUI.Model
{
    public class SerialPortHandler
    {
        public static SerialPortHandler Instance;
        public SerialPort serialPort;
        private const int baudRate = 115200;
        public bool IsOpen { get => serialPort.IsOpen; }

        // Variables used for Message Buffering
        private List<byte> bytesBuffer = new List<byte>();

        private List<byte[]> messageBuffer = new List<byte[]>();

        public SerialPortHandler(int comValue)
        {
            // Initialize the serial port
            serialPort = new SerialPort($"COM{comValue}", baudRate);
            Instance = this;
        }

        ~SerialPortHandler() => Instance = null;

        public bool Open()
        {
            bool successful = false;
            if (!serialPort.IsOpen)
            {
                try
                {
                    serialPort.Open(); // Open the serial port
                    serialPort.DataReceived += SerialPort_DataReceived;
                    successful = true;
                }
                catch (Exception)
                {
                }
            }
            return successful;
        }

        public bool Close()
        {
            bool successful = false;
            if (serialPort.IsOpen)
            {
                try
                {
                    serialPort.DataReceived -= SerialPort_DataReceived;
                    serialPort.Close(); // Close the serial port
                    successful = true;
                }
                catch (Exception) { }
            }
            return successful;
        }

        public void WriteBytes(LCE_CommandAddresses addressByte, byte[] data = null) => WriteBytes((byte)addressByte, data);

        public void WriteBytes(byte addressByte, byte[] data = null)
        {
            data ??= new byte[] { };

            if (serialPort.IsOpen)
            {
                byte[] dataToSend = new byte[data.Length + 1];
                dataToSend[0] = addressByte;
                Array.Copy(data, 0, dataToSend, 1, data.Length);
                serialPort.Write(dataToSend, 0, dataToSend.Length);
            }
            else
            {
                MainWindowViewModel.Instance.ConsoleText = "Serial Port is not open. Can't write.";
            }
        }

        public byte[] ReadBytes()
        {
            if (serialPort.IsOpen)
            {
                int bytesToRead = serialPort.BytesToRead;
                byte[] buffer = new byte[bytesToRead];
                serialPort.Read(buffer, 0, bytesToRead);
                return buffer;
            }
            return new byte[0];
        }

        private void SerialPort_DataReceived(object sender, SerialDataReceivedEventArgs e)
        {
            byte[] message = ReadBytes();
            Console.WriteLine($"Received message length: {message.Length}");

            // Add the new bytes to the buffer
            bytesBuffer.AddRange(message);

            // Process the message once the buffer has at least 7 bytes
            while (bytesBuffer.Count >= 7)
            {
                // Extract the first 7 bytes
                byte[] fullMessage = bytesBuffer.Take(7).ToArray();

                // Remove the processed bytes from the buffer
                bytesBuffer.RemoveRange(0, 7);

                messageBuffer.Add(fullMessage);
            }

            // If there are remaining bytes in the buffer that are less than 7, they will be retained
        }

        public byte[] LookForMessage(LCE_ResponseAddresses addressByte) => LookForMessage((byte)addressByte);

        public byte[] LookForMessage(byte addressByte)
        {
            byte[] response = [];
            for (int i = 0; i < messageBuffer.Count; i++)
            {
                if (messageBuffer[i][0] == addressByte)
                {
                    response = new byte[6];
                    Array.Copy(messageBuffer[i], 1, response, 0, 6);
                    messageBuffer.RemoveAt(i);
                    break;
                }
            }
            return response;
        }
    }
}