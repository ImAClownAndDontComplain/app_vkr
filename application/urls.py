from django.urls import path
from . import views
from .serializers import ToAnalyzeSerializer
urlpatterns = [
  # path('home/', views.home, name='home_path'),
  # path('hz/', views.get_username, name='hz'),
  path('all_ingr_names/', views.get_all_ingr_names, name='all_ingr_names'),
  path('analyze/', views.Analyze.as_view(), name='analyze'),
  path('analyze/get_analysis/<int:record_id>', views.GetAnalysis.as_view(), name='get_analysis'),
  path('compare/', views.Compare.as_view(), name='compare'),
  path('compare/get_comparison/<int:record_id1>/<int:record_id2>', views.GetComparison.as_view(), name='get_comparison'),
  path('profile/<str:option>', views.get_records, name='profile'),
  path('ingredient_search/<str:ingr_name>', views.get_ingredient_info, name='ingredient_info'),
  path('ingredient_search/', views.IngredientSearch.as_view(), name='ingredient_search'),
  path('profile/<str:option>/<int:record_id>', views.PutDelRecord.as_view(), name='update_record'),
]
# <str:ingr_name>,<str:effect>