from django.urls import path
from . import views
from .serializers import ToAnalyzeSerializer
urlpatterns = [
  path('home/', views.home, name='home_path'),
  path('hz/', views.get_username, name='hz'),
  path('all_ingr_names/', views.get_all_ingr_names, name='all_ingr_names'),
  path('analyze/', views.Analyze.as_view(), name='analyze'),
  path('analyze/get_analysis/<int:record_id>', views.GetAnalysis.as_view(), name='get_analysis')
]
