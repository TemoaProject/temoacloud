from django.conf import settings
from django.conf.urls import url
from django.urls import path
from dapp.views import project, model_run, scenario, files, input_data, output_data, dashboard, actions


urlpatterns = [

    # SITE general URLS
    url('^$', dashboard.index, name='index'),

    # FILES

    path('project/files/index/<uuid:project_uid>', files.index, name='files.index'),
    path('project/files/view/<uuid:project_uid>/<uuid:file_uid>', files.view, name='files.view'),
    path('project/files/delete/<uuid:project_uid>/<uuid:file_uid>', files.delete, name='files.delete'),
    path('project/files/upload/<uuid:project_uid>', files.upload, name='files.upload'),
    path('project/files/file-upload/<uuid:project_uid>', files.file_upload, name='files.file_upload'),
    path('project/files/get-file-list/<uuid:project_uid>', files.get_file_list, name='files.get_file_list'),
    path('project/files/get-ct-list/<uuid:project_uid>', files.get_ct_list, name='files.get_ct_list'),
    path(settings.PUBLIC_URL + 'projects/<uuid:project_uid>/<str:type>/<str:file_name>', files.download, name='files.download'),
    path(settings.PUBLIC_URL + 'projects/<uuid:project_uid>/<str:scenario_base>/<str:result_base>/<uuid:action_uid><str:file_ext>', files.download_result, name='files.download_result'),
    # Add more like delete files, download files etc

    # RUN INPUT
    path('project/input-data/index/<uuid:project_uid>/<uuid:scenario_uid>', input_data.index, name='input_data.index'),
    path('project/input-data/run-input/<uuid:project_uid>/<uuid:scenario_uid>',
         input_data.run_input, name='input_data.run_input'),

    # RUN MODEL
    path('project/model-run/index/<uuid:project_uid>/<uuid:scenario_uid>', model_run.index, name='model_run.index'),
    # path('^/project/model-run/post/<uuid:project_uid>', model_run.run, name='model'),

    # RUN OUTPUT
    path('project/output-data/index/<uuid:project_uid>/<uuid:scenario_uid>', output_data.index, name='output_data.index'),
    path('project/output-data/run-output/<uuid:project_uid>/<uuid:scenario_uid>',
         output_data.run_output, name='output_data.run_output'),
    path('project/output-data/generate-plot/<uuid:project_uid>/<uuid:scenario_uid>',
         output_data.generate_plot, name='output_data.generate_plot'),
    path('project/output-data/load-sector/<uuid:project_uid>/<uuid:scenario_uid>',
         output_data.load_sector, name='output_data.load_sector'),
    # path('^dbquery/$', views.dbQuery, name='dbquery'),

    # PROJECTS
    path('projects/', project.index, name='project.index'),
    path('project/add', project.add, name='project.add'),
    path('project/fetch', project.fetch, name='project.fetch'),
    path('project/edit/<uuid:project_uid>', project.edit, name='project.edit'),
    path('project/delete/<uuid:project_uid>', project.delete, name='project.delete'),
    path('project/view/<uuid:project_uid>', project.view, name='project.view'),

    # SCENARIO
    path('project/scenario/<uuid:project_uid>/<uuid:scenario_uid>', scenario.index, name='scenario.index'),
    path('project/scenario/fetch/<uuid:project_uid>', scenario.fetch, name='scenario.fetch'),
    path('project/scenario/delete/<uuid:project_uid>/<uuid:scenario_uid>', scenario.delete, name='scenario.delete'),
    path('project/scenario/view/<uuid:project_uid>/<uuid:scenario_uid>', scenario.view, name='scenario.view'),

    # ACTIONS
    path('project/scenario/<uuid:project_uid>/<uuid:scenario_uid>/<uuid:action_uid>',
         actions.index, name='actions.index'),
    path('project/scenario/delete/<uuid:project_uid>/<uuid:scenario_uid>/<uuid:action_uid>',
         actions.delete, name='actions.delete'),
    path('project/scenario/view/<uuid:project_uid>/<uuid:scenario_uid>/<uuid:action_uid>',
         actions.view, name='actions.view'),
]

