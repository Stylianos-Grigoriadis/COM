import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from tkinter import filedialog
from matplotlib.widgets import SpanSelector


# filename = filedialog.askopenfilename(initialdir="C:\\",
#                                       # initioaldir = "Which directory will the program open",
#                                       title="Select CSV File",
#                                       # title = "Title",
#                                       filetypes=(("csv files", "*.csv"), ("all files", "*.*")))
import lib

df_COM = pd.read_csv('Big Movement with first cut video.csv',
                     delimiter=',',
                     decimal='.',
                     thousands=',',
                     # skiprows=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
                     )
#print(df_COM)
column_names = list(df_COM.columns.values)
print(column_names)
column_names.remove('timestamp')
column_names.remove('angle_left')
column_names.remove('angle_right')
print(column_names)


big_movement_pixel_of_1m = 413 #pixel
ymax = (1280*1)/big_movement_pixel_of_1m
xmax = (720*1)/big_movement_pixel_of_1m
print('ymax = ' +str(ymax))
print('xmax = ' +str(xmax))
#plot = plt.plot(df_COM['right_wrist_x'],df_COM['right_wrist_y'])
# plot = plt.plot(df_COM['right_wrist_y'])
#plt.show()

def COM_segments(x_proximal,x_distal,y_proximal,y_distal,distance_of_CoM_of_each_segment_from_the_proximal,mi):
    #mi = εκατοστιαια ποσοτητα μαζας καθε μελους
    #print(type(x_proximal))
    #if x_proximal[0] == 'left_heel_x':
       # print(True)
    #print(x_proximal)
    x = []
    y = []
    for i in range(len(x_proximal)):
        x_data = (x_proximal[i] - (x_proximal[i] - x_distal[i]) * distance_of_CoM_of_each_segment_from_the_proximal) * xmax
        #x_data = (x_proximal[i] + (distance_of_CoM_of_each_segment_from_the_proximal) * (x_distal[i] - x_proximal[i])) * xmax
        x.append(x_data*mi)
        y_data = (y_proximal[i] - (y_proximal[i] - y_distal[i]) * distance_of_CoM_of_each_segment_from_the_proximal) * ymax
        y_data = abs(ymax - y_data)
        #y_data = (y_proximal[i] + (distance_of_CoM_of_each_segment_from_the_proximal) * (y_distal[i] - y_proximal[i])) * ymax
        y.append(y_data*mi)
    return x,y
