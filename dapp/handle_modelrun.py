from django.conf import settings

import uuid, os

from thirdparty.temoa.temoa_model import temoa_model

def create_config(values):

  """
	# Input File (Mandatory). Usage: --input=<your_path_to_input_file>
  # Input can be a .db or .dat file
  # Both relative path and absolute path are accepted
  --input=/home/yash/Projects/sam/dapp/thirdparty/temoa/db_io/temoa_utopia.sqlite
  
  # Output File (Mandatory). Usage: --output=<your_path_to_output_file>
  # The output file must be a existing .db file
  --output=/home/yash/Projects/sam/dapp/thirdparty/temoa/db_io/temoa_utopia.sqlite
  
  # Scenario Name (Mandatory). Usage: --scenario=<your_scenario_name>
  # This scenario name is used to store results within the output .db file
  --scenario=test_run
  
  # Spreadsheet Output (Optional). Usage: --saveEXCEL 
  # Direct model output to a spreadsheet
  # Scenario name specified above is used to name the spreadsheet
  --saveEXCEL
  
  # Miscellaneous (Optional)
  # --how_to_cite                    # Optional, display citation info and terminate program
  # --version                        # Optional, display version info and terminate program
  # --fix_variables=fix              # Optional, path to file containing variables to fix
  
  # Solver-related arguments (Optional)
  --solver=glpk                    # Optional, indicate the solver
  --generate_solver_lp_file        # Optional, generate solver-compatible LP file
  --keep_pyomo_lp_file             # Optional, generate Pyomo-compatible LP file
  
  # Modeling-to-Generate Alternatives (Optional)
  # Run name will be automatically generated by appending '_mga_' and iteration number to scenario name
  #--mga {
  #	slack=0.1                     # Objective function slack value in MGA runs
  #	iteration=4                   # Number of MGA iterations
  #        weight=integer                # MGA objective function weighting method, currently "integer" or "normalized"
  #}
	"""
  
    
  # values is all avaiable options
  
  print values
  
  filename = "/home/yash/Projects/sam/dapp/uploads/config_temp/config_ %s" % (uuid.uuid4())
  
  with open(filename, 'a') as config_file:
    for key, value in values.iteritems():
      if value:
        config_file.write(key + '=' + value + '\n')
      else:
        config_file.write(key + '\n')
  
  
  return filename
    

def run_model(request):
  
  #print ( "this is a very %s" % ("someman")
      #"long string too"
      #"for sure ..."
    # )


  #need to create config with form post data
  if request.method == 'POST':
    
    values = {}
    
    print request.POST.get("outputdatafilename", "")
    print request.POST.get("createtextfileoption", "")

    values['--input'] = settings.UPLOADED_INPUT_DIR + request.POST.get("inputdatafilename", "")
    values['--output'] = settings.UPLOADED_OUTPUT_DIR + request.POST.get("outputdatafilename", "")
    values["--scenario"] =request.POST.get("scenarioname", "")
    values["--solver"] =request.POST.get("solver", "")
    
    if request.POST.get("createspreadsheetoption", "") :
      values['--saveEXCEL'] = ""
    
    if request.POST.get("createtextfileoption", ""):
      values['--generate_solver_lp_file'] = ""
    
    if request.POST.get("generatelpfileoption", ""):
      values["--generate_solver_lp_file"] = ""
    
    #Under construction
    runoption = request.POST.get("runoption", "")
    
    filename = create_config(values)
  
    temoa_model.runModel(filename)
    
    #Remove this temp config file
    
    #FIXME uncomment below on production 
    #os.remove(filename)
