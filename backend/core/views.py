from django.http import HttpResponseNotFound
import json

def error404(request, exception):
    response_data = {}
    response_data['meta'] = {
        'status': 'error',
        'code': 404,
        'message': 'Not Found',
    }
    return HttpResponseNotFound(json.dumps(response_data), content_type="application/json")