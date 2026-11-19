from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics

options = RGBMatrixOptions()
options.rows = 32
options.cols = 64
options.disable_hardware_pulsing = 1

matrix = RGBMatrix(options = options)
canvas = matrix.CreateFrameCanvas()

font = graphics.Font()
font.LoadFont("./fonts/5x7.bdf")
textColour = graphics.Color(0, 255, 0)
background = graphics.Color(255, 0, 0)

while True:
    graphics.DrawText(canvas, font, 0, 10, textColour, background, "HELLO WORLD")