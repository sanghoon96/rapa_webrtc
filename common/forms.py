#/project/myhome/board/forms.py

#html문서로부터 form 태그의 값들을 읽어서 python 객체로 전환시켜서 
#views.py파일에서 사용이 가능 
#html페이지의 form 태그와 models의   field를 서로 연결시켜준다. 
from django import forms 
from django.contrib.auth.models import User

class SignupForm(forms.ModelForm):
   password_check = forms.CharField(max_length=200, widget=forms.PasswordInput())
#아쉽게도 User 모델에서는 password_check 필드를 제공해주지 않는다.
#따라서 따로 password_check 필드를 직접 정의해줄 필요가 있다.
#입력 양식은 type은 기본이 text이다. 따라서 다르게 지정해주고 싶을 경우 widget을 이용한다.
#widget=forms.PasswordInput()은 입력 양식을 password로 지정해주겠다는 뜻이다.

   field_order=['username','password','password_check','last_name','first_name','email']
   class Meta:
      model = User
      widgets = {'password':forms.PasswordInput}
      fields = ['username','password','last_name','first_name','email']
      
class SigninForm(forms.ModelForm): #로그인을 제공하는 class이다.
   class Meta:
       
      widgets = {'password':forms.PasswordInput}
      fields = ['username','password']      
