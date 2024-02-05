import subprocess
import os
import time
import ScriptsCall as SC
from ScriptsCall import CoordinatesManager
import json
import random
import math
from PIL import Image, ImageTk
import tkinter as tk
import pytesseract as tes

def execute_adb_command(command):
    subprocess.run(command, shell=True)

def move_cursor(x, y):
    # Эмуляция абсолютного события для перемещения курсора
    execute_adb_command(f"adb -s 127.0.0.1:5555 shell input tap --ev ABS_MT_POSITION_X {x} --ev ABS_MT_POSITION_Y {y}")

def perform_macro_events(events):
    for event in events:
        if event["EventType"] == "MouseMove":
            move_cursor(int(event['X']), int(event['Y']))
            # Пауза между событиями
            time.sleep(0.5)

def send_event(device, event_type, event_code, event_value):
    command = f"adb -s {device} shell sendevent /dev/input/event4 {event_type} {event_code} {event_value}"
    subprocess.run(command, shell=True)




if __name__ == "__main__":

    emulator_id = 'emulator-5554'  # Идентификатор вашего эмулятора
    device_serial = SC.connectDevice()
    #subprocess.run(['adb', 'connect', f'{device_serial}'])
    output_screen = "ekran.jpg"

    manager = CoordinatesManager()
    manager.load_from_file("output.txt")
    t = time.localtime()
    print(time.strftime("%H:%M:%S", t) + f" Я подключился к эмулятору : {device_serial}")
    #device_serial = SC.connectDevice(emulator_id)  # конектимся к эмулятору
    #global countFarm
    #countFarm = 0
    maxCountLegions = 3

    #comand="adb -s " + str(device_serial) + "shell am force-stop com.farlightgames.samo.gp"
    #subprocess.run(
    #subprocess.run(['adb', '-s', device_serial, 'shell', 'am', 'force-stop', 'com.farlightgames.samo.gp'])
    SC.take_screenshot(device_serial, emulator_id, output_screen)

    """
    while True:

        SC.bootGame(manager,device_serial,emulator_id)

        SC.healLegions(manager, device_serial, emulator_id)
        SC.startFarm(manager,device_serial, emulator_id, maxCountLegions)

        SC.tapFromFile(manager, "MAIN", "menu")
        time.sleep(random.randint(2, 10))
        SC.checkHeroes(manager)
        #time.sleep(random.randint(100, 200))
        #SC.tapFromFile(manager, "MAIN", "menu")
        #time.sleep(random.randint(100, 200))
        time.sleep(random.randint(2, 10))
        SC.tapFromFile(manager, "TRASH", "hand")
        SC.pathOfTheDragon(manager)
        t = time.localtime()
        print(time.strftime("%H:%M:%S", t) + " - ушел спать")
        subprocess.run(['adb', '-s', device_serial , 'shell', 'am', 'force-stop', 'com.farlightgames.samo.gp'])
        time.sleep(random.randint(1800, 2700))


    #time.sleep(1000)
"""
"""


    #SC.take_screenshot(device_serial, emulator_id, output_screen)
    #img = output_screen



"""













