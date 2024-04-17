Creating an Arduino-Based Robotic Spider Using Simulink and Stateflow
-----------------------------------------------
Description:

This demo utilizes an Arduino board, 3D printed parts, eight servo motors and various
other supporting hardware components to control a robotic spider. The body of the spider
is made of 3D printed parts and several pushbuttons dictate the movement of the spider.

To Run This Demo:
Step 1: Build the spider using the parts printed from 'Spider_3DPrint.stl'
Step 2: Construct the circuit shown in the provided schematic
Step 3: Run the model in external mode to verify that your setup works
Step 4(optional): Deploy the model to hardware to enable computer-free operation

Notes:
1) The circuit schematic has been included as "Arduino_Robotic_Spider_Schematic.png" along with this ReadMe
and the .stl file for the custom parts. The final set up can be seen in 'Robotic_Spider_SetUp.png'

2) When you deploy the model to hardware, you will need to find a power supply that can supply 
sufficient current and power. A good option to try is a Li-po battery.

3) The servo position values may need to be altered depending on the orientation of the legs 
in your spider build. In the provided model, one side of the spider was oriented differently than 
the other side. Additionally, the weight distribution of all the supporting components and circuitry 
may affect how well the spider moves. 
