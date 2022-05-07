import requests
import time

CONFIG_API_URL = 'http://127.0.0.1:8000/get/config/'
CURRENT_TEMP_API_URL = 'http://localhost:8000/temperature/current/'

header_params = {'Content-type': 'application/json', 
                 'user-id': "e924683f-6b50-4047-92ed-c314ecc4ac46", 
		 'vivint-unit-id': "d4eac273-326b-41cd-b996-0cd4a9df73ce"
		 } 

def update_config():
  #fetch the target temperature 
  response = requests.get(url=CONFIG_API_URL, headers=header_params, verify=False)
  config = response.json()
  target_temp = config['target_temp']
  current_temp = config['current_temp']
  state = config['state']
  fan = config['fan']
 
  if target_temp >= current_temp:
     state = 1 #heating
     while current_temp < target_temp:
        time.sleep(5) #simulate heating..
        current_temp += 1
  else:
     state = 0 #cooling
     while current_temp > target_temp:
        time.sleep(5) #simulate cooling..
        current_temp -= 1
  print(target_temp, current_temp, state, fan)

update_config()





