#from LAB3 import *
from ControlSystem import *
from gpiozero import MCP3002
import RPi.GPIO as GPIO
import re
from datetime import datetime
import json
from Simulator import *
import threading
import time
import socket
from Tmr import *
from PID import *

# Read MCP3002 ADC channel
adc = MCP3002(channel=1, differential=False)
def TMP36_C(channel, offset):
	adcdata = adc.value; 		# Value between 0 and 1
	voltvalue = adcdata * 5;	# Convert to volt
	return 100*voltvalue-50 + offset	# Temp in celsius
	
def UDP_msg(SP, CV, PV):
	msgFromClient       = "SP,"+str(SP) + "," "CV,"+str(CV) + ",""PV,"+str(PV)
	bytesToSend         = str.encode(msgFromClient)
	serverAddressPort   = ("192.168.9.5", 20001)
	bufferSize          = 200
	# Create a UDP socket at client side
	UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
	# Send to server using created UDP socket
	UDPClientSocket.sendto(bytesToSend, serverAddressPort)
	msgFromServer = UDPClientSocket.recvfrom(bufferSize)
	msg = "Message from Server {}".format(msgFromServer[0])
	#print(msg)
	return msg
	
def scale(rawVal, rawMax, rawMin, ScaledMax, ScaledMin):
	return (ScaledMax - ScaledMin)/(rawMax-rawMin)*(rawVal-rawMin)+ScaledMin
	
def push(a, n):
     a = np.roll(a, 1)
     a[0] = n
     return a

def str2bool(msg):
	if msg == "True'":
		return True
	else:
		return False
  
if __name__ == "__main__":
	GPIO.setup(12,GPIO.OUT) 	# PWM output for CV
	CV_PWM = GPIO.PWM(12,1000)	#create PWM instance with frequency
	CV_PWM.start(0)				#start PWM of required Duty Cycle 

	T_SP = 24.5
	Sim = False;
	
	Tf = 2 # sec
	Ts = 1 # sec
	kp = 0.8
	Ti = 20
	Td = 0
	
	PID1 = PID(Ts, Tf)
	Heater_Sim = Simulator(20.0, Ts)
	
	Tmr1 = Tmr(Ts)  # PID
	Tmr2 = Tmr(3) 	# Print data to console 
	
	try:
		while True:
			Tmr1.tmrStart()
			Tmr2.tmrStart()
					
			# PID controller, Simulator, UDP
			if Tmr1.pulse():
				if(Sim):
					Temperature =  Heater_Sim.AirHeaterModel(CV)
				else:
					Temperature =  PID1.LowPassFilter(TMP36_C(1, 0))
				CV = PID1.Controller(Temperature,T_SP,False,kp,Ti,Td,5,0, Tf, Ts)
				CV_0_100 = scale(CV,0, 5,0, 100)
				CV_PWM.ChangeDutyCycle(CV_0_100)
				Udp_msg = UDP_msg(T_SP, CV_0_100 ,Temperature)
			
				#print(Udp_msg)
				Values = list(Udp_msg.split(','))
				SP = re.findall(r"[-+]?\d*\.\d+|\d+", Values[0])
				T_SP = float(SP[0])
				Sim = str2bool(str(Values[1]))

			# Print values
			if Tmr2.pulse():
				#print("TMP36 Temperature " + str(TMP36_C(1, 0))+ " Celsius")
				print("CV " + str(PID1.trunc(CV,2))+ " CV%: " + str(PID1.trunc(CV_0_100,2))  + " PV: " + str(PID1.trunc(PID1.PV,2)) + " SP: " + str(T_SP) + " Simulating: " + str(Sim))
				
	except KeyboardInterrupt:
			print("\nKeyboard exit")
