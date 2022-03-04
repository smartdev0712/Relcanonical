from django.shortcuts import render, HttpResponse, redirect

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from api.models import APIEntry
# from api.forms import FileForm


@csrf_exempt
def getAPI(request,category,endpoint,param=None):
        
    if request.method == "POST":
        endpoint = endpoint.replace("_", " ")
        primary_keys = request.POST["primary_keys"]
        secondary_keys = request.POST["secondary_keys"]
        category = request.POST["category"]
        category =category.replace("_"," ")
        secondary_keys = [k.strip() for k in secondary_keys.split(',')]
        primary_keys = [p.strip() for p in primary_keys.split(',')]
        csv_file = request.FILES['endpoint_file']
        if not csv_file.name.endswith('.csv'):
    	    return JsonResponse({"error": 'File is not CSV type'})
        
        dbEntry = APIEntry(endpoint=endpoint, primary_keys=",".join(primary_keys),secondary_keys=",".join(secondary_keys),category=category.strip(), file = csv_file)
        dbEntry.save()
        d = []
        for p in primary_keys:
            array = {"name": p}
            for k in secondary_keys:
                array[k] = p+" "+k
            d.append(array)
        return JsonResponse(d,safe=False)

    endpoint = endpoint.replace("_", " ")
    category = category.replace("_"," ")

    
    try:
        endpointObj = APIEntry.objects.filter(endpoint=endpoint,category=category)
        
        if endpointObj == None or len(endpointObj) == 0:
            return JsonResponse({"error":"endpoint not found"})
        endpointObj = endpointObj[0]
        primary_keys = endpointObj.primary_keys.split(",")
        # print(primary_keys)
        secondary_keys = endpointObj.secondary_keys.split(",")
        # print(secondary_keys)

    

        d = []
        for p in primary_keys:
            query= request.GET.items()
            
            
            keys = {"name": p}
            for k in secondary_keys:
                keys[k] = p+" "+k
            
            if bool(query):
                allow = True
                for k,v in query:
                    if p != v:
                        allow = False
                if not allow:
                    continue
            
            if not param == None:
                d.append({param:keys[param]})
            else:
                d.append(keys)
        
            
        return JsonResponse(d,safe=False)        
    except Exception as e:

        return JsonResponse({"error":e.__str__()})


    return JsonResponse({"ok":True})

def index(request):
    return render(request, 'api/index.html')

def documentation(request):
    return render(request, 'api/documentation.html')

def generate(request):
    return render(request, 'api/generate.html')

# def fileUpload(request):
#     if request.method == 'POST':
#         form = FileForm(request.POST, request.FILES)
#         if form.is_valid():
#             newfile = File(file = request.FILES['endpoint_file'])
#             newfile.save()

#             return redirect('fileUpload')
#     else:
#         form = FileForm()

#     files = File.objects.all()
    
#     # context = {'files': files, 'form': form}
#     # return render(request, 'api/generate.html', context)
#     return JsonResponse(files,safe=False)
