from PIL import Image
import numpy as np


def rellena_color(imagen, cordenada, color):
    y, x = cordenada
    if imagen[y][x] == color:
        return
    else:
        colorantiguo = imagen[:][y][x]
        imagen[y][x] = color
        if y > 0 and imagen[y-1][x] == colorantiguo:
            rellena_color(imagen, (y-1, x), color)
        if y < len(imagen)-1 and imagen[y+1][x] == colorantiguo:
            rellena_color(imagen, (y+1, x), color)
        if x > 0 and imagen[y][x-1] == colorantiguo:
            rellena_color(imagen, (y, x-1), color)
        if x < len(imagen[0])-1 and imagen[y][x+1] == colorantiguo:
            rellena_color(imagen, (y, x+1), color)

    pass


def show_imagen(imagen):
    nparray = np.array(imagen)
    image = Image.fromarray(nparray, 'L')
    image.save('imagen.png','PNG')

    image.show()
def print_imagen(imagen):
    for i in imagen:
        print(i)


def main():
    imagen = [
        [255, 000, 100, 100, 170, 170, 200, 200, 255, 255],
        [255, 000, 255, 255, 255, 255, 255, 255, 255, 255],
        [255, 000, 000, 255, 000, 255, 255, 255, 255, 255],
        [255, 255, 000, 255, 255, 255, 100, 000, 255, 255],
        [255, 255, 100, 255, 255, 100, 100, 255, 000, 255],
        [255, 255, 100, 255, 100, 100, 100, 000, 255, 000],
        [255, 255, 100, 100, 100, 100, 255, 255, 255, 255],
        [255, 255, 255, 255, 100, 100, 255, 255, 255, 255],
        [255, 255, 255, 000, 100, 100, 255, 255, 255, 255],
        [000, 255, 255, 255, 255, 000, 000, 000, 000, 000],
        [000, 000, 255, 255, 255, 255, 000, 255, 000, 255],
        [000, 255, 000, 255, 255, 255, 000, 000, 000, 255],
        [000, 000, 255, 000, 255, 255, 255, 255, 255, 255],
        [000, 000, 255, 255, 000, 255, 255, 255, 255, 255],
    ]
    show_imagen(imagen)
    print()
    cordenada = (0, 0)
    color = 0
    rellena_color(imagen, cordenada, color)
    show_imagen(imagen)


if __name__ == "__main__":
    main()
