from  flask import g, request
import datetime

def entry_logger():
    g.time_logged = datetime.datetime.now()
    client_id = g.request_id
    method = request.method
    ip = request.remote_addr
    
    entry_info = {
            'logging_time': g.time_logged,
            'client_id': client_id,
            'method': method,
            'ip': ip
            }
    print("entry information:", entry_info)

def exit_logger(response):
    status_code = response.status_code
    duration = (datetime.datetime.now() - g.time_logged).total_seconds()
    exit_time = datetime.datetime.now()
    client_id = g.request_id

    exit_info = {
            'status_code' : status_code,
            'duration': duration,
            'exit_time': exit_time,
            'client_id': client_id
            }
    print("exit information:", exit_info)
    return response
