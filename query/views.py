from django.shortcuts import render, HttpResponse
from autocompletion import autocomplete
from django.views.decorators.csrf import csrf_exempt
import json

def index(request):
    if request.method != "GET":
        return HttpResponse("405: Method not acceptable\n")
    if len(request.GET) == 0:
        return render(request, 'query/index.html')
    elif len(request.GET) > 2:
        return HttpResponse("Invalid request\n")
    if 'Primary Key' not in request.GET or 'Secondary Keys' not in request.GET:
        return HttpResponse(request.GET.keys())

    resp = autocomplete(request.GET['Primary Key'])
    resp.extend(autocomplete(request.GET['Secondary Keys']))

    return HttpResponse(json.dumps(resp))

# REMOVE ALL ABOVE

@csrf_exempt
def complete(request):
    # if request.method != "POST":
    #     return HttpResponse("405: Method not acceptable\n")
    q = None
    if 'q' in request.POST:
        q = request.POST["q"]
    else:
        q = request.GET["q"]
    if q == None:
        return HttpResponse("Invalid request")    
    return HttpResponse(json.dumps(autocomplete(q)))
