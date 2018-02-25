from tkinter import Label,Tk,filedialog
from PIL import Image, ImageTk
import numpy as np 
import statistics
from problem import *
from search import heuristic1, heuristic2


def discretizacion(pixel_block):
    red_average = [pixel_block[p][0] for p in range (len(pixel_block))]
    green_average = [pixel_block[p][1] for p in range (len(pixel_block))]
    blue_average = [pixel_block[p][2] for p in range (len(pixel_block))]
    # print("Rojo: ", red_average)
    # print("Verde: ", green_average)
    # print("Azul: ", blue_average)
    color = [np.average(red_average), np.average(green_average), np.average(blue_average)]
    print("color:", color)
    return color

def coloring(element):
    if element == "+":
        return np.array([0, 0, 0])
    elif element == "0":
        return np.array([255, 255, 255])
    elif element == "g":
        return np.array([0, 255, 0])
    elif element == "s":
        return np.array([255, 0, 0])
    else:
        return np.array([255, 255, 255])


root = Tk()



path=filedialog.askopenfilename(filetypes=[("Image File",'.jpg')])
im = Image.open(path)

tkimage = ImageTk.PhotoImage(im)
myvar=Label(root,image = tkimage)
myvar.image = tkimage
myvar.pack()

blocks = 10
pixel_matrix = np.asarray(im)


print(pixel_matrix)

print(pixel_matrix.shape)

print(pixel_matrix.shape[0])
print(len(pixel_matrix[0])/blocks)
segments =round(len(pixel_matrix[0])/blocks) 

intervals = [(p, p+segments)  for p in range(0,len(pixel_matrix[0]),segments)
    if (p+segments) < len(pixel_matrix[0])
]

print(intervals[-1][1])
intervals.append((intervals[-1][1], intervals[-1][1] + (len(pixel_matrix[0])- intervals[-1][1])))
print (intervals)
print(pixel_matrix[0])

    # if (pixel_matrix.shape[0] >= intervals[i][1]) 
    #     and (pixel_matrix.shape[1] >= intervals[i][1]) 
    #     and pixel_matrix.shape[0] >= intervals[i][0] 
    #     and pixel_matrix.shape[1] >= intervals[i][0]

colores_rgb =[ 
    [pixel_matrix[j][p] 
        for j in range(intervals[i][0],intervals[i][1])
        for p in range(intervals[z][0],intervals[z][1])
    ]  for i in range(len(intervals))
    for z in range(len(intervals))
]
print("Primer block",len(colores_rgb))




for p in range(20, 30):
    for j in range(0, 10):
         print("Original colors: ",pixel_matrix[p][j])



matriz_discreta = [
[0 for p in range(len(intervals))]
 for i in range(len(intervals))
]


print(len(matriz_discreta))

contador_x = 0
contador_j = 0

for i in range (len(colores_rgb)):
    color = discretizacion(colores_rgb[i])
    sum_of_colors = color[0] + color[1] + color[2]
    #print(pixel_matrix[i])
    if (contador_x < len(matriz_discreta)):
        if contador_j < len(matriz_discreta[0]):
            if ((color[0] == color[1] and color[0] == color[2] and color[1] == color[2]) and (color[0] < 100 and color[1] < 100 and color[2] < 100)):
                 matriz_discreta[contador_x][contador_j] = "+"
                 print("NEGRO")
            elif ((color[0] == color[1] and color[0] == color[2] and color[1] == color[2]) and (color[0] > 100 and color[1] > 100 and color[2] > 100)):
                 matriz_discreta[contador_x][contador_j] = "0"
                 print("Blanco")
            elif (statistics.mean((color[0], color[1], color[2])) < 10):
                 matriz_discreta[contador_x][contador_j] = "+"
                 print("NEGRO")
                #print (sum_of_colors)
            elif (statistics.mean((color[0], color[1], color[2])) > 200):
                matriz_discreta[contador_x][contador_j] = "0"
                print("BLANCO")
            else:
                if (color[0] >= color[1]) and  (color[0] >= color[2]):
                    matriz_discreta[contador_x][contador_j] = "s"
                    print ( " ES ROJOOOOOOOO" )
                elif (color[1] >= color[0] and color[1] >= color[2]):
                    matriz_discreta[contador_x][contador_j] = "g"
                    print("Verde")
                else:
                    matriz_discreta[contador_x][contador_j] = "0"
                    print("Blanco")
            print(matriz_discreta[contador_x][contador_j])
            contador_j += 1
            if contador_j >= len(matriz_discreta[0]):
                contador_x += 1
                contador_j = 0

pixel_matrix.setflags(write=1)
#  for i in range(len(pixel_matrix)):
#     print(pixel_matrix[i])

problema = Problem(matriz_discreta)
print(problema.actions(problema.initial()))
print(heuristic1(problema, problema.initial()))
print(heuristic2(problema, problema.initial()))

for i in range(len(intervals)):
    for p in range(len(intervals)):
        new_color = coloring(matriz_discreta[i][p])
        for j in range(intervals[i][0],intervals[i][1]):
            for z in range(intervals[p][0],intervals[p][1]):
                pixel_matrix[j][z] = new_color

im = Image.fromarray(pixel_matrix)
im.save("your_file.jpg")


root.mainloop()
