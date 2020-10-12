from django.shortcuts import render
from django.http import HttpResponse
from django.http.response import HttpResponseRedirect
# url 처리를 위한 iport 파일 
import time #시간처리 
import os,errno,sys #파일 생성 및 제거 
from django.views.decorators.csrf import csrf_exempt #보안 토큰처리
from urllib.parse import quote # 데이터 
from urllib.request import Request, urlopen 
import json 
# Create your views here.
import base64
import pymysql 
from .models import DroneDataModels

# for login 
from django.urls.base import reverse
from django.contrib.auth.models import User #User 모델을 사용하기위해 선언해준다
from .forms import SigninForm,SignupForm
from django.contrib.auth import login, authenticate

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMAGE_DIRS=[
    os.path.join(BASE_DIR, 'image')
]

'''
    f"https://dapi.kakao.com/v2/local/geo/coord2regioncode.json?x={}&y={}"
        KakaoAK 876e9dd3cee1b67c2f15c6a58cd44f9c

'''

url = "https://dapi.kakao.com/v2/local/geo/coord2regioncode.json?"
KakaoAK = 'KakaoAK 876e9dd3cee1b67c2f15c6a58cd44f9c'


def index(request):
    return render(request, "index.html")

@csrf_exempt
def save(request):
    directory = ''
    if (request.method == 'POST'):
        id = request.POST.get('d_id')
        x = request.POST.get('x')
        y = request.POST.get('y')
        address = request.POST.get('add')
        print(id)
        img = request.POST.get('img')
        img = img.replace('data:image/png;base64,', '')
        img = img.replace(' ', '+')
        d = base64.b64decode(img)      
        now = time.localtime()
        directory = f'./image/{id}/{now.tm_year}_{now.tm_mon}_{now.tm_mday}/'
        print(id,x,y,address)
        try:
            os.makedirs(directory)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
        d_name = f'p{now.tm_hour}_{now.tm_min}_{now.tm_sec}.png'
    
        data_to_database(id,directory,d_name,x,y,address)
        file = open(directory+d_name, mode="wb")        
        file.write(d)
        file.close()
 

    return HttpResponse("receive")


def data_to_database(d_id,img_path,img_name,x,y,address):
    conn = pymysql.connect(host='localhost', user='user01', password='1234',port=5306,
                       db='mydb', charset='utf8') 
    curs = conn.cursor()
    sql = """insert into common_dronedatamodels(d_id,img_path,img_name,x,y,address)
            values (%s, %s, %s, %s, %s, %s)"""
    curs.execute(sql,(d_id,img_path,img_name,x,y,address))
    conn.commit()    
    conn.close()

def signup(request):#역시 GET/POST 방식을 사용하여 구현한다.
    if request.method == "GET":
        return render(request, 'signup.html', {'f':SignupForm()} )
    
    
    elif request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['password']  == form.cleaned_data['password_check']:
#cleaned_data는 사용자가 입력한 데이터를 뜻한다.
#즉 사용자가 입력한 password와 password_check가 맞는지 확인하기위해 작성해주었다.

                new_user = User.objects.create_user(form.cleaned_data['username'],form.cleaned_data['email'],form.cleaned_data['password'])
#User.object.create_user는 사용자가 입력한 name, email, password를 가지고 아이디를 만든다.
#바로 .save를 안해주는 이유는 User.object.create를 먼저 해주어야 비밀번호가 암호화되어 저장된다.

                new_user.last_name = form.cleaned_data['last_name']
                new_user.first_name = form.cleaned_data['first_name']
#나머지 입력하지 못한 last_name과, first_name은 따로 지정해준다.
                new_user.save()
                
                return HttpResponseRedirect(reverse('vote:index'))      
            else:
                return render(request, 'signup.html',{'f':form, 'error':'비밀번호와 비밀번호 확인이 다릅니다.'})#password와 password_check가 다를 것을 대비하여 error를 지정해준다.

        else: #form.is_valid()가 아닐 경우, 즉 유효한 값이 들어오지 않았을 경우는

            return render(request, 'signup.html',{'f':form})
#원래는 error 메시지를 지정해줘야 하지만 따로 지정해주지 않는다.
#그 이유는 User 모델 클래스에서 자동으로 error 메시지를 넘ㄱ

def signin(request):#로그인 기능
    if request.method == "GET":
        return render(request, 'customlogin/signin.html', {'f':SigninForm()} )
    
    elif request.method == "POST":
        form = SigninForm(request.POST)
        id = request.POST['username']
        pw = request.POST['password']
        u = authenticate(username=id, password=pw)
#authenticate를 통해 DB의 username과 password를 클라이언트가 요청한 값과 비교한다.
#만약 같으면 해당 객체를 반환하고 아니라면 none을 반환한다.

        if u: #u에 특정 값이 있다면
            login(request, user=u) #u 객체로 로그인해라
            return HttpResponseRedirect(reverse('vote:index'))
        else:
            return render(request, 'customlogin/signin.html',{'f':form, 'error':'아이디나 비밀번호가 일치하지 않습니다.'})
    
from django.contrib.auth import logout #logout을 처리하기 위해 선언

def signout(request): #logout 기능
    logout(request) #logout을 수행한다.
    return HttpResponseRedirect(reverse('vote:index'))
