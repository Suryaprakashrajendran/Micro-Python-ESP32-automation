# ESP32 AI-Controlled Automation

This project demonstrates controlling an ESP32 using an AI agent or HTTP requests. The ESP32 can:

- Turn an LED on/off
- Blink the LED
- Check LED status
- Track energy consumption (voltage, current, power, energy)
- Integrate with AI agents for automation
- Work remotely via Ngrok tunnel

---

## Features

- LED control on GPIO2 (turn on/off, blink)
- Energy tracking (Wh calculation based on LED usage)
- Secure access with a secret key
- Remote control using HTTP requests
- AI agent integration for automation
- Optional Ngrok remote access

---

## Hardware Requirements

- ESP32 development board
- LED and 220Ω resistor (if using external LED)
- USB cable for programming and power

---

## Software Requirements

- MicroPython firmware installed on ESP32
- Python environment (for AI agent and Ngrok)
- Optional AI agent framework (e.g., Symphony AI, PyMaker)
- Ngrok (optional, for remote HTTP access)

---

## Setup Instructions

### 1. Flash ESP32 with MicroPython
Follow the official guide: [MicroPython ESP32 Firmware](https://micropython.org/download/esp32/)

### 2. Connect ESP32 to Wi-Fi
Edit the script with your Wi-Fi credentials:

```python
ssid = 'YOUR_WIFI_SSID'
password = 'YOUR_WIFI_PASSWORD'

