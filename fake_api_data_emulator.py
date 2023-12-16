import requests
import json
import random

#vessel_id = random.randint(1,20)

usage = 0.5
list = [*range(1,38,1)]

total_count = 37
empty_data_one = [random.randint(1,10),random.randint(11,20),random.randint(21,30)]
working_charts = [*range(1,35,1)]

r_id = random.randint(1,38)

data = []

for i in list:
    tempa = random.randrange(-250,-180)
    tempb = random.randrange(-200,-150)
    level = random.randint(6,10)
    if r_id == i:
        data_array = { "vessel": 0 ,"tempa": 0,"tempb": 0 ,"level":  0, "usage": 0 }
        data.append(data_array)
        #empty_data_one.append(i)
    else:
        data_array = { "vessel": i,"tempa":tempa,"tempb":tempb,"level": level, "usage": usage }
        data.append(data_array)

#print(data)


#pth_data = '[{"pth_sensor": "192.168.9.239", "temp": "232", "humidity": 10.0, "pressure": 9.4, "tempa": 10.2}, {"pth_sensor": "192.168.100.81", "temp": "25", "humidity": 20.0, "pressure": 19.7, "tempa": 5.5}]'

#print(pth_data)
    
#print("\n\n")
#print('Summery Of Connection Details ', end='\n * ')

total_count = len(list)
#print("Total vessel Count = " + str(total_count) + "\n")

d_count = len(empty_data_one)
#print(' * Downlink Count ====> ' +  str(d_count))
#print(" * Downlink Vessels" + str(empty_data_one))
#print(empty_data_one)


s_count = len(working_charts)
#print(' * Uplink Count ====> ' + str(s_count))
#print(" * Uplink Vessel" + str(working_charts))


URL = "http://localhost/lifecell/api/charts_api.php"

final_data = {'charts' : json.dumps(data),'total_vessel_count' : total_count , 'total_connected_charts': s_count ,'not_connected_charts' : json.dumps(empty_data_one) }

attempts = 3

while(attempts > 0):
        r = requests.post(url = URL, data = final_data,timeout=5)
        print(r.text)
        print(r.status_code)
        if(r.status_code == 200):
             break
        else:
            attempts -=1
            print(attempts)
            
        print("Network not reachable")

