import pandas as pd
import matplotlib.pyplot as plt
from tkinter import filedialog


# filename = filedialog.askopenfilename(initialdir="C:\\",
#                                       # initioaldir = "Which directory will the program open",
#                                       title="Select CSV File",
#                                       # title = "Title",
#                                       filetypes=(("csv files", "*.csv"), ("all files", "*.*")))

df_COM = pd.read_csv('Big Movement with first cut.csv',
                     delimiter=',',
                     decimal='.',
                     thousands=',',
                     # skiprows=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
                     )
print(df_COM)
big_movement_pixel_of_100cm = 413
ymax = (1280*100)/big_movement_pixel_of_100cm
xmax = (720*100)/big_movement_pixel_of_100cm
print('ymax = ' +str(ymax))
print('xmax = ' +str(xmax))
plot = plt.plot(df_COM['right_wrist_x'],df_COM['right_wrist_y'])
# plot = plt.plot(df_COM['right_wrist_y'])
plt.show()

def COM_segments(x_proximal,x_distal,y_proximal,y_distal,percentage_of_COM_segment):
    x = []
    y = []
    for i in range(len(x_proximal)):
        x_data = (x_proximal[i] + (percentage_of_COM_segment) * (x_distal[i] - x_proximal[i])) * xmax
        x.append(x_data)
        y_data = (y_proximal[i] + (percentage_of_COM_segment) * (y_distal[i] - y_proximal[i])) * ymax
        y.append(y_data)
    return x,y
#βραχιωνας
right_forarm = COM_segments(df_COM['right_shoulder_x'],df_COM['right_elbow_x'],df_COM['right_shoulder_y'],df_COM['right_elbow_y'],3.2)
print(type(right_forarm))
print(right_forarm)
print(right_forarm[1])
# vasili

