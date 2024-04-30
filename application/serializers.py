from rest_framework import serializers
from rest_framework.fields import ListField

# from .models import *

COMBINATION = [("Yes", "Yes"),
               ("Carefully", "Carefully"),
               ("No", "No")]

# INTENSITY = [("Strong", "Strong"),
#              ("Medium", "Medium"),
#              ("Weak", "Weak")]

class IngrSerializer(serializers.Serializer):
    ingr_name = serializers.CharField(max_length=100, required=True)
    concentration = serializers.CharField(max_length=10, required=False)

class RecomSerializer(serializers.Serializer):
    recom_text = serializers.CharField(max_length=200, required=True)

class EffectSerializer(serializers.Serializer):
    effect = serializers.CharField(max_length=200, required=True)
    ingrs = ListField(child=serializers.CharField(max_length=100))

class EffectWithIntensitySerializer(serializers.Serializer):
    intensity = serializers.CharField(max_length=100, required=True)
    effect_with_ingrs = ListField(child=EffectSerializer())


class SideEffectSerializer(serializers.Serializer):
    side_effect = serializers.CharField(max_length=200, required=True)
    ingrs = ListField(child=serializers.CharField(max_length=100))


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
    description = serializers.CharField(max_length=500, required=True)

class CombWithTypeSerializer(serializers.Serializer):
    comb_type = serializers.CharField(max_length=100, required=True)
    combination = serializers.ListField(child=CombSerializer())

class ProductDataSerializer(serializers.Serializer):
    vegan = serializers.CharField(max_length=300, required=True)
    natural = serializers.CharField(max_length=300, required=True)
    pregnant = serializers.CharField(max_length=300, required=True)
    hypoallergenic = serializers.CharField(max_length=300, required=True)

class ToAnalyzeSerializer(serializers.Serializer):
    ingrs = serializers.ListField(child=IngrSerializer())

class AnalyzedSerializer(serializers.Serializer):
    effects = serializers.ListField(child=EffectWithIntensitySerializer())
    side_effects = serializers.ListField(child=SideEffectSerializer())
    recoms = serializers.ListField(child=RecomSerializer())
    # ingrs = serializers.ListField(child=IngrResSerializerShort())
    combs = serializers.ListField(child=CombWithTypeSerializer())
    data = ProductDataSerializer()
