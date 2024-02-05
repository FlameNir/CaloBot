import subprocess
import os
import time
import re
import tkinter as tk
import pytesseract as tes
from PIL import Image, ImageTk, ImageEnhance
import random
import numpy as np


def disconnect_all_devices():
    # Отключаем все устройства
    subprocess.run(['adb', 'disconnect'])


def connectDevice():
    # Запускаем ADB Server (если не запущен)
    subprocess.run(['adb', 'start-server'])

    # Отключаем все устройства перед новым подключением
    disconnect_all_devices()

    # Подключаемся к эмулятору
    #subprocess.run(['adb', 'connect', f'127.0.0.1:{emulator_id}'])  # 127.0.0.1:5555

    # Даем время для установки соединения
    time.sleep(3)

    # Получаем список устройств и эмуляторов
    devices = subprocess.check_output(['adb', 'devices']).decode('utf-8').strip().split('\n')[1:]

    # Если есть хотя бы одно устройство, возвращаем его серийный номер
    if devices:
        global device_serial
        device_serial = devices[0].split('\t')[0]
        subprocess.run(['adb', 'connect', device_serial])
        return devices[0].split('\t')[0]
    else:
        print("Не обнаружено подключенных устройств.")
        return None


def disconnectDevice(device_serial):
    # Отключаемся от устройства
    subprocess.run(['adb', '-s', device_serial, 'disconnect'])


def take_screenshot(device_serial, emulator_id, output_file):
    # Создаем скриншот с помощью adb shell screencap
    subprocess.run(['adb', '-s', device_serial, 'shell', 'screencap', '/sdcard/screenshot.png'])

    # Копируем скриншот с устройства на компьютер
    subprocess.run(['adb', '-s', device_serial, 'pull', '/sdcard/screenshot.png', output_file])

    # Отключаемся от устройства
    t = time.localtime()
    print(time.strftime("%H:%M:%S", t) + f" - Скриншот сохранен в {output_file}")


def tap_coordinates(x, y, device_serial):
    x=x+random.uniform(1,2)
    y = y + random.randint(1, 2)
    command = f"adb -s {device_serial} shell input tap {x} {y}"
    subprocess.run(command, shell=True)


def get_touch_events(device_path):
    adb_command = f'adb shell getevent -lt {device_path}'

    try:
        events = subprocess.check_output(adb_command, shell=True, stderr=subprocess.STDOUT, text=True)
        print(events)
    except subprocess.CalledProcessError as e:
        t = time.localtime()
        print(time.strftime("%H:%M:%S", t) + f"Ошибка при выполнении команды {adb_command}: {e.output}")


def on_mouse_click(event, image_name):
    global last_click  # Объявляем, что мы будем использовать глобальную переменную

    x = event.x
    y = event.y
    click_info = f"{image_name} : {x}, {y}"

    print(click_info)

    # Обновляем переменную с последним нажатием
    last_click = click_info

    return last_click


def scrinOut(output_file, image_name):
    root = tk.Tk()
    root.title(image_name)

    # Открываем изображение с помощью PIL
    # image_path = "screenshot.png"  # Замените путем к вашему изображению
    img = Image.open(output_file)

    # Преобразуем изображение в формат, поддерживаемый Tkinter
    tk_img = ImageTk.PhotoImage(img)

    # Создаем виджет Label для отображения изображения
    label = tk.Label(root, image=tk_img)
    label.pack()
    label.bind("<Button-1>", lambda event: on_mouse_click(event, image_name))
    # Запускаем Tkinter main loop
    root.mainloop()


def filter_last_occurrence(input_file, output_file):
    # Создаем словарь для хранения последних записей для каждого слова
    last_occurrence = {}

    # Читаем данные из файла и обрабатываем каждую строку
    with open(input_file, 'r') as file:
        for line in file:
            # Разделяем строку на слово и координаты
            parts = line.strip().split(':')
            if len(parts) == 2:
                word = parts[0].strip()
                coordinates = parts[1].strip()

                # Обновляем последнюю запись для текущего слова
                last_occurrence[word] = f"{word} : {coordinates}"

    # Записываем последние записи в выходной файл
    with open(output_file, 'w') as output:
        output.write('\n'.join(last_occurrence.values()))


class CoordinatesManager:
    def __init__(self):
        self.coordinates = {}

    def add_coordinates(self, category, name, x, y):
        if category not in self.coordinates:
            self.coordinates[category] = {}
        self.coordinates[category][name] = f"{name} : {x}, {y}"

    def save_to_file(self, filename):
        with open(filename, 'w') as file:
            for category, coordinates_dict in self.coordinates.items():
                file.write(f"{category.upper()}:\n")
                for name, coords in coordinates_dict.items():
                    file.write(f"    {coords}\n")

    def load_from_file(self, filename):
        with open(filename, 'r') as file:
            current_category = None
            for line in file:
                line = line.strip()
                if line.endswith(":"):
                    current_category = line[:-1].strip()
                elif current_category and ":" in line:
                    name, coords = line.split(":")
                    name = name.strip()
                    coords = coords.strip()
                    x, y = map(int, coords.split(","))
                    self.add_coordinates(current_category, name, x, y)


