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
from datetime import datetime
from os import path

#Custom / Thirdparty
from thirdparty import test
from thirdparty.temoa.db_io import Make_Graphviz
from handle_modelrun import run_model
from thirdparty.temoa.temoa_model import get_comm_tech

from thirdparty.temoa.db_io.db_query import get_flags
from thirdparty.temoa.db_io.MakeOutputPlots import OutputPlotGenerator

def login(request):
  return render_to_response('login.html', context_instance=RequestContext(request))

def inputData(request):

  random = str(uuid.uuid4().get_hex().upper()[0:6])

  return render_to_response('InputData.html', { 'mode' : 'input' , 'random' : random,  'title' : 'Input Data'}, context_instance=RequestContext(request))

def outputData(request):
  return render_to_response('InputData.html', { 'mode' : 'output' , 'title' : 'Output Data'}, context_instance=RequestContext(request))

def modelRun(request):
  return render_to_response('ModelRun.html', { 'title' : 'Model Run'} , context_instance=RequestContext(request))

def index(request):
  return render_to_response('About-Us.html', context_instance=RequestContext(request))

def about(request):
  return render_to_response('About-Us.html', context_instance=RequestContext(request))

def _getLog():
  originalLogFile = settings.RESULT_DIR +  "debug_logs/Complete_OutputLog.log"
  archiveLogFile = settings.RESULT_DIR + "debug_logs/OutputLog__"+str(datetime.now().date()) + "__" +str(datetime.now().time())+".log"

  file = open(originalLogFile, 'r')

  if not file:
    return "Log not found or created"

  output = file.read()

  #Maintain archive of current log file
  fileArch = open(archiveLogFile, "w")
  fileArch.write(output)

  return output


def runModel(request):
  
  msg = 'Successfully generated'
  result = True
  generatedfolderpath = ''
  zip_path = ''
  outputFilename = request.POST.get("outputdatafilename")
  
  #try:
    #This function will handle 
    #TODO try catch handling
  generatedfolderpath = run_model(request)
  
  #if not generatedfolderpath:
  #  raise "Error detected"
  zip_path = ""
  
  if outputFilename:
    random = str(uuid.uuid4().get_hex().upper()[0:6])
    output_dirname = 'db_io/db_io_' + random 
    #print "Zipping: " + settings.BASE_DIR + "/" + generatedfolderpath + " | " + output_dirname
    if path.exists(generatedfolderpath):
      shutil.make_archive( settings.RESULT_DIR + output_dirname , 'zip', generatedfolderpath)
    
      zip_path = output_dirname + ".zip"
      
    else:
      msg = "Failed to generate"
  
  #except:
  #  msg = 'An error occured. Please try again.'
  #  result = False
  
    return JsonResponse( {"result" : result , "message" : msg , 'zip_path' : zip_path, "output" : _getLog()  } )


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
  dateRange =request.POST.get("date-range", "")
  
  folder, file_extension = os.path.splitext(filename)
  
  
  imagepath = ""
    
  inputs = { 
            "-i" : settings.UPLOADED_DIR + filename , 
            "-f" : format,
            "-o" : settings.RESULT_DIR  + mode,
  }
          
  if( colorscheme == "grey"):
    inputs['-g'] = None

  if mode == "input":
    inputs["-n"]= random
  elif mode == "output":
    inputs["--scenario"] = random
    inputs["--year"] = dateRange
    
  if type == 'commodity':
    inputs["--comm"] = value
  elif type == 'technology':
    inputs["--tech"] = value
    
  print inputs

  
  error = ''
  try:
    imagepath = Make_Graphviz.createGraphBasedOnInput(inputs)
    full_path = os.path.join(settings.RESULT_DIR, mode, imagepath)

    print "output_file_path = ", imagepath
    if not path.exists(full_path):
      error = "The selected technology or commodity doesn't exist for selected period"
  except:
    error = 'An error occured. Please try again.'
  
  output_folder_name = imagepath.split('/')[0]
  output_dirname = inputs['-o'] + "/" + output_folder_name
  
  zip_file = ""
  
  if path.exists(output_dirname) :
    print "Zipping: " + output_dirname
    zip_file = mode + "/" + output_folder_name+'/'+output_folder_name + ".zip"
    zip_file_path = os.path.join(settings.RESULT_DIR, zip_file)

    if (os.path.exists(zip_file_path)):
      os.remove(zip_file_path)
    shutil.make_archive(output_folder_name, 'zip', output_dirname)
    
  else:
    error = "Result folders are missing" + output_dirname


  return JsonResponse( 
        {
          "error" : error, 
          "filename" : imagepath , 
          "zip_path": zip_file, 
          "folder" : output_folder_name , 
          "mode" : mode 
          } )
    
 
