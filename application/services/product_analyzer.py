# from typing import List
from ..serializers import *
# from ..models import *
from .repository_service import *

CONCENTRATIONS = ['High', 'Medium', 'Low']

# 13 pregnant
# 5 allergy
class ProductAnalyzer:
    def __init__(self, to_analyze: ToAnalyzeSerializer):
        self.ingredients = to_analyze.data['ingrs']
        self.quantity = 0
        self.high_conc = 0
        self.medium_conc = 0
        self.ingr_names = []
        self.concs = []
        self.ingr_types = []
        self.incis = []
        self.effects_list = []
        self.inci_effects_list = []
        self.side_effects_list = []
        self.inci_side_effects_list = []
        # self.commons_serializer = None
        self.effects_serializers = []
        self.analyzed_serializer = None
        pass

    # ingredients = List[(str, float)]
    analyzed_serializer = AnalyzedSerializer
    commons_serializer = ProductDataSerializer
    # ingr_names = []
    # ingr_types = []
    # incis = List[Inci]
    # concs = List[str]

    # список эффектов и соответствующих им компонентов
    effects_list = List[Feature]
    inci_effects_list = List[List[Inci]]

    # список побочек и соответствующих им компонентов
    side_effects_list = List[Feature]
    inci_side_effects_list = List[List[Inci]]

    # effects_serializers = List[EffectWithIntensitySerializer]

    # общие концентрации компонентов
    def get_generic_concentrations(self) -> None:
        self.high_conc = self.quantity // 4
        self.medium_conc = self.high_conc + 1 + self.quantity // 3
        for i in range(0, self.quantity):
            if i <= self.high_conc:
                self.concs.append(CONCENTRATIONS[0])
            elif i <= self.medium_conc:
                self.concs.append(CONCENTRATIONS[1])
            else:
                self.concs.append(CONCENTRATIONS[2])

    # специфические концентрации (с учетом введенных данных,
    # сравнение с данными из бд, изменение списка
    def get_specific_concentrations(self, inci: Inci, conc: str) -> None:
        if conc is None or conc == '-1':
            return

        conc_var = get_conc_by_inci(inci)
        inci_index = self.incis.index(inci)
        if conc_var is None:
            return

        if float(conc) > conc_var[1]:
            if self.concs[inci_index] == CONCENTRATIONS[0]:
                return
            else:
                for i in range(self.medium_conc, inci_index):
                    self.concs[i] = CONCENTRATIONS[0]
                    return

        if float(conc) > conc_var[2]:
            if self.concs[inci_index] == CONCENTRATIONS[1]:
                return

            if self.concs[inci_index] == CONCENTRATIONS[0]:
                for i in range(inci_index, self.high_conc):
                    self.concs[i] = CONCENTRATIONS[1]
                    return
            else:
                for i in range(self.medium_conc + 1, inci_index):
                    self.concs[i] = CONCENTRATIONS[1]
                    return

        if float(conc) <= conc_var[2]:
            if self.concs[inci_index] == CONCENTRATIONS[2]:
                return

            else:
                for i in range(inci_index, self.medium_conc):
                    self.concs[i] = CONCENTRATIONS[2]
                    return

    # получение общих данных - списка инси-имен и концентраций
    def get_data(self) -> None:
        self.quantity = len(self.ingredients)
        self.get_generic_concentrations()
        for ingredient in self.ingredients:
            ingr_name = ingredient['ingr_name']
            ingr_conc = ingredient['concentration']
            self.ingr_names.append(ingr_name)
            inci = get_inci_by_ingredient_name(ingr_name)
            if inci is not None:
                self.incis.append(inci)
                if ingr_conc is not None:
                    self.get_specific_concentrations(inci, ingr_conc)
                else:
                    pass
            else:
                self.incis.append(None)
                pass

    def check_effect_duplicating(self, feature: Feature, inci: Inci) -> bool:
        for i in range(0, len(self.effects_list)):
            effect = self.effects_list[i]
            if effect.id == feature.id:
                self.inci_effects_list[i].append(inci)
                return True
        return False

    def check_side_effect_duplicating(self, feature: Feature, inci: Inci) -> bool:
        for i in range(0, len(self.side_effects_list)):
            side_effect = self.side_effects_list[i]
            if side_effect.id == feature.id:
                self.inci_side_effects_list[i].append(inci)
                return True
        return False

    # общие характеристики всего средства
    def get_common_info(self) -> None:
        # vegan, natural, pregnant, hypoal
        commons = [True, True, True, True]

        for inci in self.incis:
            if commons[0] is True and inci.vegan is False:
                commons[0] = False

            if commons[1] is True and inci.source != 'Натуральное происхождение':
                commons[1] = False

            features = get_features_by_inci(inci)
            if features is not None:
                for feature in features:
                    
                    if commons[2] is True and feature.id == 13:
                        commons[2] = False
                        
                    if commons[3] is True and feature.id == 5:
                        commons[3] = False
        #
        # common_0 = ''
        # common_1 = ''
        # common_2 = ''
        # common_3 = ''
        
        if commons[0]:
            common_0 = 'Веганское (не содержит компонентов животного происхождения)'
        else:
            common_0 = 'Не веганское (содержит компонент(ы) животного происхождения)'

        if commons[1]:
            common_1 = 'Натуральное (не содержит компонентов синтетического происхождения)'
        else:
            common_1 = 'Не натуральное (содержит компонент(ы) синтетического происхождения)'

        if commons[2]:
            common_2 = 'Безопасно для беременных'
        else:
            common_2 = 'Не безопасно для беременных'

        if commons[3]:
            common_3 = 'Гипоаллергенное'
        else:
            common_3 = 'Не гипоаллергенное'
            
        data = {
            'vegan': common_0,
            'natural': common_1,
            'pregnant': common_2,
            'hypoallergenic': common_3,
        }
        comm_serializer = ProductDataSerializer(data=data)
        self.commons_serializer = comm_serializer
        if not self.commons_serializer.is_valid():
            return None

    def get_effects(self) -> None:
        for inci in self.incis:
            features = get_features_by_inci(inci)
            if features is not None:
                for feature in features:
                    if feature.benefit is True:
                        add_new_effect = self.check_effect_duplicating(feature, inci)
                        if not add_new_effect:
                            self.effects_list.append(feature)
                            self.inci_effects_list.append([inci])
                    else:
                        add_new_side_effect = self.check_side_effect_duplicating(feature, inci)
                        if not add_new_side_effect:
                            self.side_effects_list.append(feature)
                            self.inci_side_effects_list.append([inci])
        pass

    def get_max_concentration(self, inci_list: List[Inci]) -> str:
        inci_indices = [self.incis.index(inci) for inci in inci_list]
        min_index = min(inci_indices)
        return self.concs[min_index]

    def check_same_ingredients(self, effect_with_intensity_list: dict) -> dict:
        intensity = effect_with_intensity_list["intensity"]
        effect_list = effect_with_intensity_list['effect_with_ingrs']
        only_effects_list = []
        only_ingrs_list = []
        for effect in effect_list:
            only_effects_list.append(effect['effect'])
            only_ingrs_list.append(effect['ingrs'])
        # print(only_effects_list)
        # print(only_ingrs_list)
        changed = False
        n = len(only_effects_list) - 1
        for i in range(0, n):
            for j in range(0, n):
                if i != j:
                    if only_ingrs_list[i] == only_ingrs_list[j]:
                        changed = True
                        # print('AAA')
                        only_effects_list[i] += ', ' + only_effects_list[j]
                        only_effects_list.pop(j)
                        only_ingrs_list.pop(j)
                        n -= 1
        if not changed:
            return effect_with_intensity_list

        n += 1
        new_effects_list = []
        for i in range(0, n):
            data = {
                'effect': only_effects_list[i],
                'ingrs': only_ingrs_list[i]
            }
            # print(data)
            new_effects_list.append(data)
        data = {
            'intensity': intensity,
            'effect_with_ingrs': new_effects_list
        }
        # print(data)
        # effect_with_intensity_list = data
        return data

    def make_effects_serializers(self) -> None:
        self.get_effects()
        effect_ingrs = []
        max_concs = []
        for i in range(0, len(self.effects_list)):
            effect = self.effects_list[i]
            inci_list = self.inci_effects_list[i]
            max_conc = self.get_max_concentration(inci_list)
            effect_text = effect.effect
            names_list = []
            for inci in inci_list:
                names_list.append(self.ingr_names[self.incis.index(inci)])
            data = {
                'effect': effect_text,
                'ingrs': names_list
            }
            effect_serializer = EffectSerializer(data=data)
            if not effect_serializer.is_valid():
                return None

            effect_ingrs.append(effect_serializer.data)
            max_concs.append(max_conc)

        weak_effects = []
        medium_effects = []
        strong_effects = []
        for i in range(0, len(effect_ingrs)):
            effect = effect_ingrs[i]
            # intensity = ''
            if max_concs[i] == CONCENTRATIONS[0]:
                strong_effects.append(effect)
                # intensity = 'Strong'
            elif max_concs[i] == CONCENTRATIONS[1]:
                medium_effects.append(effect)
                # intensity = 'Medium'
            elif max_concs[i] == CONCENTRATIONS[2]:
                weak_effects.append(effect)

        data_strong = {
            'intensity': 'Сильное действие:',
            'effect_with_ingrs': strong_effects
        }
        data_strong = self.check_same_ingredients(data_strong)
        data_medium = {
            'intensity': 'Среднее по силе действие:',
            'effect_with_ingrs': medium_effects
        }
        data_medium = self.check_same_ingredients(data_medium)
        data_weak = {
            'intensity': 'Слабое действие:',
            'effect_with_ingrs': weak_effects
        }
        data_weak = self.check_same_ingredients(data_weak)
        self.effects_serializers = [data_strong, data_medium, data_weak]
            #     intensity = 'Weak'
            # # print(intensity)
            # data = {
            #     'intensity': intensity,
            #     'effect_with_ingrs': effect
            # }
            # # print(data)
            # # effect_with_intensity = EffectWithIntensitySerializer(data=data)
            # self.effects_serializers.append(data)
            # print(self.effects_serializers)
            # if effect_with_intensity.is_valid():
            #     print(effect_with_intensity.data)
            #     self.effects_serializers.append(effect_with_intensity.data)
            #     print(self.effects_serializers)


    def get_result(self) -> AnalyzedSerializer:
        self.get_data()
        self.get_common_info()
        self.make_effects_serializers()
        data = {
            'data': self.commons_serializer.data,
            'effects': self.effects_serializers
        }
        return AnalyzedSerializer(data)





