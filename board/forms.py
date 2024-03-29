#/project/myhome/board/forms.py

#html문서로부터 form 태그의 값들을 읽어서 python 객체로 전환시켜서 
#views.py파일에서 사용이 가능 
#html페이지의 form 태그와 models의   field를 서로 연결시켜준다. 
from django import forms 
from common.models import DroneDataModels 

class BoardForm(forms.ModelForm):
     class Meta:
        #중요요소 
        model = DroneDataModels #모델을 전달해줘야 서로 연결이 된다. 
        #모델과 폼을 연결시킬 필드들을 지정한다 - db에 있는 필드랑 똑같이 
        #board_write.html의 form태그안에 있는 태그들에 이 이름이 있어야 한다 
        fields = ['d_id', 'img_path', 'img_name']
        labels = {'d_id':'드론 id', 'img_path':'이미지 경로', 'img_name':'이미지 이름'}


      
