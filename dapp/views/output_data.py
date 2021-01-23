# Django
from dapp.models import DataFile, CommTech, Actions, ModelRun, OutputDataRun, InputOutputDataFile, Scenario
from accounts.models import Account
from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q
from django.core.files import File
from django.http import HttpResponse
from django.db import transaction
from dapp.models import Project
# System

import os
import uuid
import shutil
from os import path

# Custom / Thirdparty

from thirdparty.temoa.data_processing.MakeOutputPlots import OutputPlotGenerator
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

    output_data = {
        'mode': 'output',
        'title': 'Output Data',
        'project': project,
        'scenario': scenario,
        'data_file_uid': data_file.uid,
        'result_url': settings.RESULT_URL,
    }
    return render(request, 'input_and_output/output_data.html', context=output_data)


# FIX me save the database entry
def generate_plot(request, project_uid, scenario_uid):

    criterion1 = Q(uid=project_uid)
    criterion2 = Q(account=request.user)
    project = get_object_or_404(Project, criterion1 & criterion2)

    data_file_uid = request.POST.get("db-plot-datafilename", "")
    scenario = request.POST.get("plot-scenario-name", "")
    plot_type = int(request.POST.get("plot-type-name", "1"))
    sector = request.POST.get("sector-type-name", "")
    super_categories = request.POST.get("merge-tech", False)

    criterion3 = Q(uid=data_file_uid)

    data_file = get_object_or_404(DataFile, criterion3)

    db_path = settings.UPLOADED_PROJECTS_DIR + '{0}/files/{1}'.format(project_uid, data_file.name)

    # db_path = settings.UPLOADED_PROJECTS_DIR + filename

    image_path_dir = settings.RESULT_DIR + 'matplot/'
    res = OutputPlotGenerator(db_path, scenario)

    plot_path = 'result/matplot/'
    error = ""
    try:
        if plot_type == 1:
            plot_path += res.generatePlotForCapacity(sector, super_categories, image_path_dir)
        elif plot_type == 2:
            plot_path += res.generatePlotForOutputFlow(sector, super_categories, image_path_dir)
        elif plot_type == 3:
            plot_path += res.generatePlotForEmissions(sector, super_categories, image_path_dir)
    except Exception as e:
        plot_path = ""
        error = "An error occurred. Please try again in some time."

    return JsonResponse({"data": plot_path, "error": error})


# FIXME save in DB
def load_sector(request, project_uid, scenario_uid):

    criterion1 = Q(uid=project_uid)
    criterion2 = Q(account=request.user)
    project = get_object_or_404(Project, criterion1 & criterion2)

    data_file_uid = request.GET.get('filename')
    scenario = request.GET.get("scenario")
    plot_type = int(request.GET.get('plottype', '1'))

    criterion3 = Q(uid=data_file_uid)

    data_file = get_object_or_404(DataFile, criterion3)

    db_path = settings.UPLOADED_PROJECTS_DIR + '{0}/files/{1}'.format(project_uid, data_file.name)

    # db_path = settings.UPLOADED_PROJECTS_DIR + filename

    sectors = []
    error = ''
    try:
        res = OutputPlotGenerator(db_path, scenario)
        sectors = res.getSectors(plot_type)
    except Exception as e:
        error = 'Database file not supported: ' + db_path

    return JsonResponse({"data": sectors, "error": error})


@login_required
@transaction.atomic
def run_output(request, project_uid, scenario_uid):
    if request.method != 'POST':
        return HttpResponse("Use post method only", status=403)

    criterion1 = Q(uid=project_uid)
    criterion2 = Q(account=request.user)
    criterion_sc = Q(uid=scenario_uid)
    project = get_object_or_404(Project, criterion1 & criterion2)
    scenario_obj = get_object_or_404(Scenario, criterion_sc & criterion2)

    color_format = request.POST.get("format", "svg")
    color_scheme = request.POST.get("color_scheme", "color")
    commodity_technology_type = request.POST.get("commodity-technology-type", "")
    commodity_technology_value = request.POST.get("commodity-technology-value", "")
    data_file_uid = request.POST.get("datafile", "")

    mode = request.POST.get("mode", "")
    scenario = scenario_obj.name
    date_range = request.POST.get("date-range", "")

    criterion3 = Q(uid=data_file_uid)

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

        input_file = get_object_or_404(DataFile, criterion2 & criterion3)
        with open(input_file.file.path, 'rb') as fi:
            my_file = File(fi, name=os.path.basename(fi.name))

            io_data_file = InputOutputDataFile.objects.create(
                name=input_file.name,
                account=account,
                project=project,
                scenario=scenario_obj,
                actions=ac,
                mode=mode,
                file=my_file
            )

            io_data_file.save()

        model_run = ModelRun.objects.order_by('-created').first()

        odr = OutputDataRun.objects.create(
            color_scheme=color_scheme,
            output_format=color_format,
            comm_tech=comm_tech,
            input_file=io_data_file,
            model_run=model_run,
            year=date_range,
            account=account,
            project=project,
            scenario=scenario_obj,
            actions=ac
        )
        odr.save()
        success = "Scenario {0} created successfully".format(ac.name)

    except Exception as e:
        transaction.set_rollback(True)

    error = ''
    image_path = ''
    folder_path = ''
    zip_file_path = ''
    try:
        graph_gen = GraphvizDiagramGenerator(
            dbFile=input_file.file.path,
            scenario=scenario,
            outDir=settings.RESULT_DIR + mode,
            verbose=1
        )
        graph_gen.connect()
        graph_gen.setGraphicOptions(greyFlag=(color_scheme == "grey"))

        if commodity_technology_type == 'commodity' and (commodity_technology_value != ""):
                folder_path, image_path = graph_gen.CreateCommodityPartialResults(
                    period=date_range,
                    comm=commodity_technology_value,
                    outputFormat=color_format
                )
        elif commodity_technology_type == 'technology' and (commodity_technology_value != ""):
                folder_path, image_path = graph_gen.CreateTechResultsDiagrams(
                    period=date_range,
                    tech=commodity_technology_value,
                    outputFormat=color_format
                )
        else:
            folder_path, image_path = graph_gen.CreateMainResultsDiagram(
                period=date_range,
                outputFormat=color_format
            )

        graph_gen.close()

        print("output_file_path = ", image_path)
        if not path.exists(image_path):
            error = "The selected technology or commodity doesn't exist for selected period"
        else:
            if path.exists(folder_path):
                print("Zipping: " + folder_path)
                zip_file_path = folder_path + '_zip'
                result_download_folder_path = settings.UPLOADED_PROJECTS_DIR + str(project.uid) + '/scenarios/results/' + str(ac.uid)

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
