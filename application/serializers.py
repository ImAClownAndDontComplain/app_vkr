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
    concentration = serializers.CharField(max_length=10, required=False, default='0')

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
    positive_effects = serializers.ListField(child=serializers.CharField(max_length=100))

class CommonCompareSerializer(serializers.Serializer):
    vegan1 = serializers.CharField(max_length=300, required=True)
    vegan2 = serializers.CharField(max_length=300, required=True)
    natural1 = serializers.CharField(max_length=300, required=True)
    natural2 = serializers.CharField(max_length=300, required=True)
    pregnant1 = serializers.CharField(max_length=300, required=True)
    pregnant2 = serializers.CharField(max_length=300, required=True)
    hypoallergenic1 = serializers.CharField(max_length=300, required=True)
    hypoallergenic2 = serializers.CharField(max_length=300, required=True)

class SharedEffectSerializer(serializers.Serializer):
    effect = serializers.CharField(max_length=300, required=False)
    intensity1 = serializers.CharField(max_length=300, required=False)
    ingrs1 = ListField(child=serializers.CharField(max_length=100))
    intensity2 = serializers.CharField(max_length=300, required=False)
    ingrs2 = ListField(child=serializers.CharField(max_length=100))

class SharedSideEffectSerializer(serializers.Serializer):
    side_effect = serializers.CharField(max_length=300, required=False)
    ingrs1 = ListField(child=serializers.CharField(max_length=100))
    ingrs2 = ListField(child=serializers.CharField(max_length=100))

class UniqueEffectSerializer(serializers.Serializer):
    effect = serializers.CharField(max_length=300, required=False)
    intensity = serializers.CharField(max_length=300, required=False)
    ingrs = ListField(child=serializers.CharField(max_length=100))

class UniqueSideEffectSerializer(serializers.Serializer):
    side_effect = serializers.CharField(max_length=300, required=False)
    ingrs = ListField(child=serializers.CharField(max_length=100))

class SharedIngredientsSerializer(serializers.Serializer):
    recognized = serializers.BooleanField(required=True)
    ingr_name1 = serializers.CharField(max_length=100, required=False)
    ingr_name2 = serializers.CharField(max_length=100, required=False)
    inci_name = serializers.CharField(max_length=100, required=False)
    description = serializers.CharField(max_length=200, required=False)
    # type_name = serializers.CharField(max_length=100, required=False)
    # effect = serializers.CharField(max_length=200, required=False)

class ToCompareSerializer(serializers.Serializer):
    to_compare1 = ToAnalyzeSerializer(required=False)
    to_compare2 = ToAnalyzeSerializer(required=False)

class ComparedRecognizedSerializer(serializers.Serializer):
    ingr_name = serializers.CharField(max_length=100, required=False)
    recognized = serializers.BooleanField()

class IngrCompareSerializerShort(serializers.Serializer):
    recognized = serializers.BooleanField(required=True)
    ingr_name = serializers.CharField(max_length=100, required=True)
    inci_name = serializers.CharField(max_length=100, required=False)
    description = serializers.CharField(max_length=200, required=False)

class ComparedSerializer(serializers.Serializer):
    ingrs1 = serializers.ListField(child=ComparedRecognizedSerializer())
    ingrs2 = serializers.ListField(child=ComparedRecognizedSerializer())
    data = CommonCompareSerializer()
    shared_effects = serializers.ListField(child=SharedEffectSerializer())
    unique_effects1 = serializers.ListField(child=UniqueEffectSerializer())
    unique_effects2 = serializers.ListField(child=UniqueEffectSerializer())

    shared_side_effects = serializers.ListField(child=SharedSideEffectSerializer())
    unique_side_effects1 = serializers.ListField(child=UniqueSideEffectSerializer())
    unique_side_effects2 = serializers.ListField(child=UniqueSideEffectSerializer())

    shared_ingredients = serializers.ListField(child=SharedIngredientsSerializer(), required=False)
    unique_ingredients1 = serializers.ListField(child=IngrCompareSerializerShort(), required=False)
    unique_ingredients2 = serializers.ListField(child=IngrCompareSerializerShort(), required=False)

# class IngrSearchSerializer(serializers.Serializer):
#     ingr_name = serializers.CharField(max_length=100, required=False)
#     ingr_effect = serializers.CharField(max_length=100, required=False)


