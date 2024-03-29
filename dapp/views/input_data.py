# Django
from dapp.models import DataFile, CommTech, Actions, InputDataRun, ModelRun, InputOutputDataFile, Scenario
from accounts.models import Account
from django.shortcuts import redirect, get_object_or_404, render
from django.http import HttpResponse
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q
from django.core.files import File
from django.db import transaction
from dapp.models import Project
# System

import os
import uuid
import shutil
from os import path

# Custom / Thirdparty

from thirdparty.temoa.data_processing.MakeGraphviz import GraphvizDiagramGenerator


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

    random = str(uuid.uuid4().hex.upper()[0:6])
    input_data = {
        'mode': 'input',
        'random': random,
        'title': 'Input Data',
        'project': project,
        'scenario': scenario,
        'data_file_uid': data_file.uid,
        'result_url': settings.RESULT_URL,
    }
    return render(request, 'input_and_output/input_data.html', context=input_data)


@login_required
@transaction.atomic
def run_input(request, project_uid, scenario_uid):
    if request.method != 'POST':
        return HttpResponse("Use post method only", status=403)
    selected_region = request.POST.get("region-value", "")
    criterion1 = Q(uid=project_uid)
    criterion2 = Q(account=request.user)
    criterion_sc = Q(uid=scenario_uid)
    project = get_object_or_404(Project, criterion1 & criterion2)

    scenario_obj = get_object_or_404(Scenario, criterion_sc & criterion2)
    criterion4 = Q(scenario=scenario_obj)

    color_format = request.POST.get("format", "svg")
    color_scheme = request.POST.get("color_scheme", "color")
    commodity_technology_type = request.POST.get("commodity-technology-type", "")
    commodity_technology_value = request.POST.get("commodity-technology-value", "")

    data_file = get_object_or_404(DataFile, criterion4 & criterion2)

    mode = request.POST.get("mode", "")
    scenario = scenario_obj.name

    try:

        account = Account.objects.get(email=request.user.email)
        action_name = scenario + '_' + str(str(uuid.uuid4().hex.upper()[0:6]))
        ac = Actions.objects.create(name=action_name, mode=mode, project=project, account=account, scenario=scenario_obj)
        ac.save()

        comm_tech = CommTech.objects.create(name=commodity_technology_type,
                                        value=commodity_technology_value,
                                        account=account,
                                        actions=ac,
                                        scenario=scenario_obj,
                                        project=project)
        comm_tech.save()


        with open(data_file.file.path, 'rb') as fi:
            my_file = File(fi, name=os.path.basename(fi.name))

            io_data_file = InputOutputDataFile.objects.create(
                name=data_file.name,
                account=account,
                project=project,
                scenario=scenario_obj,
                actions=ac,
                mode=mode,
                file=my_file
            )

            io_data_file.save()

        idr = InputDataRun.objects.create(
            color_scheme=color_scheme,
            comm_tech=comm_tech,
            input_file=io_data_file,
            output_format=color_format,
            account=account,
            project=project,
            scenario=scenario_obj,
            actions=ac
        )
        idr.save()
        success = "Scenario {0} created successfully".format(ac.name)

    except Exception as e:
        transaction.set_rollback(True)

    model_run = ModelRun.objects.order_by('-created').first()

    error = ''
    image_path = ''
    folder_path = ''
    zip_file_path = ''

    try:
        graph_gen = GraphvizDiagramGenerator(
            dbFile=data_file.file.path,
            scenario=scenario,
            outDir=settings.RESULT_DIR + mode,
            verbose=1,
            region=selected_region
        )
        graph_gen.connect()
        graph_gen.setGraphicOptions(greyFlag=(color_scheme == "grey"))

        if mode == "input":

            if commodity_technology_type == 'commodity':
                folder_path, image_path = graph_gen.createCompleteInputGraph(
                    region=selected_region,
                    inp_comm=commodity_technology_value,
                    outputFormat=color_format
                )
            elif commodity_technology_type == 'technology':
                folder_path, image_path = graph_gen.createCompleteInputGraph(
                    region=selected_region,
                    inp_tech=commodity_technology_value,
                    outputFormat=color_format
                )
            else:
                folder_path, image_path = graph_gen.createCompleteInputGraph(region=selected_region, outputFormat=color_format)

        graph_gen.close()

        print("output_file_path = ", image_path)
        if not path.exists(image_path):
            error = "The selected technology or commodity doesn't exist for selected period"
        else:
            if path.exists(folder_path):
                print("Zipping: " + folder_path)
                zip_file_path = folder_path + '_zip'
                result_download_folder_path = settings.UPLOADED_PROJECTS_DIR + '{0}/{1}/scenarios/{2}/results/{3}'.format(
                    project.uid,
                    scenario_obj.uid,
                    ac.uid, ac.uid)

                if os.path.exists(result_download_folder_path + '.zip'):
                    os.remove(result_download_folder_path + '.zip')
                shutil.make_archive(result_download_folder_path, 'zip', folder_path)

                if os.path.exists(zip_file_path + '.zip'):
                    os.remove(zip_file_path + '.zip')
                shutil.make_archive(zip_file_path, 'zip', folder_path)
                zip_file_path = os.path.relpath(zip_file_path + '.zip', settings.RESULT_DIR)
                image_path = os.path.relpath(image_path, os.path.join(settings.RESULT_DIR, mode))
            else:
                error = "Folder is missing at " + folder_path

    except Exception as e:
        print(e)
        error = 'An error occurred. Please try again.'

    return JsonResponse({
        "success": success,
        "error": error,
        "filename": image_path,
        "zip_path": zip_file_path,
        "folder": '',
        "mode": mode
    })

