import requests
import serial
import time

API_KEY = "ENTER YOUR API KEY"

# SERIAL PORT
ser = serial.Serial('COM7', 115200)
time.sleep(2)

# FUNCTION
def simplify(step):
    instruction = step['html_instructions'].lower()
    distance_text = step['distance']['text']

    if "left" in instruction:
        direction = "LEFT"
    elif "right" in instruction:
        direction = "RIGHT"
    else:
        direction = "STRAIGHT"
  if "km" in distance_text:
        distance = distance_text.replace(" km", "") + "km"
    elif "m" in distance_text:
        distance = distance_text.replace(" m", "") + "m"
    else:
        distance = "0"
  return f"{direction},{distance}"
# USER INPUT
origin = input("Enter starting location: ")
destination = input("Enter destination: ")

# API CALL
url = f"https://maps.googleapis.com/maps/api/directions/json?origin={origin}&destination={destination}&key={API_KEY}"

response = requests.get(url)
data = response.json()

# ERROR CHECK
if data['status'] != "OK":
    print("Error:", data['status'])
    exit()

steps = data['routes'][0]['legs'][0]['steps']

print("\nSending directions...\n")

for step in steps:
    msg = simplify(step)

    print(msg)

    ser.write((msg + "\n").encode())
    if "km" in msg:
        value = float(msg.split(',')[1].replace("km", ""))
    elif "m" in msg:
value = float(msg.split(',')[1].replace("m", "")) / 1000
    else:
        value = 0

    # FINAL FIX → minimum delay added
    delay = max(8, 6 + (value * 12))

    print(f"Delay: {round(delay,2)} sec")

    time.sleep(delay)

print("\nDone")
