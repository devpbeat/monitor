def response(code, status, message, data):
    return {
        "meta": {
            "code": code,
            "status": status,
            "message": message
        },
        "data": data
    }
