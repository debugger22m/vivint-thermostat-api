import random
import json
import uuid
import pprint

class GenerateData:
      
   def init(limit):
     fan = ['on', 'off', 'auto']
     state = ['actively cooling', 'actively heating']
     user_ids = {}
     
     for i in range(limit):
       unit_ids = {}
       for j in range(random.randint(0, 4)):
          config = {}
          config['max_temp'] = random.randint(25, 125)
          config['max_temp'] = random.randint(25, 125)
          config['target_temp'] = random.randint(50, 100)
          config['current_temp'] = random.randint(50, 80)
          config['fan'] = fan[random.randint(0, len(fan) - 1 )]
          config['state'] = state[random.randint(0, len(state) - 1)]
          unit_ids[str(uuid.uuid4())] = config
      
       user_ids[str(uuid.uuid4())] = unit_ids
     return user_ids

#pp = pprint.PrettyPrinter(indent=2)
#pp.pprint(GenerateData.init(4))

