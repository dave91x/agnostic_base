import time
import dramatiq
from dramatiq.brokers.redis import RedisBroker


redis_broker = RedisBroker(host="redis", port=6379, db=0, decode_responses=True)
dramatiq.set_broker(redis_broker)

@dramatiq.actor
def process_event(event):
    print('picked up event:  {}'.format(event))
    time.sleep(5)
    print('processed event:  {}'.format(event))
