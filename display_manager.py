from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
import time
import openf1_interface

options = RGBMatrixOptions()
options.rows = 32
options.cols = 64
#options.disable_hardware_pulsing = 1

matrix = RGBMatrix(options = options)
canvas = matrix.CreateFrameCanvas()

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


d = openf1_interface.get_current_driver_data()
print(d)

while not d:
    delta = openf1_interface.get_time_until_next_session()
    f = format_timedelta(delta)

    canvas = matrix.SwapOnVSync(canvas)
    canvas.Clear()

    font = graphics.Font()
    textColour = graphics.Color(255, 0, 0)
    font.LoadFont("./fonts/5x7.bdf")

    graphics.DrawText(canvas, font, 0, 19, textColour, f)

    time.sleep(0.3)

    d = openf1_interface.get_current_driver_data()


while True:
    order = openf1_interface.get_latest_positions()
    print(order)
    drivers = []
    colours = []

    for driver_num in order:
        for driver in d:
            if driver["driver_number"] == driver_num:
                drivers.append(driver["name_acronym"])
                colours.append(driver["team_colour"])

    canvas = matrix.SwapOnVSync(canvas)
    canvas.Clear()
    display_drivers(drivers, colours)
    time.sleep(1)