from django.contrib import admin
from django.urls import path, include
from . import views
from .views import *


#'board' is not a registered namespace
app_name='common' #이렇게 써줘야 없어진다  

urlpatterns = [
    path('', views.index),
    path('save', views.save, name="write"), #http://127.0.0.1/board/write     
    path('signup/',views.signup ,name="signup"),
    path('login/',views.signup ,name="login"),
    path('logout/',views.signup ,name="logout")
]

######## 이부분 추가하기 
from django.conf import settings
from django.conf.urls.static import static
urlpatterns+=static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
print(urlpatterns)