# Serial Device Reader with Configurable Settings

## Overview
This project connects to a serial device, reads sensor data, and alerts when a threshold is exceeded. All settings are stored in a configuration file (`config.json`) so you can adjust them without editing the code.

## File Structure
project-root/
│
├── config.json # Adjustable settings
├── main.py # Main Python script
└── README.md # Project documentation

## Usage
1. Install dependencies:
pip install pyserial
2. Edit `config.json` to set your desired port, baud rate, timeout, and sensor threshold.
3. Run:

## Example `config.json`
```json
{
 "port_name": "COM3",
 "baud_rate": 9600,
 "timeout": 2,
 "sensor_threshold": 50
}

---

✅ This change is **meaningful** because:
- It **removes hard-coded values** (good coding practice).
- Makes the project **flexible for different users/hardware**.
- Still small enough for a **clear, single commit**.

---

If you want, I can also give you the **exact commit message and PR description** so it’s contribution-ready.  
Do you want me to do that next?
