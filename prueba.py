from tkinter import Label, Tk, filedialog
from PIL import Image, ImageTk
import numpy as np
import statistics
from problem import *
from search import graph_search
import sys

def discretizacion(pixel_block):
    red_average = [pixel_block[p][0] for p in range (len(pixel_block))]
    green_average = [pixel_block[p][1] for p in range (len(pixel_block))]
    blue_average = [pixel_block[p][2] for p in range (len(pixel_block))]

    # print("Rojo: ", red_average)
    # print("Verde: ", green_average)
    # print("Azul: ", blue_average)
    return [
        np.average(red_average),
        np.average(green_average),
        np.average(blue_average)
    ]

def coloring(element):
    if element == '+':
        return np.array([0, 0, 0])

    elif element == '0':
        return np.array([255, 255, 255])

    elif element == 'g':
        return np.array([0, 255, 0])

    elif element == 's':
        return np.array([255, 0, 0])

    else:
        return np.array([255, 255, 255])

root = Tk()

# TODO: Uncomment
# path = filedialog.askopenfilename(filetypes = [('Image File', '.jpg')])
path = 'C:\\Users\\Pablo\\Pictures\\input.jpg'

im = Image.open(path)

tkimage = ImageTk.PhotoImage(im)

# TODO: Remove if unused
# myvar = Label(root, image = tkimage)
# myvar.image = tkimage
# myvar.pack()

pixel_matrix = np.asarray(im)

blocks = 10

segments = round(len(pixel_matrix[0]) / blocks)

intervals = [
    (p, p + segments)
    for p in range(0, len(pixel_matrix[0]), segments)
    if (p + segments) < len(pixel_matrix[0])
]

intervals.append(
    (
        intervals[-1][1],
        intervals[-1][1]
            + (len(pixel_matrix[0]) - intervals[-1][1])
    )
)

# if (pixel_matrix.shape[0] >= intervals[i][1])
#     and (pixel_matrix.shape[1] >= intervals[i][1])
#     and pixel_matrix.shape[0] >= intervals[i][0]
#     and pixel_matrix.shape[1] >= intervals[i][0]

# Matriz de bloques a partir de la imágen original
colores_rgb = [
    [
        pixel_matrix[j][p]
        for j in range(intervals[i][0], intervals[i][1])
        for p in range(intervals[z][0], intervals[z][1])
    ]
    for i in range(len(intervals))
    for z in range(len(intervals))
]

matriz_discreta = [
    [
        0 for p in range(len(intervals))
    ]
    for i in range(len(intervals))
]

contador_x = 0
contador_j = 0

# Construcción de la matriz que representa la imágen discretizada
# '+' representa negro o pared
# '0' representa blanco
# 's' representa rojo
# 'g' representa verde

# TOOD: Subject to optimization
for i in range(len(colores_rgb)):
    color = discretizacion(colores_rgb[i])
    sum_of_colors = color[0] + color[1] + color[2]

    if (contador_x < len(matriz_discreta)):
        if contador_j < len(matriz_discreta[0]):
            if (
                (
                    color[0] == color[1]
                        and color[0] == color[2]
                        and color[1] == color[2]
                )
                    and (
                        color[0] < 100
                            and color[1] < 100
                            and color[2] < 100
                    )
            ):
                # Negro
                matriz_discreta[contador_x][contador_j] = "+"

            elif ((color[0] == color[1] and color[0] == color[2] and color[1] == color[2]) and (color[0] > 100 and color[1] > 100 and color[2] > 100)):
                # Blanco
                matriz_discreta[contador_x][contador_j] = "0"

            elif (statistics.mean((color[0], color[1], color[2])) < 10):
                # Negro
                matriz_discreta[contador_x][contador_j] = "+"

            elif (statistics.mean((color[0], color[1], color[2])) > 200):
                # Blanco
                matriz_discreta[contador_x][contador_j] = "0"

            else:
                if (color[0] >= color[1]) and  (color[0] >= color[2]):
                    # Rojo
                    matriz_discreta[contador_x][contador_j] = "s"

                elif (color[1] >= color[0] and color[1] >= color[2]):
                    # Verde
                    matriz_discreta[contador_x][contador_j] = "g"

                else:
                    # Blanco
                    matriz_discreta[contador_x][contador_j] = "0"

            contador_j += 1

            if contador_j >= len(matriz_discreta[0]):
                contador_x += 1
                contador_j = 0

pixel_matrix.setflags(write = 1)

problema = Problem(matriz_discreta)

# Imprimir imagen discretizada
for i in range(len(intervals)):
    for p in range(len(intervals)):
        new_color = coloring(matriz_discreta[i][p])
        for j in range(intervals[i][0],intervals[i][1]):
            for z in range(intervals[p][0],intervals[p][1]):
                pixel_matrix[j][z] = new_color

im = Image.fromarray(pixel_matrix)
im.save('your_file.jpg')

# print(problema.actions(problema.initial()))
# print(heuristic1(problema, problema.initial()))
# print(heuristic2(problema, problema.initial()))

# TODO: Completar
# Elegir algoritmo para aplicación de graphsearch, esto podría
# venir de los argumentos de ejecución del programa
algorithm = 'a_star'
heuristic_function = problema.steps_to_reach_goal_heuristic

# TODO: Completar
# if heuristic_function == 'steps_to_reach_goal_heuristic':
#     heuristic_function == problema.steps_to_reach_goal_heuristic
# elif heuristic_function == 'shortest_distance_heuristic':
#     heuristic_function == problema.shortest_distance_heuristic

result = graph_search(problema, algorithm, heuristic_function)

# TODO: Modificar problem matrix to add result and reprint

if result:
    print('')
    print('------------------------------')
    print('Got a solution path:\n', result)
    print('------------------------------')
else:
    print('')
    print('------------------------------')
    print('Got no solution path')
    print('------------------------------')

root.mainloop()
