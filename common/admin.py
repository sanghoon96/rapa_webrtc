from django.contrib import admin
from .models import DroneDataModels
# Register your models here.
class DroneAdmin(admin.ModelAdmin):
    list_display = ('d_id','img_path','img_name')

admin.site.register(DroneDataModels, DroneAdmin)
