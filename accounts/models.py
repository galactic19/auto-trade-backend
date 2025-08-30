from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # user 데이터 컬럼 추가
    api_key = models.CharField(max_length=100, unique=True, verbose_name='API KEY')
    secret_key = models.CharField(max_length=100, unique=True, verbose_name='SECRET KEY')

    class Meta:
        verbose_name_plural = '회원 정보'

    def __str__(self):
        return self.username


class UserToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_token')
    access_token = models.CharField(max_length=100, verbose_name='ACCESS TOKEN')
    refresh_token = models.CharField(max_length=100, verbose_name='REFRESH TOKEN')
    expires_in = models.DateTimeField(verbose_name='EXPIRES IN')
    
    class Meta:
        verbose_name_plural = '토큰 관리'

    def __str__(self):
        return self.access_token