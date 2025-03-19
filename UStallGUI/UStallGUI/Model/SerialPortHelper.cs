using System;
using System.IO.Ports;
using System.Text;

namespace UStallGUI.Model
{
    public class SerialPortHelper
    {
        public SerialPort serialPort;
        private const int baudRate = 115200;
        private readonly int maxMessagesPerSecond = 10;
        private int lastMessageTimestamp;

        public SerialPortHelper(int comValue)
        {
            // Initialize the serial port
            serialPort = new SerialPort($"COM{comValue}", baudRate);
        }

        public bool IsOpen { get => serialPort.IsOpen; }

        public bool Open()
        {
            bool successful = false;
            if (!serialPort.IsOpen)
            {
                try
                {
                    serialPort.Open(); // Open the serial port
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
                    serialPort.Close(); // Close the serial port
                    successful = true;
                }
                catch (Exception) { }
            }
            return successful;
        }

        public void WriteBytes(byte adressByte, byte[] data)
        {
            // Get the current timestamp
            int currentTimestamp = Environment.TickCount;

            // Calculate the time elapsed since the last message
            int timeElapsed = currentTimestamp - lastMessageTimestamp;

            // Check if the rate limit is exceeded
            if (timeElapsed < 1000 / maxMessagesPerSecond)
            {
                return;
            }

            // Update the last message timestamp
            lastMessageTimestamp = currentTimestamp;

            byte[] dataToSend = new byte[data.Length + 1];
            dataToSend[0] = adressByte;
            Array.Copy(data, 0, dataToSend, 1, data.Length);

            // Write the data to the serial port
            serialPort.Write(dataToSend, 0, dataToSend.Length);
        }

        public byte[] ReadBytes(int count)
        {
            if (!serialPort.IsOpen)
            {
                throw new InvalidOperationException("Serial port is not open.");
            }

            byte[] buffer = new byte[count];
            int bytesRead = 0;

            // Read bytes from the serial port
            while (bytesRead < count)
            {
                bytesRead += serialPort.Read(buffer, bytesRead, count - bytesRead);
            }

            return buffer;
        }

        public string ReadBytesString()
        {
            if (serialPort.IsOpen)
            {
                int bytesToRead = serialPort.BytesToRead;
                byte[] buffer = new byte[bytesToRead];
                serialPort.Read(buffer, 0, bytesToRead);
                return Encoding.ASCII.GetString(buffer);
            }
            return "";
        }
    }
}