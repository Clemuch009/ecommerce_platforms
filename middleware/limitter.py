from flask import request, abort
import datetime

visit_counter = {}

def rate_limiter():
    maxima = 5
    window_time  = 60
    client_ip = request.remote_addr
    
    now = datetime.datetime.now()

    if client_ip not in visit_counter:
        visit_counter[client_ip] = [0, now]

    arr = visit_counter[client_ip]
    elapsed = (now - arr[1]).total_seconds()

    if elapsed > window_time:
        arr[0] = 0
        arr[1] = now

    if arr[0] >= maxima:
        abort(429, description='Rate limit exceeded: max 5 requests per hour')
    
    arr[0] += 1
    
