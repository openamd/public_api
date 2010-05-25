# Create your views here.
from django.http import HttpResponse
import simplejson as json

def index(request):
    return HttpResponse(json.dumps({"greeting" : "Hello, world. You're at the location page"}),
			mimetype='text/plain')
