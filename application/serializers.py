from rest_framework import serializers
from rest_framework.fields import ListField

# from .models import *

COMBINATION = [("Yes", "Yes"),
               ("Carefully", "Carefully"),
               ("No", "No")]

# INTENSITY = [("Strong", "Strong"),
#              ("Medium", "Medium"),
#              ("Weak", "Weak")]

class AllNamesSerializer(serializers.Serializer):
    ingr_names = ListField(child=serializers.CharField(max_length=100, required=True))


class IngrSerializer(serializers.Serializer):
    ingr_name = serializers.CharField(max_length=100, required=True)
    concentration = serializers.CharField(max_length=10, required=False)

class ToAnalyzeSerializer(serializers.Serializer):
    ingrs = serializers.ListField(child=IngrSerializer())


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
    recognized = serializers.BooleanField(required=True)
    ingr_name = serializers.CharField(max_length=100, required=True)
    inci_name = serializers.CharField(max_length=100, required=False)
    description = serializers.CharField(max_length=200, required=False)
    type_name = serializers.CharField(max_length=100, required=False)
    effect = serializers.CharField(max_length=200, required=False)

class TypeSerializer(serializers.Serializer):
    type_name = serializers.CharField(max_length=100, required=False)
    type_description = serializers.CharField(max_length=200, required=False)

class IngrTypeSerializer(serializers.Serializer):
    concentration = serializers.CharField(max_length=100, required=False)
    type = serializers.ListField(child=TypeSerializer())

class IngrResSerializerLong(serializers.Serializer):
    inci_name = serializers.CharField(max_length=100, required=True)
    synonyms = AllNamesSerializer(required=True)
    source = serializers.CharField(max_length=100, required=False)
    vegan = serializers.CharField(max_length=100, required=False)
    types = serializers.ListField(child=IngrTypeSerializer(), required=False)
    effects = serializers.ListField(child=serializers.CharField(max_length=200), required=False)
    side_effects = serializers.ListField(child=serializers.CharField(max_length=200), required=False)

    # ... Название инси, синонимы, происхождение, веган, роль в косметике, полезные/не полезные свойства

class CombSerializer(serializers.Serializer):
    ingr_name = serializers.CharField(max_length=100, required=True)
    description = serializers.CharField(max_length=500, required=True)

class CombWithTypeSerializer(serializers.Serializer):
    comb_type = serializers.CharField(max_length=100, required=True)
    combination = serializers.ListField(child=CombSerializer())

class ProductDataSerializer(serializers.Serializer):
    #
    vegan = serializers.CharField(max_length=300, required=True)
    natural = serializers.CharField(max_length=300, required=True)
    pregnant = serializers.CharField(max_length=300, required=True)
    hypoallergenic = serializers.CharField(max_length=300, required=True)



class AnalyzedSerializer(serializers.Serializer):
    data = ProductDataSerializer()
    effects = serializers.ListField(child=EffectWithIntensitySerializer())
    side_effects = serializers.ListField(child=SideEffectSerializer())
    recoms = serializers.ListField(child=RecomSerializer())
    ingrs = serializers.ListField(child=IngrResSerializerShort())
    combs = serializers.ListField(child=CombWithTypeSerializer())

class RecordSerializer(serializers.Serializer):
    record_id = serializers.IntegerField(required=True)
    favorite = serializers.BooleanField(required=True)
    ingrs = ToAnalyzeSerializer(required=True)
    date_time = serializers.DateTimeField(required=True)
    # brand_name = serializers.CharField(max_length=100, required=False)
    # product_name = serializers.CharField(max_length=100, required=False)

class AllRecordsSerializer(serializers.Serializer):
    records = serializers.ListField(child=RecordSerializer())


class IngrNamesSerializer(serializers.Serializer):
    inci_id = serializers.IntegerField(required=True)
    inci_name = serializers.CharField(max_length=100, required=True)
    synonyms = ListField(child=serializers.CharField(max_length=100, required=True))
    effects = serializers.ListField(child=serializers.CharField(max_length=100), required=False)


class IngrListSerializer(serializers.Serializer):
    ingredients = serializers.ListField(child=IngrNamesSerializer())

# class IngrSearchSerializer(serializers.Serializer):
#     ingr_name = serializers.CharField(max_length=100, required=False)
#     ingr_effect = serializers.CharField(max_length=100, required=False)


