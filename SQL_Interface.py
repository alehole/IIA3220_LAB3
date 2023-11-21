import numpy as np
import matplotlib.pyplot as plt
import pyodbc 
import datetime
import pandas
import array
import sys 
conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=MSI\CITADEL;'
                      'Database=LAB3;'
                      'Trusted_Connection=yes;')
 
cursor = conn.cursor()

n_samples = str(input("Specify number of samples to plot: "))
str1 = 'SELECT TOP '+ n_samples + ' Value, Timestamp, TagName FROM LOG WHERE TagName = '
str3 = ' ORDER BY [Timestamp] DESC'

#100''DROP TABLE LAB3.dbo.CHARTDATA--

str2 = '\'TT01\''
SqlQuery = str1+str2+str3
print(SqlQuery)
#cursor.execute('SELECT TOP 50 Value, Timestamp, TagName FROM LOG WHERE TagName = \'TT01\' ORDER BY [Timestamp] DESC')
cursor.execute(SqlQuery)

PV_arr = []
PV_Timestamp = []
for i in cursor:
    PV_arr.append(i.Value)
    PV_Timestamp.append(i.Timestamp)


str2 = '\'SP\''
SqlQuery = str1+str2+str3
#cursor.execute('SELECT TOP 50 Value, Timestamp, TagName FROM LOG WHERE TagName = \'SP\' ORDER BY [Timestamp] DESC')
cursor.execute(SqlQuery)
SP_arr = []
for i in cursor:
    SP_arr.append(i.Value)

str2 = '\'CV\''
SqlQuery = str1+str2+str3
#cursor.execute('SELECT TOP 50 Value, Timestamp, TagName FROM LOG WHERE TagName = \'CV\' ORDER BY [Timestamp] DESC')
cursor.execute(SqlQuery)
CV_arr = []
for i in cursor:
    CV_arr.append(i.Value)


plt.plot(PV_Timestamp, PV_arr, label ='PV[°C]')
plt.plot(PV_Timestamp, SP_arr, label ='SP[°C]')
plt.plot(PV_Timestamp, CV_arr, label ='CV[0-100%]')

plt.xlabel("Time")
plt.legend()
plt.title('Heater PID controller')
plt.grid()
plt.show()

