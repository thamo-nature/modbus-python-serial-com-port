#!/usr/bin/python3
#pip install pyserial
import serial
#for reading ports
import os
#import mysql.connector
#sending data to server
import requests
import time
from time import sleep

device_id = "inc_1"

#To Test Parameters
method_list = [ "rtu", "ascii", "binary" ]

baud_dict = [2400, 4800, 9600, 14400, 19200, 2800, 38400, 57600, 76800, 115200, 230400]

#slave_address = 0; #initialization from 1 – 247

parity_list = [ "N", "O", "E" ] # ‘E’ven, ‘O’dd or ‘N’one

stopbits_list = [ 0, 1, 2 ] # Number of stop bits 0-2

com_port = 5

timeout = 4 #default 3s

total_iteration_count = 0
def all_baudrate_slave_1_247(slave_address):

    global total_iteration_count

    for cbd, current_baud_rate in enumerate(baud_dict):

        for cp, current_parity in enumerate(parity_list):

            for csb, current_stop_bit in enumerate(stopbits_list):

                if(slave_address == 0):
                    for csa, current_slave_address in enumerate(range(1, 248)):
                        # client=ModbusClient(retries=3 ,method='rtu',port='COM9',
                        # baudrate=current_baud_rate ,timeout=3 ,parity=current_parity,stopbits=1 ,strict=False)
                        
                        # result = client.connect()
                        
                        # if(result == True):
                        #         #print(i)       

                        #         response=client.read_holding_registers(address = 0 ,count =37,unit=i)
                                
                        #         if not response.isError():
                        #                 data = response.registers
                        #                 print(data)
                        # client.close()
                          print("Slave ID " + str(current_slave_address) + " current baudrate: " + str(current_baud_rate) + " current parity: " + str(current_parity) + " current stop_bit: " + str(current_stop_bit) )
                          total_iteration_count += 1
                else:
                        # client=ModbusClient(retries=3 ,method='rtu',port='COM9',
                        # baudrate=current_baud_rate ,timeout=3 ,parity=current_parity,stopbits=1 ,strict=False)
                        
                        # result = client.connect()
                        
                        # if(result == True):
                        #         #print(i)       

                        #         response=client.read_holding_registers(address = 0 ,count =37,unit=i)
                                
                        #         if not response.isError():
                        #                 data = response.registers
                        #                 print(data)
                        # client.close()
                          print("Slave ID " + str(slave_address) + " current baudrate: " + str(current_baud_rate) + " current parity: " + str(current_parity) + " current stop_bit: " + str(current_stop_bit) )
                          total_iteration_count += 1

    print(total_iteration_count)     

#slave_address default assign something like 2 # 99time
#or it will scan from 1 to 247 = 24453 time
all_baudrate_slave_1_247(1)
