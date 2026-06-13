import serial
import webbrowser
import urllib.parse
import pyautogui
import time

ser = serial.Serial('COM7', 115200)
time.sleep(2)
while True:
    data = ser.readline().decode(errors='ignore').strip()
    if data.startswith("ACCIDENT"):
        coord = data.split(":")[1]
        msg = f" Accident detected!\nLocation:\nhttps://maps.google.com/?q={coord}"
        encoded_msg = urllib.parse.quote(msg)
        number = "91XXXXXXXXXX" 
        url = f"https://web.whatsapp.com/send?phone={number}&text={encoded_msg}"
        print("Opening WhatsApp...")

        webbrowser.open(url)

        # wait for page load
        time.sleep(10)

        # press enter to send
        pyautogui.press("enter")

        print("Message sent!")

        break
