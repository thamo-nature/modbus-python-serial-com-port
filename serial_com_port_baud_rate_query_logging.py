import serial
from time import sleep

import sys
baud_dict = [2400, 4800, 9600, 14400, 19200, 2800, 38400, 57600, 76800, 115200, 230400]
#baud_dict = [ 9600]

asc_query = [ 'TIL00\r' , '?00TIL00\r' ,'TIL00\r\n' ,
              '?00TIL00\r\n', '0110 0001\r', '0001 0000\r',
              '0001 0001\r', '0001 0011\r', '0001 0010\r',
              '0110 0001\r\n', '0001 0000\r\n', '0001 0001\r\n',
              '0001 0011\r\n', '0001 0010\r\n'
            ]

#asc_query = [ '?00TIL00\r\n' , '?00TIL00\r']

ser = serial.Serial('COM10', timeout=1)
for baud_rate in baud_dict:
    #print("Trying baud rate of: " + str(baud_rate))
    ser.baudrate = baud_rate
    #print(ser)
    #temp_query= '?:3010:00::c2\r'
    
    for temp_query in asc_query:
        #print("Trying Query : " + str(temp_query))
        ser.write(temp_query.encode())
        sleep(3)
        read_val = ser.readline()
        print(read_val)
        if read_val:
            act_temp=read_val[18:25].decode()
            print(act_temp)
            #break
            #quit()
            print("Data at Baud rate "+ str(baud_rate) + " for query "+ str(temp_query) + str(read_val))
            print("HERE IS THE ANSWER" )
        else:
            print("No data at Baud rate "+ str(baud_rate) + " for query "+ str(temp_query))
    sleep(5)
    
ser.close()
