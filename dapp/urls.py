from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login$', views.login, name='login'),
    url(r'^input$', views.inputData, name='input'),
    url(r'^output$', views.outputData, name='output'),
    url(r'^modelrun$', views.modelRun, name='modelrun'),
    url(r'^about$', views.about, name='about'),
    url(r'^model$', views.runModel, name='model'),
    url(r'^fileupload$', views.fileUpload, name='fileupload'),
    url(r'^runinput$', views.runInput, name='runinput'),
    url(r'^loadfilelist$', views.loadFileList, name='loadfilelist'),
    url(r'^loadctlist$', views.loadCTList, name='loadctlist')
]
