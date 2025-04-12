import json

def read_json_file(filepath):
    """Reads the JSON file and returns the parsed data."""
    with open(filepath, 'r') as file:
        return json.load(file)

def write_json_file(filepath, data):
    """Writes the data to a JSON file, overwriting if it exists."""
    with open(filepath, 'w') as file:
        json_string = json.dumps(data)
        file.write(json_string)
    
def get_direction_uart_values_payload(direction_values):
    key_order = ["Translation", "Rotation"]
    axis_order = ["Z_Axis", "X_Axis", "Y_Axis"]
    motor_order = ["VM1", "VM2", "VM3", "HM1", "HM2", "HM3"]

    # Flatten JSON values
    addresses = [0x11,0x12,0x13,0x14,0x15,0x16]
    
    values = []
    for category in key_order:
        for axis in axis_order:
            motor_values = []
            motor_values.append(addresses[0])
            addresses.pop(0)
            for motor in motor_order:
                motor_values.append((int((direction_values[category][axis][motor] + 1) * 127.5)))
            values.append(motor_values)
            
    return values

def update_direction_values(direction_values, direction_values_matrix):
    # Define the axes and directions for translation and rotation
    axis_order = ["Z_Axis", "X_Axis", "Y_Axis"]
    motor_order = ["VM1", "VM2", "VM3", "HM1", "HM2", "HM3"]

    # Loop through each axis and its corresponding values
    for i, axis in enumerate(axis_order):
        for j, direction in enumerate(motor_order):
            # Update the translation and rotation direction values
            direction_values["Translation"][axis][direction] = direction_values_matrix[i][j]
            # Assuming you want to update rotation as well
            direction_values["Rotation"][axis][direction] = direction_values_matrix[i+3][j]

    return direction_values

if __name__ == "__main__":
    test_data = {"key": "value"}
    write_json_file("test.json", test_data)
    print(read_json_file("test.json"))

    
