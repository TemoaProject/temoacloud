# Django
from dapp.models import DataFile, Project
from accounts.models import Account
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import uuid
from django.core import serializers
from django.template.defaultfilters import slugify

# System

import os

# Custom / Thirdparty
from dapp.views.customtags.custom_tags import check_name
from thirdparty.temoa.temoa_model import get_comm_tech
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from dapp.models import Project, DataFile, Scenario

VALID_EXTENSIONS = ['.sqlite', '.sqlite3']
MAX_FILE_SIZE = 100 * 1024 * 1024


@login_required
def index(request, project_uid):
    criterion1 = Q(uid=project_uid)
    criterion2 = Q(account=request.user)

    project = get_object_or_404(Project, criterion1 & criterion2)

    criterion3 = Q(project=project)
    files = DataFile.objects.filter(criterion2 & criterion3)
    return render(request, 'files/index.html', {
        'files': files,
        'project': project
    })


@login_required
def view(request, project_uid, file_uid):
    return render(request, 'files/view.html', {})


@login_required
def download(request, project_uid, file_type, file_name):
    return render(request, '/' + settings.PUBLIC_URL + 'projects/' + project_uid + '/' + file_type + '/' + file_name, {})

@login_required
def download_result(request, project_uid, scenario_base, result_base, action_uid, file_ext):
    return render(request, '/' + settings.PUBLIC_URL + 'projectss/' + project_uid + '/' + scenario_base + '/' + result_base + '/' + action_uid + '' + file_ext, {})


@login_required
def delete(request, project_uid, file_uid):
    fe = DataFile.objects.get(uid=file_uid).delete()

    if fe:
        return JsonResponse({'message': 'Successfully deleted'})

    return JsonResponse({'error': 'Failed to delete'})


@login_required
def upload(request, project_uid):
    criterion1 = Q(uid=project_uid)
    criterion2 = Q(account=request.user)

    project = get_object_or_404(Project, criterion1 & criterion2)

    criterion3 = Q(project_uid=project_uid)
    # files = DataFile.objects.filter(criterion1 & criterion2 & criterion3)
    if request.method == 'POST':

        scenario_name = str(request.POST.get("scenario_name", ""))
        account = Account.objects.get(email=request.user)
        project = Project.objects.get(pk=project.id)

        scenario_criterion = Q(project=project)
        scenario_criterion1 = Q(name__iexact=scenario_name)

        scenarios = Scenario.objects.filter(scenario_criterion & scenario_criterion1).first()

        if scenarios:
            return JsonResponse({
                'error': 'A scenario with same name already exist'
            }, status=403)

        fname, fext = os.path.splitext(request.FILES['file'].name)

        if fext in VALID_EXTENSIONS:
            request.FILES['file'].name = check_name(request.FILES['file'].name)
            scenario = Scenario.objects.create(
                name=scenario_name,
                account=account,
                project=project,
            )

            data_file = DataFile.objects.create(
                 file=request.FILES['file'],
                 name=request.FILES['file'].name,
                 account=account,
                 project=project,
                 scenario=scenario,
            )

            if request.FILES['file'].size > MAX_FILE_SIZE:
                return JsonResponse({'error': 'File too big'}, status=403)
            else:
                data_file.save()
                scenario.save()
            return JsonResponse({'message': 'File uploaded successfully'}, status=200)

        else:
            return JsonResponse({
                'error': 'Please select a valid sqlite file. Supported extensions {}'.format
                (', '.join(VALID_EXTENSIONS))
            }, status=403)

    return render(request, 'files/upload.html', {
        # 'files': files,
        'project': project
    })


@login_required
def file_upload(request, project_uid):
    if request.method == 'POST':
        mode = request.POST.get("mode", "input")
        overwrite = request.POST.get("isOverwrite", False)
        account = Account.objects.get(email=request.user.email)
        project = Project.objects.get(pk=1)  # FIXME use correct and current project id
        data_file = DataFile.objects.create(
            mode=mode,
            file=request.FILES['file'],
            name=request.FILES['file'].name,
            account=account
        )
        data_file.save()

        # Commented the following line because this method is no longer used
        # as we are now using Django's dynamic file upload system in models.py
        # see upload_too, and it's usage in class Data_File.
        # result = handle_uploaded_file( request.FILES['file'],  mode, overwrite)

        # if string is empty we have no errors hence success
        # if not result :
        if mode == "input":
            return JsonResponse({"data": get_input_files(mode), 'mode': mode})
        elif mode == "output":
            return JsonResponse({"data": get_output_files(mode), 'mode': mode})

    else:
        return JsonResponse({'error': 'NO GET ACCESS ALLOWED'}, status=403)


