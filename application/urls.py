from django.urls import path
from . import views

urlpatterns = [
  path('home', views.home, name='home_path'),
  path('analyze/<int:record_id>', views.GetAnalysis.as_view(), name='analyze')
]
