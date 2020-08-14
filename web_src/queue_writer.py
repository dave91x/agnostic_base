import json
import time
import uuid
import redis


class QueueOperator(object):

    DRAMATIQ_DEFAULT_QUEUE = 'dramatiq:default'
    DRAMATIQ_DEF_MSG_QUEUE = 'dramatiq:default.msgs'

    def write_to_queue(self, payload):

        k = uuid.uuid4().hex
        print(k, payload)

        # process request body and push event to redis queue
        r = redis.Redis(host='redis', port=6379, db=0)
        redis_responses = []
        message_to_enqueue = {
            "queue_name": "default",
            "actor_name": "process_event",
            "args": [json.dumps(payload)],
            "kwargs": {},
            "options": {
                "redis_message_id": k
            },
            "message_id": k,
            "message_timestamp": int(round(time.time() * 1000))
        }
        redis_responses.append(r.rpush(self.DRAMATIQ_DEFAULT_QUEUE, k))
        redis_responses.append(r.hset(self.DRAMATIQ_DEF_MSG_QUEUE, k,
                                      json.dumps(message_to_enqueue, separators=(",", ":")).encode("utf-8")))

        return redis_responses
