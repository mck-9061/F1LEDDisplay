from rgbmatrix import RGBMatrix, RGBMatrixOptions

options = RGBMatrixOptions()
options.rows = 32
options.cols = 64
options.disable_hardware_pulsing = 1

matrix = RGBMatrix(options = options)

while True:
    matrix.Fill(0, 0, 255)