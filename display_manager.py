from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
import time
import openf1_interface

options = RGBMatrixOptions()
options.rows = 32
options.cols = 64
options.disable_hardware_pulsing = 1

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
        r = int("0x" + colour[0:2])
        g = int("0x" + colour[2:4])
        b = int("0x" + colour[4:6])

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


d = openf1_interface.get_result_previous()
drivers = [driver["name_acronym"] for driver in d]
colours = [driver["team_colour"] for driver in d]

while True:
    display_drivers(drivers, colours)
    canvas = matrix.SwapOnVSync(canvas)