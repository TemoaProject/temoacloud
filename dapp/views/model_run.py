# Django
from dapp.models import DataFile, ModelRun, Project, Actions, InputOutputDataFile, Scenario
from accounts.models import Account
from dapp.handle_modelrun import run_model
from django.shortcuts import render, get_object_or_404
from django.http import StreamingHttpResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.files import File
from django.db import transaction

# System

import os
import uuid
import shutil
from datetime import datetime
from os import path

# Custom / Thirdparty


@login_required
def index(request, project_uid, scenario_uid):

    criterion1 = Q(uid=project_uid)
    criterion2 = Q(account=request.user)
    project = get_object_or_404(Project, criterion1 & criterion2)
    criterion3 = Q(project=project)
    criterion4 = Q(uid=scenario_uid)
    scenario = get_object_or_404(Scenario, criterion2 & criterion3 & criterion4)

    criterion5 = Q(scenario=scenario)

    data_file = get_object_or_404(DataFile, criterion2 & criterion5)

    data = {
        'title': 'Model Run',
        'project': project,
        'mode': 'model',
        'data_file_uid': data_file.uid,
        'scenario': scenario,
    }

    if request.method == 'POST':
        return StreamingHttpResponse(running(request, project_uid, scenario_uid, scenario), content_type='text/html')

    return render(request, 'model_run/model_run.html', context=data)


# @csrf_exempt
# def run(request):
#     resp = StreamingHttpResponse(running(request), content_type='text/html')
#     return resp

@transaction.atomic
def running(request, project_uid, scenario_uid, scenario):
    msg = 'Successfully generated'
    result = True
    generated_folder_path = ''
    zip_path = ''

    # need to fetch from field
    mode = request.POST.get("mode")
    custom_flags = request.POST.get("custom_flags")
    if request.POST.get("createspreadsheetoption") == 'yes':
        create_spreadsheet = True
    else:
        create_spreadsheet = False
    if request.POST.get("createtextfileoption") == 'yes':
        create_text_file_output = True
    else:
        create_text_file_output = False

    if request.POST.get("generatelpfileoption") == 'yes':
        generate_lp_file = True
    else:
        generate_lp_file = False

    if request.POST.get("chkneosserver", ""):
        neos_server = True
    else:
        neos_server = False


    server = request.POST.get("chkneosserver")

    output_file_uid = request.POST.get("outputdatafilename")
    input_file_uid = request.POST.get("inputdatafilename")
    solver = request.POST.get("solver")
    scenario_name = scenario.name
    run_option = request.POST.get("runoption")
    mga_slack_value = request.POST.get("MGASlackValue")
    mga_iterations = request.POST.get("NumberofMGAIterations")
    mga_weighting_method = request.POST.get("MGAWeightingMethod")

    criterion1 = Q(uid=project_uid)
    criterion2 = Q(account=request.user)

    try:
        criterion_sc = Q(uid=scenario_uid)
        project = get_object_or_404(Project, criterion1 & criterion2)
        scenario_obj = get_object_or_404(Scenario, criterion_sc & criterion2)
        scenario = scenario_obj.name

        account = Account.objects.get(email=request.user.email)

        action_name = scenario + '_' + str(str(uuid.uuid4().hex.upper()[0:6]))
        ac = Actions.objects.create(name=action_name, mode=mode, project=project, account=account, scenario=scenario_obj)
        ac.save()

        input_data_file = DataFile.objects.get(uid=input_file_uid)
        output_data_file = DataFile.objects.get(uid=output_file_uid)

        with open(input_data_file.file.path, 'rb') as fi:
            my_input_file = File(fi, name=os.path.basename(fi.name))

            data_file_input = InputOutputDataFile.objects.create(
                name=input_data_file.name,
                account=account,
                project=project,
                scenario=scenario_obj,
                actions=ac,
                mode=mode,
                file=my_input_file
            )

            data_file_input

        with open(output_data_file.file.path, 'rb') as fi:
            my_output_file = File(fi, name=os.path.basename(fi.name))

            data_file_output = InputOutputDataFile.objects.create(
                name=input_data_file.name,
                account=account,
                project=project,
                scenario=scenario_obj,
                actions=ac,
                mode=mode,
                file=my_output_file
            )

            data_file_output.save()

        model_run = ModelRun.objects.create(solver=solver, run_option=run_option,
                                            mga_slack_value=mga_slack_value,
                                            mga_iterations=mga_iterations,
                                            mga_weighting_method=mga_weighting_method,
                                            scenario_name=scenario_name, account=account,
                                            create_spreadsheet=create_spreadsheet,
                                            create_text_file_output=create_text_file_output,
                                            generate_lp_file=generate_lp_file,
                                            scenario=scenario_obj,
                                            neos_server=neos_server,
                                            actions=ac, project=project, custom_flags=custom_flags,
                                            input=data_file_input, output=data_file_output)
        model_run.save()

    except Exception as e:
        transaction.set_rollback(True)

    # MR  = Model_Run.objects.create(scenario_name = scenario)
    # MR.save()
    # try:
    # This function will handle
    # TODO try catch handling

    generated_folder_path = settings.RESULT_DIR + "db_io/" + os.path.splitext(input_file_uid)[0] + "_" + action_name + "_model"

    if path.exists(generated_folder_path):
        shutil.rmtree(generated_folder_path)

    yield "<div>Starting Model Run \n"
    for k in run_model(request, action_name, input_data_file, output_data_file):
        yield k

    yield "Model Run Complete</div>"

    # if not generatedfolderpath:
    #  raise "Error detected"
    zip_path = ""

    if output_file_uid:
        random = str(uuid.uuid4().hex.upper()[0:6])
        output_dirname = 'db_io/db_io_' + random
        # print "Zipping: " + settings.BASE_DIR + "/" + generatedfolderpath + " | " + output_dirname

        result_download_folder_path = settings.UPLOADED_PROJECTS_DIR + str(project.uid) + '/scenarios/results/' + str(ac.uid)

        if os.path.exists(result_download_folder_path + '.zip'):
            os.remove(result_download_folder_path + '.zip')
        shutil.make_archive(result_download_folder_path, 'zip', generated_folder_path)

        if path.exists(generated_folder_path):
            shutil.make_archive(settings.RESULT_DIR + output_dirname, 'zip', generated_folder_path)

            zip_path = output_dirname + ".zip"
            yield "*Zip file is at path {" + zip_path + "}"

        else:
            yield "Failed to generate zip file"

    # except:
    #  msg = 'An error occurred. Please try again.'
    #  result = False

    # return JsonResponse( {"result" : result , "message" : msg , 'zip_path' : zip_path, "output" : _getLog()  } )


def _get_log():

    original_log_file = settings.RESULT_DIR + "debug_logs/Complete_OutputLog.log"
    archive_log_file = settings.RESULT_DIR + "debug_logs/OutputLog__" + str(datetime.now().date()) + "__" + str(
        datetime.now().time()) + ".log"

    file = open(original_log_file, 'r')

    if not file:
        return "Log not found or created"

    output = file.read()

    # Maintain archive of current log file
    file_arch = open(archive_log_file, "w")
    file_arch.write(output)

    return output

