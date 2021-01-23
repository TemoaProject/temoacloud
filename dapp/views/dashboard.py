from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    return render(request, 'dashboard/index.html')


# def dbQuery(request):
#     inputs = {
#         "--query": request.POST['query'],
#         "--input": request.POST['input']
#     }
#
#     result = get_flags(inputs)
#
#     return JsonResponse({"result": result})





