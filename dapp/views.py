from django.template import RequestContext
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, JsonResponse
from thirdparty import test
import json
import os
import re
import urllib
import json
from django.conf import settings


from django import forms

from django.views.decorators.csrf import csrf_exempt
#from .forms import UploadFileForm
#from .models import ModelWithFileField

from thirdparty.temoa.db_io import Make_Graphviz
#from thirdparty.temoa.temoa_model import temoa_model


import os

def login(request):
  return render_to_response('login.html', context_instance=RequestContext(request))

def inputData(request):
  return render_to_response('InputData.html', context_instance=RequestContext(request))

def outputData(request):
  return render_to_response('OutputData.html', context_instance=RequestContext(request))

def modelRun(request):
  return render_to_response('ModelRun.html', context_instance=RequestContext(request))

def runModel(request):
  
  #temoa_model.runModel()
  
  return HttpResponse("Generating model...")


def index(request):
  
  return HttpResponse("Nothing for now...")


def about(request):
  return render_to_response('About-Us.html', context_instance=RequestContext(request))

#@csrf_exempt
#def fileUpload(request):
#  upload_file(request)
#  return HttpResponse("File uploaded result")


#get posted data
def runInput(request):
  if request.method == 'POST':
    format = request.POST.get("format", "svg")
    colorscheme = request.POST.get("colorscheme", "color")
    commodityoutputlimit =request.POST.get("commodityoutputlimit", "")
    commodityinputlimit =request.POST.get("commodityinputlimit", "")
    filename =request.POST.get("datafile", "")
    
    #fulldirpath = os.path.dirname(os.path.abspath(__file__))
    
    #print settings.BASE_DIR
    
    #filename = "/home/yash/Projects/dapp/thirdparty/temoa/db_io/temoa_utopia.sqlite"
    
    inputs = { 
            "-i" : settings.BASE_DIR + "/uploads/input/" + filename , 
            "-f" : "svg",
            "--scenario" : "sname" ,
            "-o" : "result"
          }
          
    if( colorscheme == "grey"):
      inputs['-g'] = colorscheme
    
    print inputs
    
    makeGraph(inputs)
    
    return HttpResponse("Running... :)")
    
    
  

# Create your views here.
def makeGraph(inputs):
  #print test.tryme()
  
  #So we have to pass inputs to Make_Graphviz to generate graph
  #After getting response run a ajax call to get that
  
  
  
  
  
  Make_Graphviz.createGraphBasedOnInput(inputs)
  
  
  #expected result
  # image svg now fetch and show result
  #print "result/%s/" %( os.path.splitext(os.path.basename(filename))[0] )
  
  
  
  
  #if opt in ("-i", "input"):
    #ifile = arg
  #elif opt in ("-f", "--format"):
    #graph_format = arg
  #elif opt in ("-c", "--show_capacity"):
    #show_capacity = True
  #elif opt in ("-v", "--splinevar") :
    #splinevar = True
  #elif opt in ("-t", "--graph_type") :
    #graph_type = arg
  #elif opt in ("-s", "--scenario") :
    #scenario = arg
  #elif opt in ("-n", "--name") :
    #quick_name = arg
  #elif opt in ("-o", "--output") :
    #res_dir = arg
  #elif opt in ("-g", "--grey") :
  
  
  
  return HttpResponse("Index SSS") 


@csrf_exempt
def fileUpload(request):
    
  if request.method == 'POST':
    
    
    

    result = handle_uploaded_file( request.FILES['file'] )
    
    #if string is empty we have no errors hence success
    if not result :
      #fileList = loadFiles()
      #JsonResponse( {'success' : 'File uploading finished'} )

      return JsonResponse( {"data" : loadFiles() })
      
    
    return JsonResponse({'error': result}, status = 403)

def handle_uploaded_file(f):
  import os.path
  
  
  fname = 'uploads/input/' + f.name
  
  
  filename, file_extension = os.path.splitext(f.name)
  print(fname)
  print file_extension
  
  if file_extension != ".data" and file_extension != ".sqlite" :
    return "Please select a valid file. Supported files are data and sqlite"
     
  
  if(os.path.isfile(fname) ):
    print "Testing" + fname
    return "File already exists. Please rename and try to upload."
  
  with open('uploads/input/' + f.name, 'wb+') as destination:
    for chunk in f.chunks():
      destination.write(chunk)
  
  return "";


def loadFileList(request):
  fileList = { "data" : loadFiles() }
  return JsonResponse(fileList)

def loadFiles():
  import glob   
  #print glob.glob("upload/adam/*.txt")
  types = ('*.data', '*.sqlite') # the tuple of file types
  files_grabbed = []
  for type in types:
      files_grabbed.extend(glob.glob('uploads/input/' + type))
  fileList = []

  for file in files_grabbed:
    fileList.append(os.path.basename(file))

  return fileList;

    