def checkLegions(maxCountLegions, image):
    textOnTheScreen = tes.image_to_string(image, lang='rus+eng')
    # print (textOnTheScreen)
    count = -1
    # print(textOnTheScreen)

    if (textOnTheScreen.find("0/" + str(maxCountLegions)) != -1):
        # print("0 легионов")
        count = 0
    if (textOnTheScreen.find("1/" + str(maxCountLegions)) != -1):
        # print("1 легионов")
        count = 1
    if (textOnTheScreen.find("2/" + str(maxCountLegions)) != -1):
        # print("2 легионов")
        count = 2
    if (textOnTheScreen.find("3/" + str(maxCountLegions)) != -1):
        # print("3 легионов")
        count = 3
    if (textOnTheScreen.find("4/" + str(maxCountLegions)) != -1):
        # print("4 легионов")
        count = 4
    if (textOnTheScreen.find("5/" + str(maxCountLegions)) != -1):
        # print("5 легионов")
        count = 5
    return count


def tapFromFile(manager, main, extra):
    main_coords = manager.coordinates.get(main, {}).get(extra)
    if main_coords:
        x, y = map(int, main_coords.split(":")[1].strip().split(","))
        #print(device_serial)
        tap_coordinates(x, y, device_serial)
    else:
        print("Поврежден файл координат")
    time.sleep((random.randint(10, 30)) / 10)


def farmgGoldWoodStone(manager, whatNaxFarm):
    tapFromFile(manager, "MAIN", "main")
    tapFromFile(manager, "MAIN", "search")
    tapFromFile(manager, whatNaxFarm, "mine")
    tapFromFile(manager, whatNaxFarm, "lvl1_mine")
    tapFromFile(manager, whatNaxFarm, "search_mine")
    tapFromFile(manager, "MAIN", "middle")
    tapFromFile(manager, "MAIN", "gather")
    tapFromFile(manager, "MAIN", "create_legion")
    tapFromFile(manager, "MAIN", "march")
    tapFromFile(manager, "MAIN", "main")

def bootGame(manager,device_serial,emulator_id):
    t = time.localtime()
    print(time.strftime("%H:%M:%S", t) + " - Запускаю игру")
    tapFromFile(manager, "MAIN", "game")
    time.sleep(40)
    output_screen = "screenshot.png"
    take_screenshot(device_serial, emulator_id, output_screen)
    textOnTheScreen = tes.image_to_string(output_screen, lang='rus+eng')
    if textOnTheScreen.find("CONFIRM")!= -1 or textOnTheScreen.find("Подтвердить")!= -1 or textOnTheScreen.find("Confirm")!= -1 or textOnTheScreen.find("ПОДТВЕРДИТЬ")!= -1:
        t = time.localtime()
        print(time.strftime("%H:%M:%S", t) + " - Ошибка входа, перезапуск")
        subprocess.run(['adb', '-s', device_serial, 'shell', 'am', 'force-stop', 'com.farlightgames.samo.gp'])
        bootGame(manager,device_serial,emulator_id)
    else:
        t = time.localtime()
        print(time.strftime("%H:%M:%S", t) + " - Успешный вход в игру")
def startFarm(manager,device_serial, emulator_id, maxCountLegions):
    tapFromFile(manager, "MAIN", "profile")
    tapFromFile(manager, "MAIN", "legions")
    output_screen = "screenshot.png"
    take_screenshot(device_serial, emulator_id, output_screen)
    img = output_screen
    global countFarm
    countFarm = 0
    countLegions = checkLegions(maxCountLegions, img)

    tapFromFile(manager, "MAIN", "profile")
    tapFromFile(manager, "MAIN", "profile")
    if countLegions != -1:
        for i in range(maxCountLegions - countLegions):
            if countFarm == 3:
                countFarm = 0
            if countFarm == 0:
                farmgGoldWoodStone(manager, "GOLD")
                print("Негры на GOLD")
                countFarm += 1
            elif countFarm == 1:
                farmgGoldWoodStone(manager, "WOOD")
                print("Негры на WOOD")
                countFarm += 1
            elif countFarm == 2:
                farmgGoldWoodStone(manager, "STONE")
                print("Негры на STONE")
                countFarm += 1
        time.sleep(1)
    else:
        tapFromFile(manager, "MAIN", "confirm")


