import requests
import sys
import json

def get_status(url, key):
    try:
        response = requests.get(f"{url}/status?key={key}", timeout=10)
        status = response.text.strip().lower()
        return status
    except Exception as e:
        print("Failed to get status:", e)
        return None

def send_command(command, url, key):
    if command == "status":
        status = get_status(url, key)
        if status is not None:
            print(f"Current light status: {status.upper()}")
        else:
            print("Could not determine current light status.")
        return

    if command == "blink":
        try:
            response = requests.get(f"{url}/blink?key={key}", timeout=10)
            print("Blink command sent successfully!")
            print("ESP32 response:", response.text.strip())
        except Exception as e:
            print("Error sending blink command:", e)
        return

    if command == "energy":
        try:
            response = requests.get(f"{url}/energy?key={key}", timeout=10)
            data = response.text.strip()
            print("Energy usage report")
            print("-------------------------")

            energy_data = {}
            for line in data.splitlines():
                if line.startswith("Light ON for"):
                    hours = float(line.split(" ")[3])
                    minutes = round(hours * 60, 2)
                    human_readable = f"Light ON for {minutes} minutes ({hours:.2f} hours)"
                    print(human_readable)
                    energy_data["Light_ON"] = {
                        "hours": hours,
                        "minutes": minutes,
                        "human_readable": human_readable
                    }

                elif line.startswith("Voltage:"):
                    voltage = float(line.split()[1])
                    print(f"Voltage: {voltage:.2f} V")
                    energy_data["Voltage"] = voltage

                elif line.startswith("Current:"):
                    current = float(line.split()[1])
                    print(f"Current: {current} mA")
                    energy_data["Current_mA"] = current

                elif line.startswith("Power:"):
                    power = float(line.split()[1])
                    print(f"Power: {power:.3f} W")
                    energy_data["Power_W"] = power

                elif line.startswith("Energy used:"):
                    energy = float(line.split()[2])
                    print(f"Energy used: {energy:.4f} Wh")
                    energy_data["Energy_Wh"] = energy

            print("-------------------------")

            # JSON output
            print(json.dumps(energy_data, indent=4))

        except Exception as e:
            print("Error fetching energy data:", e)
        return

    # Handle ON / OFF
    current_status = get_status(url, key)
    if current_status is None:
        print("Could not determine current light status.")
        return

    if current_status == command:
        print(f"Light is already {command.upper()}")
        return

    try:
        response = requests.get(f"{url}/{command}?key={key}", timeout=5)
        print(f"Light turned {command.upper()} successfully!")
        print("ESP32 response:", response.text.strip())
    except Exception as e:
        print("Error sending command:", e)

#main
if len(sys.argv) < 4:
    print("Usage: python control_light_cli.py on|off|status|blink|energy <ESP32_URL> <SECRET_KEY>")
    sys.exit(1)

command = sys.argv[1].strip().lower()
ESP32_URL = sys.argv[2].strip()
SECRET_KEY = sys.argv[3].strip()

if command in ["on", "off", "status", "blink", "energy"]:
    send_command(command, ESP32_URL, SECRET_KEY)
else:
    print("Invalid command. Use 'on', 'off', 'status', 'blink', or 'energy'.")

