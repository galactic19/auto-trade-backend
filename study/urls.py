from django.urls import path

from study import views

app_name = 'study'

urlpatterns = [
    # path('', views.get_study, name='get_study')
    path('', views.StudyListView.as_view(), name='get_study'),
    path('<int:pk>/', views.StudyDetailView.as_view(), name='get_study_detail'),
]
