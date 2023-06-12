# 3D-Room-Scanner :milky_way:
 ## Simple Demo

https://github.com/Micnasr/3D-Room-Scanner/assets/44876651/8eb9bd10-51ab-415c-9767-50d06f5833d9


 
 ## About
My mission is to revolutionize the way we perceive and interact with our surroundings. Using a time of flight sensor, I have developed a system that can scan an entire room and generate a detailed image of its shape. It enables users to explore and analyze the spatial dimensions of any environment effortlessly. Whether it's for architectural design, virtual reality, or smart home applications, The sensor's precise measurements and high-resolution imaging capabilities will undoubtedly redefine the way we experience and understand the world around us. 

<br />

<img align = Right width="50%" alt="image" src="https://github.com/Micnasr/3D-Room-Scanner/assets/44876651/579fd76a-d0b2-4556-8142-624dfa45ddd0">

### Hardware ⚙
* Microcontroller (MSP432E401Y)
* Time of Flight Sensor (vl53l1x)
* Stepper Motor (28byj-48)
* Motor Driver (ULN2003)

<br />

### How it works :zap:
The microcontroller communicates with the time of flight sensor using I2C in order to take up to 512 measurements per meter. 

The sensor will rotate 360 degrees while taking measurements of the area to get a complete picture. The data in polar form (distance, angle) is transmitted to the computer using the UART communication protocol. 

The data is then converted to cartesian form (x, y, z) which can be graphed onto the screen. All the vertices are connected together to give the final render a polish. To capture depth, the machine needs to be moved every time the sensor compeletes a 360 degree turn. In order to make sure that the wires don't get tangled, the motor will spin backwards after a full turn to reset its position.

All user input to start/stop the data acquisition process is done using polling on the microcontroller.

<br />

### Data sheet

[Datasheet.pdf](https://github.com/Micnasr/3D-Room-Scanner/files/11729097/Datasheet.pdf)

<br />

### Examples :camera:
![image](https://github.com/Micnasr/3D-Room-Scanner/assets/44876651/3684cee7-2dc8-4a35-a2ff-7fea29ed6001)

![image](https://github.com/Micnasr/3D-Room-Scanner/assets/44876651/dffde2b4-c0c4-4526-b839-db442b3066d3)

