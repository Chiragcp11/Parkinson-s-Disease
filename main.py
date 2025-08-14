import json
import serial  # pip install pyserial
import time

def load_config(config_path="config.json"):
    """Load settings from a configuration file."""
    try:
        with open(config_path, "r") as f:
            config = json.load(f)
        print("[INFO] Configuration loaded successfully.")
        return config
    except FileNotFoundError:
        print("[ERROR] Configuration file not found.")
        exit(1)
    except json.JSONDecodeError:
        print("[ERROR] Invalid JSON format in configuration file.")
        exit(1)

def connect_to_device(port, baud_rate, timeout):
    """Establish a serial connection to the device."""
    try:
        ser = serial.Serial(port=port, baudrate=baud_rate, timeout=timeout)
        print(f"[INFO] Connected to {port} at {baud_rate} baud.")
        return ser
    except serial.SerialException as e:
        print(f"[ERROR] Failed to connect: {e}")
        exit(1)

def read_sensor_data(serial_connection, threshold):
    """Read and process sensor data."""
    try:
        while True:
            if serial_connection.in_waiting > 0:
                data = serial_connection.readline().decode("utf-8").strip()
                if data.isdigit():
                    value = int(data)
                    print(f"[DATA] Sensor value: {value}")
                    if value > threshold:
                        print("[ALERT] Sensor threshold exceeded!")
                else:
                    print(f"[WARN] Invalid data: {data}")
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("\n[INFO] Stopping data reading.")
    finally:
        serial_connection.close()

if __name__ == "__main__":
    # Load configuration
    config = load_config()

    # Connect to device
    serial_conn = connect_to_device(
        port=config["port_name"],
        baud_rate=config["baud_rate"],
        timeout=config["timeout"]
    )

    # Start reading sensor data
    read_sensor_data(serial_conn, config["sensor_threshold"])