from django.shortcuts import render
from django.http import HttpResponse
from common.models import DroneDataModels
from .forms import BoardForm
from django.utils import timezone 
from django.shortcuts import redirect 
from common.CommonPage import CommonPage, dictFectchAll
from django.db import connection

# Create your views here.

def index(request):
    return HttpResponse("This is my board")

def group_list(request):
    cursor =  connection.cursor()    
    page = int(request.GET.get('page', '1'))  # 페이지
    num = 10

    #페이징을 위해 drone ID의 갯수를 카운터 
    sql ="""
    select count(*) from (select distinct d_id from  common_dronedatamodels) A
    """
    cursor.execute(sql)
    totalCount= int(cursor.fetchone()[0])
    commonPage = CommonPage(totalCount, page)
    start = (page-1)*10

    #Drone ID의 데이터를 중복없이 취득
    sql = '''
        SELECT distinct d_id from common_dronedatamodels 
    '''
    cursor.execute(sql)
    boards_obj = dictFectchAll(cursor)
    
    context = {'board_list': boards_obj, "commonPage":commonPage}
    return render(request, 'board/board_id_list.html', context)


def list(request,group_id):
    #페이징에 필요한 정보들
    #나타낼 블록 
    cursor =  connection.cursor()    
    page = int(request.GET.get('page', '1'))  # 페이지
    num = 10

    #전체 레코드 개수 구하기 
    sql =f"select count(*) from common_dronedatamodels where d_id='{group_id}'"
    cursor.execute(sql)
    totalCount= int(cursor.fetchone()[0])
    commonPage = CommonPage(totalCount, page)
    start = (page-1)*10

    # 드론 ID를 기준으로 페이징을 위한 rnum 을 추가한 리스트를 얻기위한 쿼리문
    sql = f'''
    SELECT *
    FROM  (
		SELECT 
		  cast((SELECT  @ROWNUM := @ROWNUM + 1) as integer) AS rnum,
		  d_id, img_path, img_name,address, id         
		 FROM  common_dronedatamodels T 
         ,(SELECT @ROWNUM := 0 ) TMP 
         where T.d_id='{group_id}'
         ORDER BY ID ASC
    ) as B 
    ORDER BY B.rnum DESC
    LIMIT {start}, 10;
    '''
    cursor.execute(sql)
    boards_obj = dictFectchAll(cursor)
    context = {'board_list': boards_obj, "commonPage":commonPage}

    return render(request, 'board/board_list.html', context)

#/project/myhome/board/views.py 


def write(request): # 참고사항
    #폼객체를 만들어서 render 의 세번째 인자로 전달하자 
    form = BoardForm()
    return render(request, 'board/board_write.html', {'form':form})

#save 까지 
def save(request):
    form = BoardForm(request.POST) #POST 로 전송받는거만 처리하겠다 
    
    #디비에 저장하기 위해서 model 객체를 가져온다 
    board = form.save(commit=False) #반드시 - commit는 False 로  
    #True로 지정하면 바로 db로 저장되기 때문에 중간에, 저장은 막고 
    #모델 객체만 반환받으려면 commit 속성을 반드시 False로 해줘야 한다 
     #이 두 요소는 form 객체에 없었음 
    board.save() # 모델내의 save함수를 호출하여  db에 저장한다 
    return redirect('board:list')

#python manage.py createsuperuser 

from django.shortcuts import get_object_or_404
def view(request, id):

    cursor =  connection.cursor()
    sql = f'''
    select * from common_dronedatamodels where id={id}
    '''
    cursor.execute(sql)
    boards_obj = dictFectchAll(cursor)    
    print(boards_obj)
    context = {'board':boards_obj[0]}
    print(context)
    return render(request, 'board/board_view.html', context)

def delete(request,id,d_id):
    cursor =  connection.cursor()
    sql = f'''
    delete from common_dronedatamodels where id = {id}
    '''
    print(d_id )
    cursor.execute(sql)
    return redirect('board:list',d_id)

    