@login_required
def get_input_files(mode, project_uid):
    print('Come in input function')
    if mode == 'input':
        print('Come in input function')
        types = ('.data', '.sqlite', '.sqlite3', '.dat')
        filelist = [each for each in os.listdir(settings.UPLOADED_PROJECTS_DIR) if each.endswith(types)]
        return sorted(filelist, key=lambda s: s.lower())
    return []


@login_required
def get_output_files(mode, project_uid):
    if mode == 'output':
        types = ('.sqlite', '.sqlite3')
        filelist1 = [each for each in os.listdir(settings.UPLOADED_OUTPUT_DIR) if each.endswith(types)]
        return sorted(filelist1, key=lambda s: s.lower())
    return []

    # else:


@login_required
def get_file_list(request, project_uid):
    criterion1 = Q(uid=project_uid)
    criterion2 = Q(account=request.user)

    project = get_object_or_404(Project, criterion1 & criterion2)

    criterion3 = Q(project=project)
    file_list = DataFile.objects.filter(criterion2 & criterion3).only('name')
    # file_list = sorted(files, key=lambda s: s.lower())
    return JsonResponse(serializers.serialize("json", file_list), safe=False)


@login_required
def get_ct_list(request, project_uid):
    error = ''
    data = {}

    mode = request.GET.get('mode', '')

    file_uid = request.GET.get('filename')
    criterion_data_file1 = Q(account=request.user)
    criterion_data_file2 = Q(uid=file_uid)
    data_file = get_object_or_404(DataFile, criterion_data_file1 & criterion_data_file2)
    filename = data_file.name

    list_type = request.GET.get('type', '')
    scenario_name = request.GET.get('scenario-name', '')

    criterion1 = Q(uid=project_uid)
    criterion2 = Q(account=request.user)

    project = get_object_or_404(Project, criterion1 & criterion2)

    if mode == "output":
        input_dict = {"--input": settings.UPLOADED_PROJECTS_DIR + str(project.uid) + '/files/' + filename}
        _, fext = os.path.splitext(filename)
    else:
        input_dict = {"--input": settings.UPLOADED_PROJECTS_DIR + str(project.uid) + '/files/' + filename}
        _, fext = os.path.splitext(filename)

    if mode == "output" and fext == '.dat':
        error = "For output, only database files supported (.sqlite)"
        return JsonResponse({"data": data, "error": error})

    if list_type == 'commodity':
        input_dict["--comm"] = True

    elif list_type == 'technology':
        input_dict["--tech"] = True

    elif list_type == 'scenario':
        input_dict["--scenario"] = True

    elif list_type == 'period':
        input_dict["--period"] = True

    try:
        data = get_comm_tech.get_info(input_dict)
    except Exception as e:
        error = 'An error occurred. Please try again.'

    return JsonResponse({"data": data, "error": error})
    # return JsonResponse( {"result" : msg , "message" : msg } )


def handle_uploaded_file(f, mode, overwrite):
    import os.path
    print("mode: " + mode)

    fname = settings.UPLOADED_PROJECTS_DIR + f.name

    filename, file_extension = os.path.splitext(f.name)
    # print(fname)
    # print file_extension

    if file_extension != ".data" and file_extension != ".sqlite" and file_extension != ".dat":
        return "Please select a valid file. Supported files are data and sqlite"

    if os.path.isfile(fname):

        if int(overwrite) != 0:
            # print("isOverwrite 2", overwrite )
            try:
                os.remove(fname)
            except OSError as e:  # name the Exception `e`
                # print "Failed with:", e.strerror # look what it says
                # print "Error code:", e.code
                return "File already exists and failed to overwrite. Reason is {0}. Please try again.".format(
                    e.strerror)
        else:
            # print("isOverwrite 3", overwrite )
            # print "Testing" + fname
            return "File already exists. Please rename and try to upload."

    with open(fname, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

    return ""
