from django.shortcuts import render_to_response
from django.template import RequestContext
 
def index(request):
    return render_to_response('login.html', context_instance=RequestContext(request))