class VKRService:
    def __init__(self):
        pass

    # def get_analysis(self, to_analyze: ToAnalyzeSerializer) -> AnalyzedSerializer:
    #     analyzer = ProductAnalyzer(to_analyze)
    #     return analyzer.get_result()

    def post_temp_record(self, to_analyze: ToAnalyzeSerializer) -> int:
        ingr_list = ''
        conc_list = ''
        for ingr in to_analyze['ingrs']:
            ingr_list += ingr['ingr_name']
            ingr_list += ', '
            conc_list += ingr['concentration']
            conc_list += ', '
        return add_temp_record(ingr_list=ingr_list, conc_list=conc_list)

    def post_record(self, to_analyze: ToAnalyzeSerializer, user_id: int) -> List[int]:
        ingr_list = ''
        conc_list = ''
        for ingr in to_analyze['ingrs']:
            ingr_list += ingr['ingr_name']
            ingr_list += ', '
            conc_list += ingr['concentration']
            conc_list += ', '
        return add_record_now(id=user_id, ingr_list=ingr_list, conc_list=conc_list)

    def get_analysis(self, record_id: int) -> AnalyzedSerializer:
        record = get_temp_record_by_id(id=record_id)
        ingr_list = record.ingr_list.split(', ')
        conc_list = record.conc_list.split(', ')
        # to_analyze = List[dict]
        to_analyze = []
        for i in range(0, len(ingr_list)):
            data = {'ingr_name': ingr_list[i],
                    'concentration': conc_list[i]}
            to_analyze.append(data)
        data = {
            'ingrs': to_analyze,
        }
        to_analyze_serializer = ToAnalyzeSerializer(data=data)
        if to_analyze_serializer.is_valid():
            analyzer = ProductAnalyzer(to_analyze_serializer)
            return analyzer.get_result()
