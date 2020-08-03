import json
import time
import uuid
import redis
import starlette.status as status
from json import JSONDecodeError
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.exceptions import HTTPException


DRAMATIQ_DEFAULT_QUEUE = 'dramatiq:default'
DRAMATIQ_DEF_MSG_QUEUE = 'dramatiq:default.msgs'


async def events(request):
    print(request.method)
    headers = request.headers
    print(headers)
    # TODO auth based on header token
    if 'secretapitoken' in headers:  # and headers['secretapitoken'] in VAULT:
        try:
            payload = await request.json()
            k = uuid.uuid4().hex
            print(k, payload)
            # process request body and push event to redis queue
            r = redis.Redis(host='redis', port=6379, db=0, decode_responses=True)
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
            redis_responses.append(r.rpush(DRAMATIQ_DEFAULT_QUEUE, k))
            redis_responses.append(r.hset(DRAMATIQ_DEF_MSG_QUEUE, k,
                                          json.dumps(message_to_enqueue, separators=(",", ":")).encode("utf-8")))

            if not all(redis_responses):
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="event_failed_to_queue")
        except JSONDecodeError:
            print('cannot_parse_request_body')
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="cannot_parse_request_body")
        except redis.exceptions.ConnectionError:
            print('internal_server_connection_error')
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="internal_server_connection_error")
        except TypeError:
            print('internal_server_connection_error')
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="internal_server_connection_error")
    else:
        print('not_authorized_to_access')
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="not_authorized_to_access")
    return JSONResponse({"status": "received"})


async def http_exception(request, exc):
    return JSONResponse({"detail": exc.detail}, status_code=exc.status_code)


routes = [
    Route('/events', endpoint=events, methods=["POST"])
]

exception_handlers = {
    400: http_exception,
    403: http_exception,
    404: http_exception,
    500: http_exception
}

app = Starlette(debug=True, routes=routes, exception_handlers=exception_handlers)