#find the coordinates of each segment
#use of πινακας 5.8 kollias
#right_upperarm
right_upperarm = COM_segments(df_COM['right_shoulder_x'],df_COM['right_elbow_x'],df_COM['right_shoulder_y'],df_COM['right_elbow_y'],0.436,0.027)
#print(type(right_upperarm))
#print(right_upperarm)
#print(right_upperarm[1])
#left_upperarm
left_upperarm = COM_segments(df_COM['left_shoulder_x'],df_COM['left_elbow_x'],df_COM['left_shoulder_y'],df_COM['left_elbow_y'],0.436,0.027)
#head_and_neck
#head_and_neck = COM_segments(df_COM['left_shoulder_x'],df_COM['left_elbow_x'],df_COM['left_shoulder_y'],df_COM['left_elbow_y'],2.8)
#right_forarm
right_forarm = COM_segments(df_COM['right_elbow_x'],df_COM['right_index_x'],df_COM['right_elbow_y'],df_COM['right_index_y'],0.677,0.023)
#left_forarm
left_forarm = COM_segments(df_COM['left_elbow_x'],df_COM['left_index_x'],df_COM['left_elbow_y'],df_COM['left_index_y'],0.677,0.023)
# #right_palm
# right_palm = COM_segments(df_COM['right_wrist_x'],df_COM['right_index_x'],df_COM['right_wrist_y'],df_COM['right_index_y'],0.6)
# #left_palm
# left_palm = COM_segments(df_COM['left_wrist_x'],df_COM['left_index_x'],df_COM['left_wrist_y'],df_COM['left_index_y'],0.6)
#right_thigh
right_thigh = COM_segments(df_COM['right_hip_x'],df_COM['right_knee_x'],df_COM['right_hip_y'],df_COM['right_knee_y'],0.433,0.102)
#left_thigh
left_thigh = COM_segments(df_COM['left_hip_x'],df_COM['left_knee_x'],df_COM['left_hip_y'],df_COM['left_knee_y'],0.433,0.102)
#right_shank
right_shank = COM_segments(df_COM['right_knee_x'],df_COM['right_ankle_x'],df_COM['right_knee_y'],df_COM['right_ankle_y'],0.433,0.046)
#left_shank
left_shank = COM_segments(df_COM['left_knee_x'],df_COM['left_ankle_x'],df_COM['left_knee_y'],df_COM['left_ankle_y'],0.433,0.046)
#right_foot
right_foot = COM_segments(df_COM['right_heel_x'],df_COM['right_foot_index_x'],df_COM['right_heel_y'],df_COM['right_foot_index_y'],0.149,0.015)
#left_foot
left_foot = COM_segments(df_COM['left_heel_x'],df_COM['left_foot_index_x'],df_COM['left_heel_y'],df_COM['left_foot_index_y'],0.149,0.015)
#to find the trunk we need to take the average position of the shoulders and the hips and assume that
#the trunk is the distance between those
#proximal from shoulders
#distal from hips
proximal_trunk_x = []
proximal_trunk_y = []
distal_trunk_x = []
distal_trunk_y = []
for i in range(len(df_COM['right_shoulder_x'])):

    #print(i)
    proximal_x = ((df_COM['right_shoulder_x'][i]+df_COM['left_shoulder_x'][i])/2) * xmax
    #print(type(proximal_x))
    proximal_trunk_x.append(proximal_x)
    proximal_y = ((df_COM['right_shoulder_y'][i] + df_COM['left_shoulder_y'][i]) / 2) * ymax
    proximal_trunk_y.append(proximal_y)
    distal_x = ((df_COM['right_hip_x'][i]+df_COM['left_hip_x'][i])/2) * xmax
    distal_trunk_x.append(distal_x)
    distal_y = ((df_COM['right_hip_y'][i] + df_COM['left_hip_y'][i]) / 2) * ymax
    distal_trunk_y.append(distal_y)
#print(proximal_trunk_x)
trunk = COM_segments(proximal_trunk_x,distal_trunk_x,proximal_trunk_y,distal_trunk_y,0.500,0.495)
#print(type(trunk))
#To find the head and neck coordinates we will add 12.5 cm to each of the nose data so that we can find the
#highest position of the head at each time and use the proximal trunk positions (x,y) as proximal position of
#the neck
#first we make a list with the nose data so that we can turn them form percentages to cm and then add 12.5
head_neck_distal_x = []
head_neck_distal_y = []

for i in range(len(df_COM['nose_x'])):
    x = (df_COM['nose_x'][i] * xmax)
    head_neck_distal_x.append(x)
    y = (df_COM['nose_y'][i] * ymax) + 12.5
    head_neck_distal_y.append(y)
#print(head_neck_distal_x)
head_neck = COM_segments(proximal_trunk_x,head_neck_distal_x,proximal_trunk_y,head_neck_distal_y,0.567,0.079)

#To find the coordinates (x,y) of the CoM
print(head_neck[0])
print(head_neck[1])
print(head_neck[0][1])
#for i in range(len(head_neck)):
COM_x = []
COM_y = []
for i in range(len(head_neck[0])):
    COMx = right_upperarm[0][i] + left_upperarm[0][i] + right_forarm[0][i] + left_forarm[0][i] + right_thigh[0][i] + left_thigh[0][i] + right_shank[0][i] + left_shank[0][i] + right_foot[0][i] + left_foot[0][i] + trunk[0][i] + head_neck[0][i]
    COMy = right_upperarm[1][i] + left_upperarm[1][i] + right_forarm[1][i] + left_forarm[1][i] + right_thigh[1][i] + left_thigh[1][i] + right_shank[1][i] + left_shank[1][i] + right_foot[1][i] + left_foot[1][i] + trunk[1][i] + head_neck[1][i]
    COM_x.append(COMx)
    COM_y.append(COMy)

