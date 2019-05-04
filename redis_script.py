import redis
from itertools import zip_longest
import json

class redis_cache:



    def __init__(self):

        
        self.r = self.set_redis_connection()
    def batcher(self,iterable, n):
        args = [iter(iterable)] * n
        return zip_longest(*args)


    def clean_redis_cache(self):
        for keybatch in self.r.scan_iter():
            self.r.delete(keybatch)



    def set_redis_connection(self):

        

        r = redis.Redis(
            host='localhost',
            port=6379)

        return r


    def set_redis(self,data_dict,dict_id):
        
        rval = json.dumps(data_dict)     
        self.clean_redis_cache()
        
        self.r.set(dict_id,rval)
    
                    
    def get_redis(self,dict_id):
        new_data = self.r.get(dict_id)

        new_data = json.loads(new_data)            

        return new_data

















