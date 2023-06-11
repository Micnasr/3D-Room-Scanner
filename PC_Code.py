import serial
import numpy as np
import open3d as o3d
from math import cos, sin, radians

from math import cos, sin

#IMPORTANT: When you press the onboard BUTTON J0 the machine will perform 64 measurements. After its done it will reverse back to home and prompt you to continue, if you dont it will open a graph with the results

s = serial.Serial('COM4', 115200, timeout=10)
print("Opening: " + s.name)

# reset the buffers of the UART port to delete the remaining data in the buffers
s.reset_output_buffer()
s.reset_input_buffer()

# wait for user's signal to start the program
input("Press Enter to start communication...")

angle = ""
distance = ""
data = []
count = 0
passes = 0
depth = 0

#Data Points Per Rotation
points_per = 64

while True:

    count = 0
    while True:
        x = s.readline()
        print(x.decode())

        try:
            angle = x.decode().split(" ")[5].strip()
            distance = x.decode().split(" ")[1][:-1]
            
            if (angle != "" and distance.isdecimal()):
                data.append([depth, distance, angle])
                count+=1

        except:
            print("")

        if (distance.isdecimal()):
            if ((count >= points_per) or (float(angle) >= (360-(float(360/points_per)))-1)):
                break

    passes+=1
    #lab asks for no depth
    depth+=0

    ans = input('Continue? Y/N ')

    if (ans == 'N'):
        print("Data Gathering Process Terminated")
        break
       


#close the port
print("Closing: " + s.name)
s.close()


cartesian_array = []


for polar_point in data:
    distance = float(polar_point[1])
    angle = radians(float(polar_point[2]))
    x = polar_point[0]
    y = distance * cos(angle)
    z = distance * sin(angle)
    cartesian_point = [x, y, z]
    cartesian_array.append(cartesian_point)


if __name__ == "__main__":
    #Remember the goals of modularization
    #   -- smaller problems, reuse, validation, debugging
    #To simulate the data from the sensor lets create a new file with test data 
    f = open("demofile2dx.xyz", "w")    #create a new file for writing 
    
    #Test data: Lets make a rectangular prism as a point cloud in XYZ format
    #   A simple prism would only require 8 vertices, however we
    #   will sample the prism along its x-axis a total of 10x
    #   4 vertices repeated 10x = 40 vertices
    #   This for-loop generates our test data in xyz format
    
    for points in cartesian_array:
            f.write('{0:d} {1:.4f} {2:.4f}\n'.format(points[0], points[1], points[2]))
        
    f.close()   #there should now be a file containing 40 vertex coordinates                               
    
    #Read the test data in from the file we created        
    print("Read in the prism point cloud data (pcd)")
    pcd = o3d.io.read_point_cloud("demofile2dx.xyz", format="xyz")

    #Lets see what our point cloud data looks like numerically       
    print("The PCD array:")
    print(np.asarray(pcd.points))

    #Lets see what our point cloud data looks like graphically       
    print("Lets visualize the PCD: (spawns seperate interactive window)")
    o3d.visualization.draw_geometries([pcd])

    #OK, good, but not great, lets add some lines to connect the vertices
    #   For creating a lineset we will need to tell the packahe which vertices need connected
    #   Remember each vertex actually contains one x,y,z coordinate

    #Give each vertex a unique number
    yz_slice_vertex = []
    for x in range(0,count*passes):
        yz_slice_vertex.append([x])

    lines = []  
    stepper = 1
    for x in range(0,count*passes,count):
        for i in range(x, (stepper*count)-1,1):
            lines.append([yz_slice_vertex[i], yz_slice_vertex[i+1]])
        lines.append([yz_slice_vertex[x+count-1], yz_slice_vertex[x]])
        stepper+=1

    stepper = 1
    if (passes != 1):
        passes -= 1
        for x in range(0,count*(passes),1):
            lines.append([yz_slice_vertex[x], yz_slice_vertex[x+count]])

            stepper +=1

    #This line maps the lines to the 3d coordinate vertices
    line_set = o3d.geometry.LineSet(points=o3d.utility.Vector3dVector(np.asarray(pcd.points)),lines=o3d.utility.Vector2iVector(lines))

    #Lets see what our point cloud data with lines looks like graphically       
    o3d.visualization.draw_geometries([line_set])