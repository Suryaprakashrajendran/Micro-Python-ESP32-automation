import network
import socket
from machine import Pin
import time

# LED on GPIO2 output
led = Pin(2, Pin.OUT)
led.value(1)  # Off initially

# Wi-Fi credentials
ssid = '**************'
password = '**************'

# Secret key for access
SECRET_KEY = "************"

# Energy tracking variables
led_on_time = 0        # total ON time in seconds
last_on_timestamp = 0  # when LED was last turned on
VOLTAGE = 3.3          # ESP32 GPIO supply voltage
CURRENT_A = 0.020      # 20mA LED current assumption
POWER_WATT = VOLTAGE * CURRENT_A  # = 0.066 W

# Connect to Wi-Fi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

print("Connecting to Wi-Fi...")
while not wlan.isconnected():
    time.sleep(1)

ip = wlan.ifconfig()[0]
print("Connected! ESP32 IP:", ip)

# Start HTTP server on port 80
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)

print("Listening on:", ip)

def update_led_on_time():
    """Update total ON time if LED is currently ON."""
    global led_on_time, last_on_timestamp
    if led.value() == 0:  # ON (inverted logic)
        led_on_time += time.time() - last_on_timestamp
        last_on_timestamp = time.time()

while True:
    cl, addr = s.accept()
    print("Client connected from", addr)

    request = cl.recv(1024).decode()
    print("Request:", request)

    # Build HTTP response header
    response = "HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\n"

    if f"key={SECRET_KEY}" not in request:
        cl.send(response + "Unauthorized. Provide ?key=SECRET")
        cl.close()
        continue

    if "/on" in request:
        if led.value() == 1:  # If OFF, switch ON and mark timestamp
            last_on_timestamp = time.time()
        led.value(0)
        cl.send(response + "Light turned ON")

    elif "/off" in request:
        if led.value() == 0:  # If ON, update ON time before turning OFF
            update_led_on_time()
        led.value(1)
        cl.send(response + "Light turned OFF")

    elif "/status" in request:
        status = "on" if led.value() == 0 else "off"
        cl.send(response + f"Light is {status}")

    elif "/blink" in request:
        for _ in range(5):
            if led.value() == 1:  # If currently OFF, mark ON timestamp
                last_on_timestamp = time.time()
            led.value(0)
            time.sleep(0.3)
            update_led_on_time()
            led.value(1)
            time.sleep(0.3)
        cl.send(response + "Light blinked 5 times")

    elif "/energy" in request:
        # Update ON time if LED is still ON
        if led.value() == 0:
            update_led_on_time()

        # Calculate energy (Wh)
        hours_on = led_on_time / 3600.0
        energy_used = hours_on * POWER_WATT  # in watt-hours

        cl.send(response +
                f"Light ON for {hours_on:.2f} hours\n"
                f"Voltage: {VOLTAGE:.2f} V\n"
                f"Current: {CURRENT_A*1000:.0f} mA\n"
                f"Power: {POWER_WATT:.3f} W\n"
                f"Energy used: {energy_used:.4f} Wh")
    else:
        cl.send(response + "Invalid request")
    cl.close()
