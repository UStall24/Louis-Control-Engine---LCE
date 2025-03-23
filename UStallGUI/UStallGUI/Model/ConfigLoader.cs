using Newtonsoft.Json;
using System;
using System.IO;

namespace UStallGUI.Model
{
    public class ConfigLoader
    {
        public readonly static string currentControllerParametersFilepath = "directionValues.json";

        public static DirectionValues LoadControllerParameters(string path)
        {
            //EnsureConfigFileExists();
            DirectionValues loadedValues = null;
            try
            {
                var json = File.ReadAllText(path);
                var config = JsonConvert.DeserializeObject<DirectionValues>(json);
                loadedValues = config;
            }
            catch (Exception) { }
            return loadedValues;
        }

        public static bool UpdateConfigurationFile(DirectionValues newConfig, string path)
        {
            bool successful = false;
            try
            {
                string json = JsonConvert.SerializeObject(newConfig, Formatting.Indented);
                File.WriteAllText(path, json);
                successful = true;
            }
            catch (Exception) { }
            return successful;
        }

        public static bool EnsureConfigFileExists()
        {
            if (!File.Exists(currentControllerParametersFilepath))
            {
                var defaultConfig = DirectionValues.GetDefaultDirectionValues(); // assuming this is the default constructor
                string json = JsonConvert.SerializeObject(defaultConfig, Formatting.Indented);
                File.WriteAllText(currentControllerParametersFilepath, json);
                return false; // file was created
            }
            return true; // file already existed
        }
    }
}