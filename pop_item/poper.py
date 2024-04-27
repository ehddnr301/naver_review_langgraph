# code for pop redis list from restaurant_list
import time
import random

import redis

r = redis.Redis(host="redis", port=6379, password="pseudolab", decode_responses=True)

while True:
    poped_item = r.rpop("restaurant_list")

    if poped_item:
        r.rpush("poped_list", poped_item)

    time.sleep(random.randint(60, 120))
