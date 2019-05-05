import redis
from itertools import zip_longest
import json

class redis_cache:



    def __init__(self):

        
        self.r = self.set_redis_connection()
    def batcher(self,iterable, n):
        args = [iter(iterable)] * n
        return zip_longest(*args)


    def clean_redis_cache(self,dict_id):
        for keybatch in self.r.scan_iter(match=dict_id):
            self.r.delete(keybatch)



    def set_redis_connection(self):

        

        r = redis.Redis(
            host='localhost',
            port=6379)

        return r


    def set_redis(self,data_dict,dict_id):
        
        rval = json.dumps(data_dict)     
        self.clean_redis_cache(dict_id)
        
        self.r.set(dict_id,rval)
    
                    
    def get_redis(self,dict_id):
        new_data = self.r.get(dict_id)

        new_data = json.loads(new_data)            

        return new_data




if __name__ == '__main__':




    dict1 = {"Hello":2,"Nll":3}

    r = redis_cache()

   # r.set_redis(dict1,"A")


    
    n = r.get_redis("A")
    n = r.get_redis("b")

    print (n)












