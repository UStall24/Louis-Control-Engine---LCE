using Newtonsoft.Json;
using System;
using System.IO;

namespace UStallGUI.Model
{
    public class ConfigLoader
    {
        private static string currentControllerParametersFilepath = "directionValues.json";

        public static DirectionValues LoadControllerParameters()
        {
            EnsureConfigFileExists();
            DirectionValues loadedValues = null;
            try
            {
                var json = File.ReadAllText(currentControllerParametersFilepath);
                var config = JsonConvert.DeserializeObject<DirectionValues>(json);
                loadedValues = config;
            }
            catch (Exception) { }
            return loadedValues;
        }

        public static void UpdateConfigurationFile(DirectionValues newConfig)
        {
            try
            {
                string json = JsonConvert.SerializeObject(newConfig, Formatting.Indented);
                File.WriteAllText(currentControllerParametersFilepath, json);
            }
            catch (Exception) { }
        }

        private static bool EnsureConfigFileExists()
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