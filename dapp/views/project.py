# Django
from django.shortcuts import redirect, get_object_or_404, render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q
# APP
from dapp.models import Project, Scenario
from dapp.forms.project import ProjectForm


@login_required()
def index(request):

    criterion1 = Q(account=request.user)
    projects = Project.objects.filter(criterion1)
    context = {
        'projects': projects
    }
    # if request.method == 'POST': # why POST is required?

    return render(request, 'project/index.html', context)


@login_required()
def fetch(request):

    q = request.GET['q']

    criterion1 = Q(name__icontains=q)
    criterion2 = Q(account=request.user)

    results = Project.objects.filter(criterion1 & criterion2)

    rows = []
    for result in results:
        rows.append({"id": result.id, "text": result.name})

    return JsonResponse({"items": rows})


@login_required()
def add(request):
    form = None
    if request.method == 'POST':
        # lines = ast.literal_eval(request.POST['lines'])

        form = ProjectForm(request.POST)

        if form.is_valid():
            form.instance.account = request.user
            form.save()

            return redirect('project.index')
    else:
        form = ProjectForm()

    return render(request, 'project/add.html', {'form': form})


@login_required()
def edit(request, project_uid):

    form = None

    criterion1 = Q(uid=project_uid)
    criterion2 = Q(account=request.user)

    project = Project.objects.select_related().filter(criterion1 & criterion2).first()

    if request.method == 'POST':
        # lines = ast.literal_eval(request.POST['lines'])

        form = ProjectForm(request.POST, instance=project)

        if form.is_valid():
            form.instance.account = request.user
            form.save()
            # return HttpResponse("done")
            return redirect('project.index')

    else:
        form = ProjectForm(instance=project)

    # for item in addressItem.items.all():
    #    print( "item", item.name )

    return render(request, 'project/edit.html', {'form': form, 'project': project})


@login_required()
def delete(request, project_uid):

    criterion1 = Q(uid=project_uid)
    criterion2 = Q(account=request.user)
    project = get_object_or_404(Project, criterion1 & criterion2)

    p = project.delete()

    if p:
        return JsonResponse({'message': 'Successfully deleted'})

    return JsonResponse({'error': 'Failed to delete'})

    # return HttpResponseRedirect(reverse('listsaleitems'))
    # return redirect('project.manage')


@login_required()
def view(request, project_uid):

    # objects = SaleItemLine.objects.select_related().filter(sale_item_id=id)
    # __init__.pyprint ("id : ", id)

    criterion1 = Q(uid=project_uid)
    criterion2 = Q(account=request.user)

    project = get_object_or_404(Project, criterion1 & criterion2)

    scenario_criterion1 = Q(project=project)
    scenario_criterion2 = Q(account=request.user)

    scenarios = Scenario.objects.filter(scenario_criterion1 & scenario_criterion2)

    return render(request, 'project/view.html', {'project': project, 'scenarios': scenarios})
