import socket
import re
import pyodbc 
import time
import numpy as np
import matplotlib.pyplot as plt
import time
from Tmr import *
import json

def trunc(floatNum, decimal_places):
    multiplier = 10 ** decimal_places
    return int(floatNum * multiplier) / multiplier 

Values = []
def readUDP(T_SP, Sim):
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    message = bytesAddressPair[0]
    address = bytesAddressPair[1]
    clientMsg = "UDP message :{}".format(message)
    clientIP  = "UDP Client IP Address:{}".format(address)
    #print(clientMsg)
    #print(clientIP)
    global Values
    Values = list(clientMsg.split(','))
    if(Values):
        global SP, CV, PV
        SP = Values[1]
        CV = Values[3]
        PV = Values[5]
        PV = PV[:-1]
        #print("PV: " + PV)
        #print("SP: " + SP)
        #print("CV: " + CV)
    # Sending a reply to client
    sendStr = str(T_SP) +"," +str(Sim)
    bytesToSend         = str.encode(sendStr)
    UDPServerSocket.sendto(bytesToSend, address)

SP = -1.0
PV = -1.0
CV = -1
            
def Updt_SQL_Local(value, name):
    if(PV != -1.0):
        dbCon = pyodbc.connect('Driver={SQL Server};'
                              'Server=MSI\CITADEL;'
                              'Database=LAB3;'
                              'Trusted_Connection=yes;')
        cursor  = dbCon.cursor ()

        str1 = "insert into LOG(Value, Timestamp, TagName) values ("
        str2 = str(value)
        str3 = ", CURRENT_TIMESTAMP ,'"
        str4 = str(name)
        str5 = "')"
        SqlQuery = str1+str2+str3+str4+str5
        #print(SqlQuery)
        cursor.execute(SqlQuery)
        dbCon.commit()
        print(SqlQuery)
           
def Updt_SQL_Azure(value, name):
    if(PV != -1.0):
        dbCon=pyodbc.connect('Driver={SQL Server};'
                    'Server=iia-lab-ah.database.windows.net;'
                    'Database=LAB3;'
                    'UID=adm;'
                    'PWD=iia_2017pw;')

        cursor  = dbCon.cursor ()

        str1 = "insert into LOG(Value, Timestamp, TagName) values ("
        str2 = str(value)
        str3 = ", CURRENT_TIMESTAMP ,'"
        str4 = str(name)
        str5 = "')"
        SqlQuery = str1+str2+str3+str4+str5
        #print(SqlQuery)
        cursor.execute(SqlQuery)
        dbCon.commit()
        print(SqlQuery)
        
def ParseJson():
	f = open('ControllerInterface.json')
	data = json.load(f)
	#for i in data['PID1']:
	#	print(i)
	sp = float(data['PID1'][0]['SP'])
	sim = eval(data['PID1'][1]['Simulate'])
	# Closing file
	f.close()
	return [sp, sim]

if __name__ == "__main__":
    localIP     = "0.0.0.0"
    localPort   = 20001
    bufferSize  = 200
    UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    UDPServerSocket.bind((localIP,localPort))
    Tmr1 = Tmr(1)  # Update SQL
    Tmr2 = Tmr(4)  # Parse JSon
    Tmr3 = Tmr(1)  # Update Azure Sql Server
    
    T_SP = 24.5
    Sim = False
    
    try:
        while True:
            Tmr1.tmrStart()
            Tmr2.tmrStart()
            Tmr3.tmrStart()
            
            readUDP(T_SP,Sim)
            
            if Tmr1.pulse():
                Updt_SQL_Local(PV, 'TT01')
                Updt_SQL_Local(CV, 'CV')
                Updt_SQL_Local(SP, 'SP')
                
            if Tmr2.pulse():
                [T_SP, Sim ] = ParseJson()
            
            if Tmr3.pulse():
                Updt_SQL_Azure(PV, 'TT01')
                Updt_SQL_Azure(CV, 'CV')
                Updt_SQL_Azure(SP, 'SP')
                
    except KeyboardInterrupt:
        print("\nKeyboard exit")








# localIP     = "0.0.0.0"
# localPort   = 20001
# bufferSize  = 1024
# msgFromServer       = "Hello UDP Client"
# bytesToSend         = str.encode(msgFromServer)

# # Create a datagram socket
# UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
# # Bind to address and ip
# #UDPServerSocket.bind((localIP, localPort))
# UDPServerSocket.bind((localIP,localPort))
# print("UDP server up and listening")
# # Listen for incoming datagrams
# while(True):
#     bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
#     message = bytesAddressPair[0]
#     address = bytesAddressPair[1]
#     clientMsg = "Message from Client:{}".format(message)
#     clientIP  = "Client IP Address:{}".format(address)
    
#     print(clientMsg)
#     print(clientIP)
#     # Sending a reply to client
#     #UDPServerSocket.sendto(bytesToSend, address)