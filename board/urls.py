

from django.contrib import admin
from django.urls import path, include

from . import views

#'board' is not a registered namespace
app_name='board' #이렇게 써줘야 없어진다  

urlpatterns = [
       
    # myhome/urls.py - path('board/', include('board.urls')),
    # 내가 받은 url중에 /board ~~~ 시작하는 url이 있으면 이거는 
    # board 폴더아래에 있는 urls.py  가 처리하라 
    
   
    path('group_list', views.group_list, name="group_list"),#http://127.0.0.1/board/list 

    path('list/<str:group_id>', views.list, name="list"),#http://127.0.0.1/board/list 
    path('write', views.write, name="write"), #http://127.0.0.1/board/write 
    path('save', views.save, name="save"), #http://127.0.0.1/board/save 
    
    path('view/<int:id>', views.view, name="view"), #http://127.0.0.1/board/view/1 
    #get방식으로 보내면 board_write.html에 디비 불러온거 그냥 뿌리고 
    #post방식으로 보내면 update를 실행한다 

    path('delete/<int:id>/<str:d_id>', views.delete, name="delete") 
    
]