def dbQuery(request):

  inputs = {}

  inputs["--query"] = request.POST['query']
  inputs["--input"] = request.POST['input']

  result = get_flags(inputs)

  return  JsonResponse( {"result" : result })


@csrf_exempt
def fileUpload(request):
    
  if request.method == 'POST':
    mode = request.POST.get("mode", "input")
    overwrite = request.POST.get("isOverwrite", False)
    
    #print("overwrite", overwrite )
    result = handle_uploaded_file( request.FILES['file'],  mode, overwrite)
    
    #if string is empty we have no errors hence success
    if not result :
      #fileList = loadFiles()
      #JsonResponse( {'success' : 'File uploading finished'} )

      return JsonResponse( {"data" : loadFiles(), 'mode' : mode })
      
    
    return JsonResponse({'error': result}, status = 403)

def handle_uploaded_file(f, mode, overwrite):
  import os.path
  
  
  fname = settings.UPLOADED_DIR  + f.name
  
  
  filename, file_extension = os.path.splitext(f.name)
  #print(fname)
  #print file_extension
  
  if file_extension != ".data" and file_extension != ".sqlite" and file_extension != ".dat" :
    return "Please select a valid file. Supported files are data and sqlite"
     
  
  if(os.path.isfile(fname) ):
    
    if int(overwrite) <> 0:
      #print("isOverwrite 2", overwrite )
      try:
        os.remove(fname)
      except OSError as e: # name the Exception `e`
        #print "Failed with:", e.strerror # look what it says
        #print "Error code:", e.code 
        return "File already exists and failed to overwrite. Reason is {0}. Please try again.".format(e.strerror)
    else: 
      #print("isOverwrite 3", overwrite )
      #print "Testing" + fname
      return "File already exists. Please rename and try to upload."
  
  with open(fname, 'wb+') as destination:
    for chunk in f.chunks():
      destination.write(chunk)
  
  return "";


def loadFileList(request):
  #mode = request.GET.get('mode','input')
  fileList = { "data" : loadFiles() }
  return JsonResponse(fileList)

def loadFiles():
  #print mode
  types = ('.data', '.sqlite', '.sqlite3', '.dat') # the tuple of file types
  
  return [each for each in os.listdir(settings.UPLOADED_DIR) if each.endswith(types)]
  
def loadsector(request):
  filename = request.GET.get('filename')
  scenario = request.GET.get("scenario")
  plottype = int(request.GET.get('plottype', '1'))
  db_path = settings.UPLOADED_DIR + filename

  sectors =[]
  error = ''
  try:
    res = OutputPlotGenerator(db_path, scenario)
    sectors = res.getSectors(plottype)
  except:
    error = 'Database file not supported: ' +db_path

  return JsonResponse({"data" : sectors, "error": error})

def generateplot(request):
  filename =request.POST.get("db-plot-datafilename", "")
  scenario = request.POST.get("plot-scenario-name", "")
  plottype = int(request.POST.get("plot-type-name", "1"))
  sector =request.POST.get("sector-type-name", "")
  supercategories = request.POST.get("merge-tech", False)

  db_path = settings.UPLOADED_DIR + filename

  image_path_dir = settings.RESULT_DIR + 'matplot/'
  res = OutputPlotGenerator(db_path, scenario)

  plotpath = 'result/matplot/'
  error = ""
  try:
    if (plottype == 1):
      plotpath += res.generatePlotForCapacity(sector, supercategories, image_path_dir)
    elif (plottype == 2):
      plotpath += res.generatePlotForOutputFlow(sector, supercategories, image_path_dir)
    elif (plottype == 3):
      plotpath += res.generatePlotForEmissions(sector, supercategories, image_path_dir)
  except Exception as e:
    plotpath = ""
    error = "An error occured. Please try again in some time."
  

  return JsonResponse({"data" : plotpath, "error": error})


def loadCTList(request):
  error = ''  
  data = {}

  mode = request.GET.get('mode','input')
  filename = request.GET.get('filename')
  listType = request.GET.get('type','')
  scenarioName = request.GET.get('scenario-name','')
  
  input = {"--input" : settings.UPLOADED_DIR + filename}
  
  _, fext = os.path.splitext(filename)
  if mode == "output" and fext == '.dat':
    error = "For output, only database files supported (.sqlite)"
    return JsonResponse( { "data" : data , "error" : error } )

  if listType == 'commodity':
    input["--comm"] = True

  elif listType == 'technology':
    input["--tech"] = True

  elif listType == 'scenario':
    input["--scenario"] = True
  
  elif listType == 'period':
    input["--period"] = True  
    
  try:
    data = get_comm_tech.get_info(input)
  except:
    error = 'An error occured. Please try again.'  
      
  
  return JsonResponse( { "data" : data , "error" : error } )
