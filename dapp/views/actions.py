from dapp.models import Scenario, Project, InputDataRun, OutputDataRun, CommTech, InputOutputDataFile, ModelRun, Actions

from django.shortcuts import  get_object_or_404, render
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from dapp.views import files


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

    actions = Actions.objects.filter(scenario_criterion1 & scenario_criterion2, action_criterion1)

    return render(request, 'scenario/index.html', {'actions': actions, 'project': project, 'scenario': scenario})


@login_required()
def delete(request, project_uid, scenario_uid, action_uid):

    criterion1 = Q(uid=action_uid)
    criterion2 = Q(account=request.user)
    action = get_object_or_404(Actions, criterion1 & criterion2)

    s = action.delete()

    if s:
        return JsonResponse({'message': 'Successfully deleted'})

    return JsonResponse({'error': 'Failed to delete'})


@login_required()
def view(request, project_uid, scenario_uid, action_uid):
    criterion1 = Q(uid=action_uid)
    criterion2 = Q(account=request.user)
    criterion_sc = Q(uid=scenario_uid)

    scenario = get_object_or_404(Scenario, criterion2 & criterion_sc)
    action = get_object_or_404(Actions, criterion1 & criterion2)
    criterion3 = Q(actions=action)
    if action.mode == 'input':
        class_name = InputDataRun
    elif action.mode == 'output':
        class_name = OutputDataRun
    else:
        class_name = ModelRun
    input_data = get_object_or_404(class_name, criterion2 & criterion3)
    if action.mode == 'input' or action.mode == 'output':
        criterion4 = Q(id=input_data.comm_tech_id)
        comm_tech_data = get_object_or_404(CommTech, criterion4)
        criterion5 = Q(id=input_data.input_file_id)
        io_data_file = get_object_or_404(InputOutputDataFile, criterion5)

        return render(request, 'scenario/view.html', {'action': action, 'project_uid': project_uid,
                                                      'scenario': scenario,
                                                      'input_data': input_data, 'comm_tech_data': comm_tech_data,
                                                      'data_file': io_data_file, 'files': files})
    else:
        model_run = input_data
        criterion1 = Q(id=model_run.input_id)
        input_data_file = get_object_or_404(InputOutputDataFile, criterion1)
        criterion2 = Q(id=model_run.output_id)
        output_data_file = get_object_or_404(InputOutputDataFile, criterion2)
        return render(request, 'scenario/view.html',
                      {'action': action, 'project_uid': project_uid, 'model_run': model_run, 'scenario': scenario,
                       'input_data_file': input_data_file, 'output_data_file': output_data_file, 'files': files})
