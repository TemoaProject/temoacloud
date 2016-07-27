#Django
from django.template import RequestContext
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django import forms
from django.views.decorators.csrf import csrf_exempt

#System
import json
import os
import re
import urllib
import json
import os
import uuid 
import shutil

#Custom / Thirdparty
from thirdparty import test
from thirdparty.temoa.db_io import Make_Graphviz
from handle_modelrun import run_model
from thirdparty.temoa.temoa_model import get_comm_tech

def login(request):
  return render_to_response('login.html', context_instance=RequestContext(request))

def inputData(request):

  random = str(uuid.uuid4().get_hex().upper()[0:6])

  return render_to_response('InputData.html', { 'mode' : 'input' , 'random' : random,  'title' : 'Input Data'}, context_instance=RequestContext(request))

def outputData(request):
  return render_to_response('InputData.html', { 'mode' : 'output' , 'title' : 'Output Data'}, context_instance=RequestContext(request))

def modelRun(request):
  return render_to_response('ModelRun.html', { 'title' : 'Model Run'} , context_instance=RequestContext(request))

def runModel(request):
  
  msg = 'Successfully generated'
  result = True
  generatedfolderpath = ''
  zip_path = ''
  
  try:
    #This function will handle 
    #TODO try catch handling
    generatedfolderpath = run_model(request)
    
    #if not generatedfolderpath:
    #  raise "Error detected"
    
    
    random = str(uuid.uuid4().get_hex().upper()[0:6])
    output_dirname = 'db_io/db_io_' + random 
    #print "Zipping: " + settings.BASE_DIR + "/" + generatedfolderpath + " | " + output_dirname
    shutil.make_archive( 'result/' + output_dirname , 'zip', settings.BASE_DIR + "/" + generatedfolderpath)
    
    zip_path = output_dirname + ".zip"
  
  
  except:
    msg = 'An error occured. Please try again.'
    result = False
  
  
  return JsonResponse( {"result" : result , "message" : msg , 'zip_path' : zip_path  } )


def index(request):
  return HttpResponse("Nothing for now...")


def about(request):
  return render_to_response('About-Us.html', context_instance=RequestContext(request))


#get posted data
def runInput(request):
  
  if request.method != 'POST':
    return HttpResponse("Use post method only", status = 403)
  
  
  format = request.POST.get("format", "svg")
  colorscheme = request.POST.get("colorscheme", "color")
  type =request.POST.get("commodity-technology-type", "")
  value =request.POST.get("commodity-technology-value", "")
  filename =request.POST.get("datafile", "")
  mode =request.POST.get("mode", "")

  random =request.POST.get("scenario-name", "")
  
  folder, file_extension = os.path.splitext(filename)
  
  
  imagepath = ""
    
  #fulldirpath = os.path.dirname(os.path.abspath(__file__))
  #print settings.BASE_DIR
  #filename = "/home/yash/Projects/dapp/thirdparty/temoa/db_io/temoa_utopia.sqlite"
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
    
  inputs = { 
            "-i" : settings.BASE_DIR + "/uploads/uploaded/" + mode + "/" + filename , 
            "-f" : format,
            "-o" : settings.BASE_DIR + "/result/" + mode
  }
          
  if( colorscheme == "grey"):
    inputs['-g'] = colorscheme
    
    

  if mode == "input":
    
    inputs["-n"]= random
    
    imagepath = folder + "_" + random + "/" + folder + "_" + random + ".svg"

  elif mode == "output":

    inputs["--scenario"] = random

    imagepath = folder + "_" + random + "/simple_model.svg"

    
  if type == 'commodity':
  
    inputs["--comm"] = value
    imagepath = folder + "_" + random + "/commodities/commodity_" + value + ".svg" if mode == "output" else folder + "_" + random + "/" + folder + "_" + random + ".svg"
    

  elif type == 'technology':
  
    inputs["--tech"] = value
    #imagepath = 
    imagepath = folder + "_" + random + "/processes/process_" + value + ".svg" if mode == "output" else folder + "_" + random + "/" + folder + "_" + random + ".svg"
    
  print inputs

  output_dirname = inputs['-o']+"/"+folder + "_" + random
  #remove existing folder
  
  
  error = ''
  try:  
    
    shutil.rmtree(output_dirname, ignore_errors=True)
  
    makeGraph(inputs)
  except:
    error = 'An error occured. Please try again.'
    

  print "Zipping: " + output_dirname
  shutil.make_archive(folder + "_" + random , 'zip', output_dirname)
  
  zip_file = mode + "/" + folder + "_" + random + ".zip"

    
  return JsonResponse( {"error" : error, "filename" : imagepath , "zip_path": zip_file, "folder" : folder + "_" + random , "mode" : mode , } )
    
    
  

# Create your views here.
def makeGraph(inputs):
  return Make_Graphviz.createGraphBasedOnInput(inputs)


@csrf_exempt
def fileUpload(request):
    
  if request.method == 'POST':
    mode = request.POST.get("mode", "input")
    

    result = handle_uploaded_file( request.FILES['file'],  mode)
    
    #if string is empty we have no errors hence success
    if not result :
      #fileList = loadFiles()
      #JsonResponse( {'success' : 'File uploading finished'} )

      return JsonResponse( {"data" : loadFiles(mode), 'mode' : mode })
      
    
    return JsonResponse({'error': result}, status = 403)

def handle_uploaded_file(f, mode):
  import os.path
  
  
  fname = settings.BASE_DIR + '/uploads/uploaded/'+mode+'/' + f.name
  
  
  filename, file_extension = os.path.splitext(f.name)
  #print(fname)
  #print file_extension
  
  if file_extension != ".data" and file_extension != ".sqlite" :
    return "Please select a valid file. Supported files are data and sqlite"
     
  
  if(os.path.isfile(fname) ):
    #print "Testing" + fname
    return "File already exists. Please rename and try to upload."
  
  with open(fname, 'wb+') as destination:
    for chunk in f.chunks():
      destination.write(chunk)
  
  return "";


def loadFileList(request):
  mode = request.GET.get('mode','input')
  fileList = { "data" : loadFiles(mode) }
  return JsonResponse(fileList)

def loadFiles(mode):
  #print mode
  types = ('.data', '.sqlite') # the tuple of file types
  
  return [each for each in os.listdir(settings.BASE_DIR + '/uploads/uploaded/'+ mode) if each.endswith(types)]
  


def loadCTList(request):
  mode = request.GET.get('mode','input')
  filename = request.GET.get('filename')
  listType = request.GET.get('type','')
  
  input = {"--input" : settings.BASE_DIR + '/uploads/uploaded/'+ mode + "/" + filename}
  
  if listType == 'commodity':
    input["--comm"] = True

  elif listType == 'technology':
    input["--tech"] = True

  elif listType == 'scenario':
    input["--scenario"] = True
  
  elif listType == 'date':
    input["--date"] = True  
    
  error = ''  
  data = {}
  
  try:
    data = get_comm_tech.get_info(input)
  except:
    error = 'An error occured. Please try again.'  
    
    #FIXME remove this when we get scenerios from tables
    #return JsonResponse( { "data" : {"Test1" : "Test1" , "Test2" : "Test2"} } )
  
  return JsonResponse( { "data" : data , "error" : error } )
