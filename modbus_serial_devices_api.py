#!/usr/bin/env python
import requests
import json
from pymodbus.client.sync import ModbusSerialClient as ModbusClient

#slave id of devices

list = [1,2,3]

chart_data = []

for i in list:

            client=ModbusClient(method='rtu',port='COM1',
            baudrate=9600,timeout=1,parity='N',stopbits=1 ,strict=False)            
            result = client.connect()
            
            if(result == True):
                    #Read holding registers give count according to the device registers
                    #i is the slave id

                    response=client.read_holding_registers(address = 0 ,count =37,unit=i)
                    
                    if not response.isError():
                            data = response.registers
                            #read whatever register you want
                            data_array = { "id":i,"register_2":str(data[2]),"register_3":str(data[3]),"register_5":str(data[5]),"register_4":data[4] }

                            #add read values to the declared variable
                            chart_data.append(data_array)
                            client.close()
                    else:
                           #if failed to read registers
                           # pass
                            data_array = {"id":i,"failed_to_read":0}
                            chart_data.append(data_array)

                    
            else:
                    pass
                    
print(chart_data)

#api part code

URL = "http://server_ip/modbus_api.php"
final_data = {'modbus_data' : json.dumps(chart_data)}
r = requests.post(url = URL, data = final_data,timeout=5)
print(r.text)
print(r.status_code)

###in your server handle the data 
