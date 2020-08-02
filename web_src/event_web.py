import starlette.status as status
from json import JSONDecodeError
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.exceptions import HTTPException


async def events(request):
    print(request.method)
    headers = request.headers
    print(headers)
    # TODO auth based on header token
    if 'secretapitoken' in headers:  # and headers['secretapitoken'] in VAULT:
        try:
            payload = await request.json()
            print(payload)
            # TODO process request body and push event to redis queue
        except JSONDecodeError:
            print('cannot_parse_request_body')
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="cannot_parse_request_body")
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
