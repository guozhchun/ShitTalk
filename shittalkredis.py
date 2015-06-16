#coding=utf-8
import redis

def redis_write(room,content):   
	key = room
	val = content  
	r = redis.StrictRedis(host='127.0.0.1',port=6379)  
	r.sadd(key,val)  

		
def redis_read(room):  

    key = room  
    r = redis.StrictRedis(host='127.0.0.1',port=6379)  
    value = r.smembers(key)
    for i in value:
        print i.encode('utf-8')  
	print value
    return value  

	
def redis_clean():
    r = redis.StrictRedis(host='127.0.0.1',port=6379)
    r.flushdb()