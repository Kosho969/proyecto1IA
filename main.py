# Author: Pablo Barreno Koch 
# Main program 
# To run use 'py filename algorithm heuristic'
# i.e (py prueba.py bfs 1)


from tkinter import Label, Tk, filedialog, Toplevel, Canvas, BOTH, NW
from PIL import Image, ImageTk
import numpy as np
import statistics
from problem import *
from search import graph_search
import sys
import time

def discretizacion(pixel_block):
    red_average = [pixel_block[p][0] for p in range (len(pixel_block))]
    green_average = [pixel_block[p][1] for p in range (len(pixel_block))]
    blue_average = [pixel_block[p][2] for p in range (len(pixel_block))]

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
    elif element == 'p':
        return np.array([148, 0, 211])

    else:
        return np.array([255, 255, 255])

blocks = 15

# Segmento para escoger imagen
root = Tk()
print(str(sys.argv[1]))
print(str(sys.argv[2]))
path = filedialog.askopenfilename(filetypes = [('Image File', '.jpg'), ('bitmap', '.bmp')])
im = Image.open(path)
tkimage = ImageTk.PhotoImage(im)
# TODO: Remove if unused
myvar = Label(root, image = tkimage)
myvar.image = tkimage
myvar.pack()


# Separar en un arreglo la imagen 
pixel_matrix = np.asarray(im)

segments = round(len(pixel_matrix[0]) / blocks)

# Calculo de intervalos para la discretizacion 
intervals = [
    (p, p + segments)
    for p in range(0, len(pixel_matrix[0]), segments)
    if (p + segments) < len(pixel_matrix[0])
]

# Calcular el ultimo segmento de intervalo. s
intervals.append(
    (
        intervals[-1][1],
        intervals[-1][1]
            + (len(pixel_matrix[0]) - intervals[-1][1])
    )
)

# Matriz de bloques a partir de la imágen original
colores_rgb = [
    [
        pixel_matrix[j][p]
        for j in range(intervals[i][0], intervals[i][1])
        for p in range(intervals[z][0], intervals[z][1])
# Uncomment for non-square images
# if (pixel_matrix.shape[0] >= intervals[i][1])
#     and (pixel_matrix.shape[1] >= intervals[i][1])
#     and pixel_matrix.shape[0] >= intervals[i][0]
#     and pixel_matrix.shape[1] >= intervals[i][0]
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
                    round(color[0]) == round(color[1])
                        and round(color[0]) == round(color[2])
                        and round(color[1]) == round(color[2])
                )
                    and (
                        color[0] < 100
                            and color[1] < 100
                            and color[2] < 100
                    )
            ):
                # Negro
                matriz_discreta[contador_x][contador_j] = "+"

            elif (
                    (
                       round(color[0]) == round(color[1])
                        and round(color[0]) == round(color[2])
                        and round(color[1]) == round(color[2])
                    )
                        and 
                        (
                            color[0] > 100 
                            and color[1] > 100 
                            and color[2] > 100
                    )
                ):
                # Blanco
                matriz_discreta[contador_x][contador_j] = "0"

            elif (statistics.mean((color[0], color[1], color[2])) < 10):
                # Negro
                matriz_discreta[contador_x][contador_j] = "+"

            elif (statistics.mean((color[0], color[1], color[2])) > 200):
                # Blanco
                matriz_discreta[contador_x][contador_j] = "0"

            else:
                if (color[0] >= color[1]) and  (color[0] >= color[2] ):
                    # Rojo
                    print(color)
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

# Llamada al frameqork de problema 
problema = Problem(matriz_discreta)

# Impresion solo para mostrar progreso y representacion discreta
for j in range(len(matriz_discreta)):
    print(matriz_discreta[j])

# Imprimir imagen discretizada
for i in range(len(intervals)):
    for p in range(len(intervals)):
        new_color = coloring(matriz_discreta[i][p])
        for j in range(intervals[i][0],intervals[i][1]):
            for z in range(intervals[p][0],intervals[p][1]):
                pixel_matrix[j][z] = new_color


im = Image.fromarray(pixel_matrix)
im.save('discrete_image.jpg')

# Correr algoritmo de busqueda para las soluciones. 
algorithm = str(sys.argv[1])
option = str(sys.argv[2])
heuristic_function = problema.steps_to_reach_goal_heuristic

if option == '1':
    heuristic_function = problema.steps_to_reach_goal_heuristic
elif option == '2':
    heuristic_function = problema.shortest_distance_heuristic

t1 = time.time()
result = graph_search(problema, algorithm, heuristic_function)
t2 = time.time()

print("time: ", str(t2-t1))

if result:
# Si hay resultado entonces mostrar la imegn resultante, de lo contrario no mostrar solucion
    print('')
    print('------------------------------')
    print('Got a solution path:\n', result)
    print('------------------------------')

    for i in range(len(result)):
        matriz_discreta[result[i][0]][result[i][1]] = 'p'

    # Imprimir imagen discretizada
    for i in range(len(intervals)):
        for p in range(len(intervals)):
            new_color = coloring(matriz_discreta[i][p])
            for j in range(intervals[i][0],intervals[i][1]):
                for z in range(intervals[p][0],intervals[p][1]):
                    pixel_matrix[j][z] = new_color

    im = Image.fromarray(pixel_matrix)
    im.save('result.jpg')
    tkimage2 = ImageTk.PhotoImage(im)
    top = Toplevel()
    top.title('Optimized Map')
    top.wm_geometry("794x370")
    optimized_canvas = Canvas(top)
    optimized_canvas.pack(fill=BOTH, expand=1)
    optimized_image = optimized_canvas.create_image(0, 0, anchor=NW, image=tkimage2)
else:
    print('')
    print('------------------------------')
    print('Got no solution path')
    print('------------------------------')

root.mainloop()
