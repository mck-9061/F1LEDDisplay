import datetime
import threading
from datetime import timezone

from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
import time
import openf1_interface

options = RGBMatrixOptions()
options.rows = 32
options.cols = 64
#options.disable_hardware_pulsing = 1

matrix = RGBMatrix(options = options)
canvas = matrix.CreateFrameCanvas()

delay = 35

# drivers = [
#     "ANT",
#     "VER",
#     "RUS",
#     "HAM",
#     "LEC",
#     "NOR",
#     "PIA",
#     "HAD",
#     "LAW",
#     "GAS",
#     "LIN",
#     "COL",
#     "BEA",
#     "BOR",
#     "HUL",
#     "OCO",
#     "ALO",
#     "SAI",
#     "ALB",
#     "TSU",
#     "HIR",
#     "STR"
# ]

def draw_border(r, g, b):
    for x in range(0, 64):
        canvas.SetPixel(x, 0, r, g, b)
        canvas.SetPixel(x, 31, r, g, b)

    for y in range(0, 32):
        canvas.SetPixel(0, y, r, g, b)
        canvas.SetPixel(63, y, r, g, b)

def draw_chequered_border(r, g, b):
    black = (int(time.time()) % 2 == 0)

    for x in range(0, 64):
        if not black:
            canvas.SetPixel(x, 0, r, g, b)
            canvas.SetPixel(x, 31, r, g, b)

        if x % 4 == 0:
            black = not black

    for y in range(0, 32):
        if not black:
            canvas.SetPixel(0, y, r, g, b)
            canvas.SetPixel(63, y, r, g, b)

        if y % 4 == 0:
            black = not black

def display_drivers(drivers, colours):
    i = 0

    x = 1
    y = 8

    font = graphics.Font()

    for driver in drivers:
        colour = colours[i]
        r = int(colour[0:2], 16)
        g = int(colour[2:4], 16)
        b = int(colour[4:6], 16)

        textColour = graphics.Color(r, g, b)

        if i == 0:
            font.LoadFont("./fonts/7x7-7.bdf")
        elif i == 1:
            font.LoadFont("./fonts/5x6-6.bdf")
        elif i == 2:
            font.LoadFont("./fonts/4x5-5.bdf")
        elif i == 3:
            font.LoadFont("./fonts/4x4-4.bdf")
        else:
            font.LoadFont("./fonts/3x4-4.bdf")

        graphics.DrawText(canvas, font, x, y, textColour, driver)

        i += 1

        if i == 1: y = 15
        elif i == 2: y = 21
        elif i == 3: y = 26
        elif i == 4: y = 31
        elif i == 5:
            x = 26
            y = 10
        else:
            y += 5
            if y > 30:
                y = 5
                x += 13

def format_timedelta(td):
    hours, remainder = divmod(td.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    return f"{td.days:02d}:{hours:02d}:{minutes:02d}:{seconds:02d}"

d = []
def get_driver_data_initial():
    global d

    while not d:
        d = openf1_interface.get_current_driver_data()
        time.sleep(0.5)

t = openf1_interface.get_next_session_time()

th = threading.Thread(target=get_driver_data_initial)
th.start()

while not d:
    delta = t - datetime.datetime.now(timezone.utc)
    f = format_timedelta(delta)

    canvas = matrix.SwapOnVSync(canvas)
    canvas.Clear()

    font = graphics.Font()
    textColour = graphics.Color(255, 0, 0)
    font.LoadFont("./fonts/5x7.bdf")

    graphics.DrawText(canvas, font, 5, 19, textColour, f)
    draw_border(255, 255, 255)

drivers = []

current_order = ["HLD", "HLD", "HLD", "HLD", "HLD", "HLD", "HLD", "HLD", "HLD", "HLD", "HLD", "HLD", "HLD", "HLD", "HLD", "HLD", "HLD", "HLD", "HLD", "HLD", "HLD", "HLD"]
current_colours = ["FFFFFF", "FFFFFF", "FFFFFF", "FFFFFF", "FFFFFF", "FFFFFF", "FFFFFF", "FFFFFF", "FFFFFF", "FFFFFF", "FFFFFF", "FFFFFF", "FFFFFF", "FFFFFF", "FFFFFF", "FFFFFF", "FFFFFF", "FFFFFF", "FFFFFF", "FFFFFF", "FFFFFF", "FFFFFF"]

def fetch_data():
    while True:
        openf1_interface.get_race_control()
        order = openf1_interface.get_latest_positions()
        print(order)

        i = 0
        for driver_num in order:
            i += 1

            driver_obj = {}

            for driver in d:
                if driver["driver_number"] == driver_num:
                    driver_obj["name"] = driver["name_acronym"]
                    driver_obj["position"] = i
                    driver_obj["colour"] = driver["team_colour"]
                    driver_obj["valid_at"] = datetime.datetime.now(timezone.utc) + datetime.timedelta(seconds=delay)

            drivers.append(driver_obj)

        time.sleep(0.5)

th = threading.Thread(target=fetch_data)
th.start()

while True:
    canvas = matrix.SwapOnVSync(canvas)
    canvas.Clear()

    if openf1_interface.red_flag:
        draw_border(0, 0, 255)
    elif openf1_interface.chequered_flag:
        draw_chequered_border(255, 255, 255)
    elif openf1_interface.safety_car:
        draw_chequered_border(247, 104, 6)
    elif openf1_interface.virtual_safety_car:
        draw_chequered_border(255, 255, 0)
    elif openf1_interface.yellow_sectors or openf1_interface.double_yellow_sectors:
        draw_border(255, 255, 0)
    else:
        draw_border(0, 30, 0)

    # Construct drivers array
    new_drivers = []
    for driver in drivers:
        if driver["valid_at"] <= datetime.datetime.now(timezone.utc):
            current_order[driver["position"]] = driver["name"]
            current_colours[driver["position"]] = driver["colour"]
        else:
            new_drivers.append(driver)

    drivers = new_drivers

    display_drivers(current_order, current_colours)