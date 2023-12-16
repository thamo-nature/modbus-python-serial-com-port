"""
#!/usr/bin/env python
import requests
import json
import mysql.connector

from pyModbusTCP.client import ModbusClient

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="lifecell"
)

mycursor = mydb.cursor()

query = "select ip from pth_location"

mycursor.execute(query)

get_result = mycursor.fetchall()

list = [i[0] for i in get_result]

pth_data = []


for i in list:
             print(i)
             client = ModbusClient(host=i, port=1025, auto_open=True, auto_close=True, timeout=10)
             
             result = client.open()
             
             if(result == True):
                    data = client.read_holding_registers(0, 4)    # FUNCTIE 03 - Lees register 0, 1 lang
                    print(data)
                    if data:
                     #if client.open():
                       # data = response.registers
                        #print(data)
                        ##or 17,18,19
                        #no_of_rec = data[45]
                        #print("no of records")
                        #print(no_of_rec)
                        data_array = { "pth_sensor":i,"temp":str(data[0]),"humidity":str(data[2]),"pressure": str(data[1]) }
                        insert = "."
                        for key, value in data_array.copy().items():
                            #fareheit to degree (637 - 32)*5/9
                             if(key == "temp"):
                               #  data_array["tempa"]= value
                               afirst = value[:2]          
                               asecond = value[2:]
                               temp = float(afirst+insert+asecond)
                               data_array["tempa"] = temp
                               
                             if(key == "humidity"):
                               #  data_array["humidity"]= value
                                bfirst = value[:2]          
                                bsecond = value[2:]
                                hum = float(bfirst+insert+bsecond)
                                data_array["humidity"] = hum
                               
                             if(key == "pressure"):
                                cfirst = value[:2]          
                                csecond = value[2:]
                                pres = float(cfirst+insert+csecond)
                                data_array["pressure"]= pres
                               # pass
                        #print ("Waarde register: ", data[0])
                        pth_data.append(data_array)
                        client.close()
                    else:
                        # pass
                        data_array = [i,0]
                        pth_data.append(data_array)
                        
             else:
                     pass
#print(pth_data)

#reset_data = client.write.registera(46,1)

#api part
URL = "http://192.168.20.129/lifecell/api/pth_api.php"
final_data = {'pth' : json.dumps(pth_data)}
r = requests.post(url = URL, data = final_data,timeout=5)
print(r.text)
print(r.status_code)
"""

###!/usr/bin/env python
##import requests
##import json
##from pyModbusTCP.client import ModbusClient

"""
list = [
         "192.168.100.87"         
       ]

pth_data = []


for i in list:
             client = ModbusClient(host=i, port=1025, auto_open=True, auto_close=True, timeout=10)
             
             result = client.open()
             if(result == True):
                    data = client.read_holding_registers(0, 4)    # FUNCTIE 03 - Lees register 0, 1 lang
                    print(data)
                    if data:
                     #if client.open():
                       # data = response.registers
                        #print(data)
                        ##or 17,18,19
                        #no_of_rec = data[45]
                        #print("no of records")
                        #print(no_of_rec)
                        data_array = { "pth_sensor":i,"temp":str(data[0]),"humidity":str(data[2]),"pressure": str(data[1]) }
                        insert = "."
                        for key, value in data_array.copy().items():
                            #fareheit to degree (637 - 32)*5/9
                             if(key == "temp"):
                               #  data_array["tempa"]= value
                               afirst = value[:2]          
                               asecond = value[2:]
                               temp = float(afirst+insert+asecond)
                               data_array["tempa"] = temp
                               
                             if(key == "humidity"):
                               #  data_array["humidity"]= value
                                bfirst = value[:2]          
                                bsecond = value[2:]
                                hum = float(bfirst+insert+bsecond)
                                data_array["humidity"] = hum
                               
                             if(key == "pressure"):
                                cfirst = value[:2]          
                                csecond = value[2:]
                                pres = float(cfirst+insert+csecond)
                                data_array["pressure"]= pres
                               # pass
                        #print ("Waarde register: ", data[0])
                        pth_data.append(data_array)
                        client.close()
                    else:
                        # pass
                        data_array = [i,0]
                        pth_data.append(data_array)
                        
             else:
                     pass
print(pth_data)

#reset_data = client.write.registera(46,1)

#api part
URL = "http://192.168.20.129/lifecell/api/pth_api.php"
final_data = {'pth' : json.dumps(pth_data)}
r = requests.post(url = URL, data = final_data,timeout=5)
print(r.text)
print(r.status_code)
"""


#!/usr/bin/env python
import requests
import json
import mysql.connector
import ipaddress
from pyModbusTCP.client import ModbusClient

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="lifecell"
)

mycursor = mydb.cursor()

query = "select ip from pth_location"

mycursor.execute(query)

get_result = mycursor.fetchall()

list = [i[0] for i in get_result]

pth_data = []

empty_data_one = []

for i in list:
             ip_space_remove = i.replace(" ", "")
             ip_check = format(ipaddress.IPv4Address(ip_space_remove))
             #print(ip_check)

             count= 2 
             while(count > 0):
                 #print("Tryin to connect "+ str(ip_check) + " " +str(count) + "th time")
                 individual_pth_data = []
                
                 client = ModbusClient(host=ip_check, port=1025, auto_open=True, auto_close=True, timeout=3)
                 
                 result = client.open()
                 
                 if(result == True):
                        data = client.read_holding_registers(0, 4)    # FUNCTIE 03 - Lees register 0, 1 lang
                        #print(data)
                        if data:
                         #if client.open():
                           # data = response.registers
                            #print(data)
                            ##or 17,18,19
                            #no_of_rec = data[45]
                            #print("no of records")
                            #print(no_of_rec)
                            data_array = { "pth_sensor": ip_check,"temp":str(data[0]),"humidity":str(data[2]),"pressure": str(data[1]) }
                            insert = "."
                            for key, value in data_array.copy().items():
                                #fareheit to degree (637 - 32)*5/9
                                 if(key == "temp"):
                                   #  data_array["tempa"]= value
                                   afirst = value[:2]          
                                   asecond = value[2:]
                                   temp = float(afirst+insert+asecond)
                                   data_array["tempa"] = temp
                                   
                                 if(key == "humidity"):
                                   #  data_array["humidity"]= value
                                    bfirst = value[:2]          
                                    bsecond = value[2:]
                                    hum = float(bfirst+insert+bsecond)
                                    data_array["humidity"] = hum
                                   
                                 if(key == "pressure"):
                                    cfirst = value[:2]          
                                    csecond = value[2:]
                                    pres = float(cfirst+insert+csecond)
                                    data_array["pressure"]= pres
                                   # pass
                            #print ("Waarde register: ", data[0])
                            individual_pth_data.append(data_array)
                            client.close()
                            if individual_pth_data:
                               pth_data.append(data_array)
                               #print(pth_data)
                               break
                 count -=1
             
             else:
                # pass
                e_array = ip_check
                empty_data_one.append(e_array)
                print("unable to connect pth device "+ str(ip_check))
                            
##                 else:
##                         pass
#print(pth_data)
#print("Following are not pinging data")
#print(empty_data_one)
#reset_data = client.write.registera(46,1)

   
#api part
URL = "http://192.168.20.129/lifecell/api/pth_api.php"
final_data = {'pth' : json.dumps(pth_data)}
attempts = 3

while(attempts > 0):
        r = requests.post(url = URL, data = final_data,timeout=10)
        #print(r.text)
        print(r.status_code)
        if(r.status_code == 200):
             break
        else:
            attempts -=1
            print(attempts)
            
        print("Network not reachable")

