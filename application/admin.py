from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Inci)
admin.site.register(Type)
admin.site.register(Ingredient)
admin.site.register(Feature)
admin.site.register(InciFeature)
admin.site.register(Recommendation)
admin.site.register(InciRecom)
admin.site.register(Combination)
admin.site.register(Record)
