# Django
from django.shortcuts import render

from django.shortcuts import redirect, get_object_or_404, render
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required, user_passes_test

from dapp.models import Scenario, Project, DataFile, InputDataRun, OutputDataRun, CommTech, InputOutputDataFile, ModelRun, Actions
from dapp.views import files
# System

# Custom / Thirdparty


@login_required
def index(request, project_uid, scenario_uid):

    project_criterion1 = Q(uid=project_uid)
    project_criterion2 = Q(account=request.user)

    project = Project.objects.select_related().filter(project_criterion1 & project_criterion2).first()

    scenario_criterion1 = Q(project=project)
    scenario_criterion2 = Q(account=request.user)
    scenario_criterion3 = Q(uid=scenario_uid)

    scenario = Scenario.objects.select_related().filter(scenario_criterion1 & scenario_criterion2,
                                                        scenario_criterion3).first()

    action_criterion1 = Q(scenario=scenario)

    data_file = get_object_or_404(DataFile, scenario_criterion2 & action_criterion1)

    actions = Actions.objects.filter(scenario_criterion1 & scenario_criterion2, action_criterion1)

    return render(request, 'scenario/index.html', {'actions': actions,
                                                   'project': project,
                                                   'scenario': scenario,
                                                   'data_file': data_file,
                                                   'files': files})


@login_required()
def fetch(request):

    q = request.GET['q']

    criterion1 = Q(name__icontains=q)
    criterion2 = Q(account=request.user)

    results = Actions.objects.filter(criterion1 & criterion2)

    rows = []
    # for result in results:
    #     rows.append({"id": result.id, "text": result.name})

    return JsonResponse({"items": rows})


@login_required()
def delete(request, project_uid, scenario_uid):

    criterion1 = Q(uid=scenario_uid)
    criterion2 = Q(account=request.user)
    scenario = get_object_or_404(Scenario, criterion1 & criterion2)

    s = scenario.delete()

    if s:
        return JsonResponse({'message': 'Successfully deleted'})

    return JsonResponse({'error': 'Failed to delete'})

    # return HttpResponseRedirect(reverse('listsaleitems'))
    # return redirect('project.manage')


@login_required()
def view(request, project_uid, scenario_uid):

    project_criterion1 = Q(uid=project_uid)
    project_criterion2 = Q(account=request.user)

    project = Project.objects.select_related().filter(project_criterion1 & project_criterion2).first()

    scenario_criterion1 = Q(project=project)
    scenario_criterion2 = Q(account=request.user)
    scenario_criterion3 = Q(uid=scenario_uid)

    scenario = Scenario.objects.select_related().filter(scenario_criterion1 & scenario_criterion2, scenario_criterion3).first()

    action_criterion1 = Q(scenario=scenario)
    data_file = get_object_or_404(DataFile, scenario_criterion2 & action_criterion1)

    actions = Actions.objects.filter(scenario_criterion1 & scenario_criterion2, action_criterion1)

    return render(request, 'scenario/index.html', {'actions': actions,
                                                   'project': project,
                                                   'scenario': scenario,
                                                   'data_file': data_file,
                                                   'files': files})


