from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics

options = RGBMatrixOptions()
options.rows = 32
options.cols = 64
options.disable_hardware_pulsing = 1

matrix = RGBMatrix(options = options)
canvas = matrix.CreateFrameCanvas()

drivers = [
    "ANT",
    "VER",
    "RUS",
    "HAM",
    "LEC",
    "NOR",
    "PIA",
    "HAD",
    "LAW",
    "GAS",
    "LIN",
    "COL",
    "BEA",
    "BOR",
    "HUL",
    "OCO",
    "ALO",
    "SAI",
    "ALB",
    "TSU",
    "HIR",
    "STR"
]

def display_drivers(drivers):
    i = 0

    x = 1
    y = 8

    font = graphics.Font()
    font.LoadFont("./fonts/3x4-4.bdf")

    for driver in drivers:
        if i == 0: font.LoadFont("./fonts/7x7-7.bdf")
        if i == 1: font.LoadFont("./fonts/5x6-6.bdf")
        if i == 2: font.LoadFont("./fonts/4x5-5.bdf")
        if i == 3: font.LoadFont("./fonts/4x4-4.bdf")
        else: font.LoadFont("./fonts/3x4-4.bdf")

        textColour = graphics.Color(0, 255, 0)

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


while True:
    display_drivers(drivers)
    canvas = matrix.SwapOnVSync(canvas)