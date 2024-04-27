from rest_framework import serializers
from rest_framework.fields import ListField

# from .models import *

COMBINATION = [("Yes", "Yes"),
               ("Carefully", "Carefully"),
               ("No", "No")]

INTENSITY = [("Strong", "Strong"),
             ("Medium", "Medium"),
             ("Weak", "Weak")]

class IngrSerializer(serializers.Serializer):
    ingr_name = serializers.CharField(max_length=100, required=True)
    conc = serializers.FloatField(required=False)

class RecomSerializer(serializers.Serializer):
    recom_text = serializers.CharField(max_length=200, required=True)

class EffectSerializer(serializers.Serializer):
    # ingr_name = serializers.CharField(max_length=100, required=True)
    effect = serializers.CharField(max_length=200, required=True)
    intensity = serializers.ChoiceField(choices=INTENSITY, required=True)
    ingr = ListField(child=serializers.CharField(max_length=100))

class SideEffectSerializer(serializers.Serializer):
    ingr_name = serializers.CharField(max_length=100, required=True)
    side_effect = serializers.CharField(max_length=200, required=True)


class IngrResSerializerShort(serializers.Serializer):
    ingr_name = serializers.CharField(max_length=100, required=True)
    inci_name = serializers.CharField(max_length=100, required=False)
    type_name = serializers.CharField(max_length=100, required=True)
    description = serializers.CharField(max_length=200, required=True)
    effect = serializers.CharField(max_length=200, required=False)


class IngrResSerializerLong(serializers.Serializer):
    ingr_name = serializers.CharField(max_length=100, required=True)
    # ... потом доделаю


class CombSerializer(serializers.Serializer):
    ingr_name = serializers.CharField(max_length=100, required=True)
    inci_name_2 = serializers.CharField(max_length=100, required=False)
    comb_type = serializers.ChoiceField(choices=COMBINATION, required=True)
    description = serializers.CharField(max_length=500, required=True)

class ProductDataSerializer(serializers.Serializer):
    vegan = serializers.CharField(max_length=300, required=True)
    natural = serializers.CharField(max_length=300, required=True)
    pregnant = serializers.CharField(max_length=300, required=True)
    hypoallergenic = serializers.CharField(max_length=300, required=True)

class ToAnalyzeSerializer(serializers.Serializer):
    ingrs = ListField(child=IngrSerializer())

class AnalyzedSerializer(serializers.Serializer):
    effects = serializers.ListField(child=EffectSerializer())
    side_effects = serializers.ListField(child=SideEffectSerializer())
    recoms = serializers.ListField(child=RecomSerializer())
    ingrs = serializers.ListField(child=IngrResSerializerShort())
    combs = serializers.ListField(child=CombSerializer())
    data = ProductDataSerializer()
