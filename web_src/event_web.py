import redis
from json import JSONDecodeError
import starlette.status as status
from starlette.routing import Route
from queue_writer import QueueOperator
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.exceptions import HTTPException


async def events(request):
    headers = request.headers
    # TODO auth based on header token
    if 'secretapitoken' in headers:  # and headers['secretapitoken'] in VAULT:
        try:
            payload = await request.json()
            redis_responses = QueueOperator().write_to_queue(payload)
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
