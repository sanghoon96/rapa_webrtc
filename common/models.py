from django.db import models

# Create your models here.
class DroneDataModels(models.Model):
  id = models.AutoField(primary_key=True)     # 고유 ID
  d_id = models.CharField(max_length=100)     # 드론 아이디 
  img_path = models.CharField(max_length=200) # 이미지 경로 연_월_일 로 저장
  img_name = models.CharField(max_length=200) # 이미지 이름 시간_분_초 로 저장
  x = models.FloatField()                     # GPS 경도 좌표
  y = models.FloatField()                     # GPS 위도 좌표
  address = models.CharField(max_length=200)  # GPS 좌표에 해당하는 주소
  
