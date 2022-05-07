# vivint-thermostat-api

Design and implement an API for a simple cloud-based service to control customer thermostats.

The user of the API should be able to

GET the current actual temperature.

GET and SET the temperature set points, i.e., set the desired heating/cooling target temperature.

GET and SET the state of the thermostat, i.e., actively heating/cooling, fan on/off/auto, etc.

Bonus stretch goal:  If you have time and interest, it would be fun to have the current actual temperature respond slowly to the state and temperature set-point(s) of the thermostat.

-------------------------------------------------
The API is build using fastapi python framework. 

To start the service, type **fastapi run** or **uvicorn app.main:app --reload** and go to **http://127.0.0.1:8000/docs**


All APIs require user-id and vivint-unit-id to be passed in the header. It could have been part of the URI as well and be passed as a parameter. But I don't wanted to expose the IDs in the params and since indeployment all the routes will be SSL it will be good have it the header for better security.


**Data Model**
I created a helper class to generate random data set for thermostat. When the API server boots up, the data set is generated. So, we can test our APIs.

  "a30a4727-ab30-4279-91f6-e2f0cb0d2856": { //user-id. Unique identifier for a user. I used UUID for this.
    "852d3f4d-f459-4f4b-a11b-f8b34132d1e8": { //vivint-thermostat-id. Unique identifier for each device belonging to a user. A customer can have multiple devices.
      "max_temp": 121,
      "target_temp": 70,
      "current_temp": 73,
      "fan": "off",
      "state": "actively cooling"
    }
  }

I created these mappings for the PUT APIs. So we don't need to send string values in JSON. We can just map it to int. However, I have generated those in strings in the data set, because I can easily identify it. But in case of APIs I thought just sending int values will be ok. 

thermostat_state = {0: "actively cooling", 1: "actively heating"}
thermostat_fan_mode = {0 : "off", 1 : "on", 2 : "auto"}

<img width="740" alt="Screen Shot 2022-05-06 at 9 38 17 PM" src="https://user-images.githubusercontent.com/21069692/167236670-1339742e-03aa-44f3-be75-08d0eab4d40f.png">


**How can we improve this API**

- **Security:** Each API requests needs to be authenticated. The security token issued by the AUTH service should be validated. For example if we are using JWT token for validating requests and authorization, we will need to set timeouts and do not store these tokens anywhere. The USER/Client needs to re auth after some time again. Verify and discard header options. The API should be using secure headers to prevent attacks like cross-site scripting(XSS)

- **Rate Limiting:** Prevent against DDoS and rogue clients trying to connect to the API service. 

- **Proper HTTP status codes:** We will need better error handling and proper HTTP status code for the client/user of the API to response according to the status codes. For example 429 for exceeding quota and 401 for auth related requests.

- **SSL:** All the endpoints should be SSL. We could have the service running behind an Ngnix service and it can do the SSL termination and have reverse proxy to the service. But all the public facing APIs should be SSL

- **Strict JSON**: Payload verification should be important. All malformed data should be logged and discarded, so its not adding noise to the data storage.

- **Error handling:** Right now the API would throw Internal Server Error, if the user-id in the request in not present. I think proper error handling is required, so that the API doesn't crashes. Also, it gives proper error messages back to the user, like saying "User-id not found". 

- **Performance:** We could deploy the API on ECS and have a AWS load balancer. Have it auto scale and the requests can be load balanced depending on the amount of traffic.

- **Tests**: We should implement test cases. Unit and performance testing should be done on the each API routes.


**Vivint Thermostat APIs**
The API requires the user-id and vivint-unit-id in the header. 

**GET the current temperature**
http://localhost:8000/temperature/current/

curl -X 'GET' \
  'http://localhost:8000/temperature/current/' \
  -H 'accept: application/json' \
  -H 'user-id: 874b1021-7be6-473f-a1af-23ae068ee14f' \
  -H 'vivint-unit-id: 3476f1ed-64ad-43c5-b194-bd238e899533'

**GET the target temperature**
http://localhost:8000/temperature/target

curl -X 'GET' \
  'http://localhost:8000/temperature/target' \
  -H 'accept: application/json' \
  -H 'user-id: 874b1021-7be6-473f-a1af-23ae068ee14f' \
  -H 'vivint-unit-id: 3476f1ed-64ad-43c5-b194-bd238e899533'

**GET current state**
http://localhost:8000/state/

curl -X 'GET' \
  'http://localhost:8000/state/' \
  -H 'accept: application/json' \
  -H 'user-id: 874b1021-7be6-473f-a1af-23ae068ee14f' \
  -H 'vivint-unit-id: 3476f1ed-64ad-43c5-b194-bd238e899533'

**GET Fan Mode**
http://localhost:8000/fan/

curl -X 'GET' \
  'http://localhost:8000/fan/' \
  -H 'accept: application/json' \
  -H 'user-id: 874b1021-7be6-473f-a1af-23ae068ee14f' \
  -H 'vivint-unit-id: 3476f1ed-64ad-43c5-b194-bd238e899533'

**SET current temperature**
http://localhost:8000/temperature/current/<temperature>

curl -X 'PUT' \
  'http://localhost:8000/temperature/current/55' \
  -H 'accept: */*' \
  -H 'user-id: 874b1021-7be6-473f-a1af-23ae068ee14f' \
  -H 'vivint-unit-id: 3476f1ed-64ad-43c5-b194-bd238e899533'

**SET target temperature**
http://localhost:8000/temperature/target/<temperature>

curl -X 'PUT' \
  'http://localhost:8000/temperature/target/73' \
  -H 'accept: */*' \
  -H 'user-id: 874b1021-7be6-473f-a1af-23ae068ee14f' \
  -H 'vivint-unit-id: 3476f1ed-64ad-43c5-b194-bd238e899533'  

**SET current state**
http://localhost:8000/state/<0/1>

curl -X 'PUT' \
  'http://localhost:8000/state/0' \
  -H 'accept: application/json' \
  -H 'user-id: 874b1021-7be6-473f-a1af-23ae068ee14f' \
  -H 'vivint-unit-id: 3476f1ed-64ad-43c5-b194-bd238e899533'

**SET FAN mode**
http://localhost:8000/fan/<0/1/2>

curl -X 'PUT' \
  'http://localhost:8000/fan/2' \
  -H 'accept: application/json' \
  -H 'user-id: 874b1021-7be6-473f-a1af-23ae068ee14f' \
  -H 'vivint-unit-id: 3476f1ed-64ad-43c5-b194-bd238e899533'

**Bonus Goal**

I tried working on a thermostat client to simulate heating and cooling. The client fetches the config from the thermostat API and try to heat or cool depending on the target and current temp. It also updates the current temp back to the API. 

**Warning** Since, all the data set is loaded in memory. We need to hardcode the user-id and vivint-unit-id from the dataset. We could just read it from the API and use it as well. 



