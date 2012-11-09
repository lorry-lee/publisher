from django.http import HttpResponse
from django.utils import simplejson

def json_response(d):
    return HttpResponse(simplejson.dumps(d), mimetype='application/javascript')
