from django.contrib import admin
from dapp.models import DataFile, CommTech, InputDataRun, ModelRun, OutputDataRun
# Register your models here.


admin.site.register(DataFile)
admin.site.register(CommTech)
admin.site.register(InputDataRun)
admin.site.register(ModelRun)
admin.site.register(OutputDataRun)
