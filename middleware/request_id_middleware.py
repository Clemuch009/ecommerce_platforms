import uuid
from flask import request, g

def set_request_id():
    header_id = request.headers.get('X-Request-ID')
    if header_id:
        g.request_id = header_id
    else:
       g.request_id = str(uuid.uuid4())

def attach_id(response):
    if hasattr(g, 'request_id'):
        response.headers['X-Request-ID'] = g.request_id
    return response