# print(COM_x)
# print(COM_y)
# #plot = plt.plot(COM_x,COM_y)
# fig,(ax1,ax2,ax3)=plt.subplots(3)
# ax1.plot(COM_x)
# ax2.plot(COM_y)
# ax3.plot(COM_x,COM_y)
# #plt.legend('Center of Mass')
# plt.show()

df_force = pd.read_csv('Big Movement force.csv',
                     delimiter=',',
                     decimal='.',
                     thousands=',',
                     skiprows=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
                     index_col= False
                     )
print(df_force.columns)
df_force.rename(columns = {'Time (s)':'Time (s)',
                              'CHANNEL_1' : 'CHANNEL_1L',
                              'CHANNEL_2' : 'CHANNEL_2L',
                              'CHANNEL_3' : 'CHANNEL_3L',
                              'CHANNEL_4' : 'CHANNEL_4L',
                              'Unnamed: 5': 'Unnamed: 5',
                              'CHANNEL_1.1' : 'CHANNEL_1R',
                              'CHANNEL_2.1' : 'CHANNEL_2R',
                              'CHANNEL_3.1' : 'CHANNEL_3R',
                              'CHANNEL_4.1' : 'CHANNEL_4R'
                           }, inplace = True)
print(df_force.columns)
# plt.plot(df_force['CHANNEL_1.1'], df_force['CHANNEL_1'])
# plt.show()
# fig,(ax1,ax2,ax3,ax4)=plt.subplots(4)
# ax1.plot(df_force['CHANNEL_1.1'])
# ax2.plot(df_force['CHANNEL_2.1'])
# ax3.plot(df_force['CHANNEL_3.1'])
# ax4.plot(df_force['CHANNEL_4.1'])
#
# #plt.legend('Center of Mass')
# plt.show()
list_of_right_platform = []

for i in range(len(df_force['CHANNEL_1R'])):
    list = df_force['CHANNEL_1R'][i] + df_force['CHANNEL_2R'][i] + df_force['CHANNEL_3R'][i] + df_force['CHANNEL_4R'][i]
    list_of_right_platform.append(list)
    print(list_of_right_platform[i])

fig, (ax1) = plt.subplots(1)

ax1.plot(list_of_right_platform)
ax1.set_title('Press left mouse button and drag '
              'to select a region in the top graph')

def onselect(xmin, xmax):
    max_y = list_of_right_platform[int(xmin)]
    global max_y_index
    for l in range(int(xmin),int(xmax)):
        if list_of_right_platform[l] > max_y:
            max_y = list_of_right_platform[l]
            max_y_index = l

    print(max_y)
    print(max_y_index)

span = SpanSelector(
    ax1,
    onselect,
    "horizontal",
    useblit=True,
    props=dict(alpha=0.5, facecolor="tab:red"),
    interactive=True,
    drag_from_anywhere=True
)
plt.show()
print(df_force)

print(df_force)
print(len(COM_y))
df_force = df_force[max_y_index:].reset_index()
del df_force["index"]
print(df_force)
list_of_right_platform = list_of_right_platform[max_y_index:]
COM_y = COM_y[:797]
COM_x = COM_x[:797]

step = len(COM_y)/len(list_of_right_platform)
COM_y = lib.Linear_Interpolation(COM_y,step,plus=0)
COM_x = lib.Linear_Interpolation(COM_x,step,plus=0)

fig,ax=plt.subplots()
ax.plot(list_of_right_platform, label = 'Force',color='blue')
ax2 = ax.twinx()
plt.plot(COM_x,label='CoM',color='red')
plt.legend()
plt.show()

CoP = lib.compute_cop(31,26,df_force)

fig,ax=plt.subplots()
ax.plot(CoP[0], label = 'CoP',color='blue')
ax2 = ax.twinx()
plt.plot(COM_x,label='CoM',color='red')
plt.legend()
plt.show()
print(CoP[0])

