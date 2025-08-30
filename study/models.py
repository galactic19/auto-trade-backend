from django.contrib.auth import get_user_model
from django.db import models

user = get_user_model()

class StudyModel(models.Model):
    name = models.CharField(max_length=255, unique=True, null=False, blank=False, verbose_name='작성자')
    description = models.TextField()
    auther = models.ForeignKey(user, on_delete=models.CASCADE, related_name='study_auther')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = 'DRF 공부'

    def __str__(self):
        return self.name