def adjust_contrast(image_path, contrast_factor):
    # Открываем изображение
    image = Image.open(image_path)

    # Конвертируем изображение в режим RGB
    image = image.convert("RGB")

    # Создаем объект для регулировки контраста
    enhancer = ImageEnhance.Contrast(image)

    # Изменяем контраст
    image_with_adjusted_contrast = enhancer.enhance(contrast_factor)

    # Сохраняем измененное изображение
    image_with_adjusted_contrast.save("screenshot.jpg")

def adjust_color(image_path, color_factor):
    # Открываем изображение
    image = Image.open(image_path)

    # Конвертируем изображение в режим RGB
    image = image.convert("RGB")

    # Создаем объект для регулировки цвета
    enhancer = ImageEnhance.Color(image)

    # Изменяем цвет
    image_with_adjusted_color = enhancer.enhance(color_factor)

    # Сохраняем измененное изображение
    image_with_adjusted_color.save("screenshot.jpg")


def replace_color(image_path, target_color, replacement_color, tolerance=30):
    # Открываем изображение
    image = Image.open(image_path)

    # Преобразуем изображение в массив NumPy для более удобной обработки
    img_array = np.array(image)

    # Определяем границы цвета с учетом допустимого отклонения (tolerance)
    lower_bound = np.array([component - tolerance for component in target_color])
    upper_bound = np.array([component + tolerance for component in target_color])

    # Создаем маску для пикселей, соответствующих цвету в пределах заданного отклонения
    mask = np.all((img_array[:, :, :3] >= lower_bound) & (img_array[:, :, :3] <= upper_bound), axis=-1)

    # Заменяем цвет на новый цвет
    img_array[mask, :3] = replacement_color

    # Создаем новое изображение из массива NumPy
    new_image = Image.fromarray(img_array)

    # Сохраняем измененное изображение в формате PNG
    new_image.save("image_with_replaced_color.png", format='PNG')


def healLegions(manager,device_serial, emulator_id):
    tapFromFile(manager, "BUILDING", "treatment_build")
    tapFromFile(manager, "BUILDING", "treatment_enter")
    output_screen = "screenshot.png"
    take_screenshot(device_serial, emulator_id, output_screen)
    textOnTheScreen = tes.image_to_string(output_screen, lang='rus+eng')
    if textOnTheScreen.find("отряды")!=-1:
        t = time.localtime()
        print(time.strftime("%H:%M:%S", t) + " - Найдены тяжелораненые отряды")
        tapFromFile(manager, "BUILDING", "heal_legions")
        tapFromFile(manager, "MAIN", "profile")
    else:
        t = time.localtime()
        print(time.strftime("%H:%M:%S", t) + " - Все вылечены")
        tapFromFile(manager, "MAIN", "profile")


def checkHeroes(manager):
    tapFromFile(manager, "MAIN", "heroes")
    random_number = random.randint(2, 8)
    time.sleep(random.randint(2, 10))
    hero = "hero" + str(random_number)
    tapFromFile(manager, "TRASH", hero)
    time.sleep(random.randint(2, 10))
    random_number = random.randint(1, 4)
    time.sleep(random.randint(2, 10))
    if random_number==4:
        random_number = random.randint(1, 8)
        hero = "hero" + str(random_number)
        time.sleep(random.randint(2, 10))
        tapFromFile(manager, "TRASH", hero)
    random_number = random.randint(1, 3)
    if random_number==1:
        time.sleep(random.randint(2, 10))
        tapFromFile(manager, "TRASH", "art")
    elif random_number==2:
        tapFromFile(manager, "TRASH", "talents")
    elif random_number == 3:
        tapFromFile(manager, "TRASH", "skills")
        time.sleep(random.randint(2, 10))
    tapFromFile(manager, "MAIN", "profile")
    time.sleep(random.randint(2, 10))
    tapFromFile(manager, "MAIN", "profile")
def pathOfTheDragon(manager):
    tapFromFile(manager, "TRASH", "path_of_the_dragon_button")
    tapFromFile(manager, "TRASH", "path_of_the_dragon")
    time.sleep(random.randint(6,10))
    tapFromFile(manager, "TRASH", "dragon_exp")
    tapFromFile(manager, "TRASH", "get_xp")
    #проверку на то, что добычи нет или маол
    tapFromFile(manager, "TRASH", "dragon_out")
    tapFromFile(manager, "TRASH", "dragon_out")
    time.sleep(random.randint(6, 10))



"""
def fullscreen():
    window_handle = FindWindow(None, "BlueStacks App Player")
    window_rect   = GetWindowRect(window_handle)   
    image = pyscreenshot.grab(bbox=window_rect) 
    image.save("testscreen.png")
    return tes.image_to_string(Image.open('testscreen.png'), lang = 'rus+eng')"""
