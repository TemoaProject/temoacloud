from django.shortcuts import render
from django.http import HttpResponse
from thirdparty import test
from thirdparty.temoa.db_io import Make_Graphviz

# Create your views here.
def index(request):
  print test.tryme()
  
  #So we have to pass inputs to Make_Graphviz to generate graph
  #After getting response run a ajax call to get that
  
  inputs = {  }
  
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

