from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics

options = RGBMatrixOptions()
options.rows = 32
options.cols = 64
options.disable_hardware_pulsing = 1

matrix = RGBMatrix(options = options)
canvas = matrix.CreateFrameCanvas()

font = graphics.Font()
font.LoadFont("./fonts/3x4.bdf")
textColour = graphics.Colour(0, 255, 0)

while True:
    canvas.Clear()
    graphics.DrawText(canvas, font, 0, 10, textColour, "HELLO WORLD")