# from typing import List
from ..serializers import *
# from ..models import *
from .repository_service import *

CONCENTRATIONS = ['High', 'Medium', 'Low']
COMBINATIONS = ['Yes', 'Carefully', 'No']

# 13 pregnant
# 5 allergy
class ProductAnalyzer:
    def __init__(self, to_analyze: ToAnalyzeSerializer):
        self.ingredients = to_analyze.data['ingrs']
        self.quantity = 0
        self.inci_quantity = 0
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
        self.commons_serializer = None
        self.effects_serializers = []
        self.side_effects_serializers = []
        self.analyzed_serializer = None
        self.recoms_serializers = []
        self.comb_serializers = []
        self.ingr_serializers = []
        pass

    # результат анализа
    analyzed_serializer = AnalyzedSerializer
    # общие сведения по продукту
    commons_serializer = ProductDataSerializer
    # эффекты средства
    effects_serializers = List[dict]
    # побочные эффекты средства
    side_effects_serializers = List[dict]
    # рекомендации по применению
    recoms_serializers = List[dict]
    # рекомендации по комбинированию
    comb_serializers = List[dict]
    # информация по компонентам
    ingr_serializers = List[dict]


    # список эффектов и соответствующих им компонентов
    effects_list = List[Feature]
    inci_effects_list = List[List[Inci]]

    # список побочек и соответствующих им компонентов
    side_effects_list = List[Feature]
    inci_side_effects_list = List[List[Inci]]

    # концентрации компонентов по умолчанию
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

    # специфические концентрации (с учетом введенных данных, сравнение с данными из бд, изменение списка
    def get_specific_concentrations(self, inci: Inci, conc: str) -> None:
        if inci is None or conc is None or conc == '0':
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

        if float(conc) > conc_var[0]:
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

        if float(conc) <= conc_var[0]:
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
                self.inci_quantity += 1
                self.incis.append(inci)
                if ingr_conc is not None:
                    self.get_specific_concentrations(inci, ingr_conc)
            else:
                self.incis.append(None)

    # проверка дублирования эффектов (если два компонента имеют один эффект, они относятся к одному эффекту)
    def check_effect_duplicating(self, feature: Feature, inci: Inci) -> bool:
        for i in range(0, len(self.effects_list)):
            effect = self.effects_list[i]
            if effect.id == feature.id:
                self.inci_effects_list[i].append(inci)
                return True
        return False

    # проверка дублирования побочек (тот же принцип)
    def check_side_effect_duplicating(self, feature: Feature, inci: Inci) -> bool:
        for i in range(0, len(self.side_effects_list)):
            side_effect = self.side_effects_list[i]
            if side_effect.id == feature.id:
                self.inci_side_effects_list[i].append(inci)
                return True
        return False

    # проверка дублирования рекомендаций при добавлении
    def check_recoms_duplicating(self, recom: Recommendation) -> bool:
        for recom_dict in self.recoms_serializers:
            if recom_dict['recom_text'] == recom.recom:
                return True
        return False

    #
    def filter_combs_by_min_value(self, combinations: List[dict]) -> List[dict]:
        n = len(combinations)
        for i in range(0, n):
            for j in range(0, n):
                if i != j:
                    if combinations[i]['ingr_name'] == combinations[j]:
                        comb_type_i = COMBINATIONS.index(combinations[i]['comb_type'])
                        comb_type_j = COMBINATIONS.index(combinations[j]['comb_type'])
                        if comb_type_i == comb_type_j:
                            combinations.pop(j)
                        elif comb_type_i > comb_type_j:
                            combinations.pop(j)
                        else:
                            combinations.pop(i)
                        n -= 1
        return combinations

    # общие характеристики всего средства
    def get_common_info(self) -> None:
        # vegan, natural, pregnant, hypoal
        commons = [True, None, True, True]
        naturals = 0

        for inci in self.incis:
            if inci is not None:
                if commons[0] is True and inci.vegan is False:
                    commons[0] = False

                if inci.source == 'Естественное происхождение':
                    naturals += 1

                features = get_features_by_inci(inci)
                if features is not None:
                    for feature in features:

                        if commons[2] is True and feature.id == 13:
                            commons[2] = False

                        if commons[3] is True and feature.id == 5:
                            commons[3] = False
        
        if commons[0]:
            common_0 = 'Веганское (не содержит компонентов животного происхождения)'
        else:
            common_0 = 'Не веганское (содержит компонент(ы) животного происхождения)'

        if commons[2]:
            common_2 = 'Безопасно для беременных'
        else:
            common_2 = 'Не безопасно для беременных'

        if commons[3]:
            common_3 = 'Гипоаллергенное'
        else:
            common_3 = 'Не гипоаллергенное'

        if self.inci_quantity == 0: self.inci_quantity = 1

        data = {
            'vegan': common_0,
            'natural': str(naturals/self.inci_quantity * 100),
            'pregnant': common_2,
            'hypoallergenic': common_3,
        }
        comm_serializer = ProductDataSerializer(data=data)
        self.commons_serializer = comm_serializer
        if not self.commons_serializer.is_valid():
            return None

    # получение списка всех эффектов и побочек без учета концентраций
    def get_effects(self) -> None:
        for inci in self.incis:
            if inci is not None:
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

    # получение максимальной концентрации компонента по отношению к эффекту
    def get_max_concentration(self, inci_list: List[Inci]) -> str:
        inci_indices = [self.incis.index(inci) for inci in inci_list]
        min_index = min(inci_indices)
        return self.concs[min_index]

    # # алгоритм для проверки того, обусловлены ли разные эффекты одинаковым набором ингредиентов
    # def check_same_ingredients_algorithm(self, effects_list: List, ingrs_list: List) -> (bool, List, List):
    #     changed = False
    #     n = len(effects_list) - 1
    #     for i in range(0, n):
    #         for j in range(0, n):
    #             if i != j:
    #                 if ingrs_list[i] == ingrs_list[j]:
    #                     changed = True
    #                     effects_list[i] += ', ' + effects_list[j]
    #                     effects_list.pop(j)
    #                     ingrs_list.pop(j)
    #                     n -= 1
    #     if not changed:
    #         return (False, effects_list, ingrs_list)
    #     else:
    #         return (True, effects_list, ingrs_list)
    # # проверка и конкатенация эффектов
    # def check_same_ingredients_for_effects(self, effect_with_intensity_list: dict) -> dict:
    #     intensity = effect_with_intensity_list['intensity']
    #     effect_list = effect_with_intensity_list['effect_with_ingrs']
    #     only_effects_list = []
    #     only_ingrs_list = []
    #     for effect in effect_list:
    #         only_effects_list.append(effect['effect'])
    #         only_ingrs_list.append(effect['ingrs'])
    #     changed = self.check_same_ingredients_algorithm(only_effects_list, only_ingrs_list)
    #     if changed[0] is False:
    #         return effect_with_intensity_list
    #     new_effects_list = []
    #     n = len(changed[1])
    #     only_effects_list = changed[1]
    #     only_ingrs_list = changed[2]
    #     for i in range(0, n):
    #         data = {
    #             'effect': only_effects_list[i],
    #             'ingrs': only_ingrs_list[i]
    #         }
    #         new_effects_list.append(data)
    #     data = {
    #         'intensity': intensity,
    #         'effect_with_ingrs': new_effects_list
    #     }
    #     return data

    # проверка и конкатенация побочек
    def check_same_ingredients_for_side_effects(self, side_effect_list: List[dict]) -> List[dict]:
        only_side_effects_list = []
        only_ingrs_list = []
        for side_effect in side_effect_list:
            only_side_effects_list.append(side_effect['side_effect'])
            only_ingrs_list.append(side_effect['ingrs'])
        changed = self.check_same_ingredients_algorithm(only_side_effects_list, only_ingrs_list)
        if changed[0] is False:
            return side_effect_list
        n = len(changed[1])
        only_side_effects_list = changed[1]
        only_ingrs_list = changed[2]
        new_side_effects_list = []
        for i in range(0, n):
            data = {
                'side_effect': only_side_effects_list[i],
                'ingrs': only_ingrs_list[i]
            }
            new_side_effects_list.append(data)
        return new_side_effects_list

    # создание списка выходных сериалайзеров эффектов
    def make_effects_serializers(self) -> None:
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
            effect_ingrs.append(data)
            max_concs.append(max_conc)

        all_effects = [[], [], []]
        for i in range(0, len(effect_ingrs)):
            effect = effect_ingrs[i]
            index_effect = CONCENTRATIONS.index(max_concs[i])
            all_effects[index_effect].append(effect)

        intensities = ['Сильное действие', 'Среднее действие', 'Слабое действие']
        all_effects_data = [{'intensity': intensities[i], 'effect_with_ingrs': all_effects[i]} for i in range(0, 3)]
        # for i in range(0, len(all_effects_data)):
        #     all_effects_data[i] = self.check_same_ingredients_for_effects(all_effects_data[i])
        self.effects_serializers = all_effects_data

    # создание списка выходных сериалайзеров побочек
    def make_side_effects_serializers(self) -> None:
        for i in range(0, len(self.side_effects_list)):
            side_effect = self.side_effects_list[i]
            inci_list = self.inci_side_effects_list[i]
            side_effect_text = side_effect.effect
            names_list = []
            for inci in inci_list:
                names_list.append(self.ingr_names[self.incis.index(inci)])
            data = {
                'side_effect': side_effect_text,
                'ingrs': names_list
            }
            side_effect_serializer = SideEffectSerializer(data=data)
            if not side_effect_serializer.is_valid():
                return None

            self.side_effects_serializers.append(side_effect_serializer.data)
        # self.side_effects_serializers = self.check_same_ingredients_for_side_effects(self.side_effects_serializers)

    # создание списка выходных сериалайзеров рекомендаций
    def make_recoms_serializers(self) -> None:
        for inci in self.incis:
            if inci is not None:
                recoms = get_all_recoms_by_inci(inci)
                if recoms is not None:
                    for recom in recoms:
                        add_new_recom = self.check_recoms_duplicating(recom)
                        if add_new_recom:
                            pass
                        else:
                            data = {
                                'recom_text': recom.recom,
                            }
                            self.recoms_serializers.append(data)

    #
    def make_comb_serializers(self) -> None:
        combinations = []
        for inci in self.incis:
            if inci is not None:
                combs = get_all_combs_by_inci(inci)
                if combs is not None:
                    for comb in combs:
                        data = {
                            'ingr_name': comb.inci_id_2.inci_name,
                            'comb_type': comb.comb_type,
                            'description': comb.combination
                        }
                        combinations.append(data)
        combinations = self.filter_combs_by_min_value(combinations)
        all_combs = [[], [], []]
        for comb in combinations:
            index_comb = COMBINATIONS.index(comb['comb_type'])
            all_combs[index_comb].append({'ingr_name': comb['ingr_name'], 'description': comb['description']})
        comb_types = ['Рекомендуется', 'Допустимо с осторожностью', 'Не рекомендуется']
        self.comb_serializers = [
            {'comb_type': comb_types[i], 'combination': all_combs[i]} for i in range(0, 3)
        ]

    #
    def make_ingredients_serializers(self):
        for i in range(0, self.quantity):
            inci = self.incis[i]
            inci_types = []
            if inci is not None:

                type_options = get_type_options_by_inci(inci)
                if len(type_options) == 1:
                    inci_types = [type_options[0].type_id.type_short]
                else:
                    for type_option in type_options:
                        if type_option.conc is None or type_option.conc == self.concs[i]:
                            inci_types.append(type_option.type_id.type_short)
            inci_name = ''
            if inci is not None:
                inci_name = 'INCI имя - ' + inci.inci_name

            description = ''
            if inci is not None:
                description = inci.description

            types_str = ''
            if len(inci_types) > 0:
                types_str += 'Используется как '
            if len(inci_types) == 1:
                types_str += inci_types[0]
            elif len(inci_types) == 2:
                types_str += inci_types[0] + ' и ' + inci_types[1]
            elif len(inci_types) > 2:
                for inci_type in inci_types:
                    if inci_type is not inci_types[-1]:
                        types_str += inci_type + ', '
                    else:
                        types_str = types_str[:-2]
                        types_str += ' и ' + inci_type

            effects_str = ''
            if inci is not None and check_if_active_by_inci(inci):
                effect_list = get_positive_features_by_inci(inci)
                for effect in effect_list:
                    effects_str += effect.effect + ', '
            if len(effects_str) > 0:
                effects_str = effects_str[:-2]
                effects_str = 'Эффект: ' + effects_str

            data = {
                'ingr_name': self.ingr_names[i],
                'inci_name': inci_name,
                'description': description,
                'type_name': types_str,
                'effect': effects_str
            }
            self.ingr_serializers.append(data)

    #
    def get_result(self) -> AnalyzedSerializer:
        self.get_data()
        self.get_common_info()
        self.get_effects()
        self.make_effects_serializers()
        self.make_side_effects_serializers()
        self.make_recoms_serializers()
        self.make_comb_serializers()
        self.make_ingredients_serializers()
        data = {
            'data': self.commons_serializer.data,
            'effects': self.effects_serializers,
            'side_effects': self.side_effects_serializers,
            'recoms': self.recoms_serializers,
            'combs': self.comb_serializers,
            'ingrs': self.ingr_serializers
        }
        return AnalyzedSerializer(data)





class IngredientInfo:
    def __init__(self):
        # self.ingr_name = ingr_name
        self.inci = None
        self.synonyms = None
        self.conc_list = []
        self.types_list = []
        self.effects_list = []
        self.side_effects_list = []
        self.source = None
        self.vegan = None

    conc_list = List[InciType]
    types_list = List[List[Type]]
    effects_list = List[Feature]
    side_effects_list = List[Feature]

    def get_synonyms(self, ingr_name: str):
        self.inci = get_inci_by_ingredient_name(ingr_name)
        if self.inci is None:
            self.inci = get_inci_by_name(ingr_name)
            if self.inci is None:
                return
        self.synonyms = [ingr.ingredient for ingr in get_all_ingredients_by_inci(self.inci)]
        self.source = self.inci.source
        if self.inci.vegan:
            self.vegan = "Веганский"
        else:
            self.vegan = "Животного происхождения"

    #
    def check_types_duplicating(self, inci_type: InciType, type: Type) -> bool:
        for i in range(0, len(self.conc_list)):
            type_conc = self.conc_list[i]
            if inci_type.conc == type_conc.conc:
                self.types_list[i].append(type)
                return True
        return False


    def get_types(self):
        if self.inci is None:
            return
        inci_types = get_type_options_by_inci(self.inci)
        types = get_types_by_inci(self.inci)
        for i in range(0, len(types)):
            add_new_type = self.check_types_duplicating(inci_types[i], types[i])
            if not add_new_type:
                self.conc_list.append(inci_types[i])
                self.types_list.append([types[i]])

    def get_all_effects(self):
        self.effects_list = get_features_by_inci(self.inci)
        self.side_effects_list = get_negative_features_by_inci(self.inci)

    def get_result(self, ingr_name: str) -> IngrResSerializerLong:
        self.get_synonyms(ingr_name)
        self.get_types()
        self.get_all_effects()

        types_with_conc = []
        for i in range(0, len(self.types_list)):
            types_with_descr = []
            for type in self.types_list[i]:
                data = {
                    'type_name': type.type_short,
                    'type_description': type.type_description
                }
                types_with_descr.append(data)

            conc = ''
            if self.conc_list[i].conc is None:
                conc = '0'
            elif self.conc_list[i].conc == 'High':
                conc = 'Высокая концентрация'
            elif self.conc_list[i].conc == 'Medium':
                conc = 'Средняя концентрация'
            elif self.conc_list[i].conc == 'Low':
                conc = 'Низкая концентрация'
            data = {
                'concentration': conc,
                'type': types_with_descr
            }
            types_with_conc.append(data)

        effects = []
        side_effects = []

        for effect in self.effects_list:
            if effect.benefit:
                effects.append(effect.effect)
            else:
                side_effects.append(effect.effect)

        ingr_names = {'ingr_names': self.synonyms}

        data = {
            'inci_name': self.inci.inci_name,
            'synonyms': ingr_names,
            'source': self.source,
            'vegan': self.vegan,
            'types': types_with_conc,
            'effects': effects,
            'side_effects': side_effects
        }

        return IngrResSerializerLong(data=data)





class IngredientFilter:
    def __init__(self):
        self.all_incis = []
        self.all_ingrs = []
        self.all_effects = []
        pass

    def get_all_ingredients(self):
        self.all_incis = get_all_inci()
        for inci in self.all_incis:
            ingrs = get_all_ingredients_by_inci(inci)
            self.all_ingrs.append([ingr.ingredient for ingr in ingrs])
            effects = get_positive_features_by_inci(inci)
            self.all_effects.append([effect.effect for effect in effects])

    def filter_ingredients(self, ingr_name: str, ingr_effect: str):
        for i in range(0, len(self.all_incis)):
            flag = True
            for ingr in self.all_ingrs[i]:
                if ingr_name in ingr.ingredient:
                    pass
                else:
                    flag = False
                if ingr_effect in self.all_effects[i]:
                    pass
                else:
                    flag = False
            if not flag:
                self.all_incis.pop(i)
                self.all_ingrs.pop(i)
                self.all_effects.pop(i)
                i -= 1

    def get_result(self, ingr_name: str, ingr_effect: str):
        self.get_all_ingredients()
        self.filter_ingredients(ingr_name, ingr_effect)
        ingrs = []
        for i in range(0, len(self.all_incis)):
            ingr_names = {'ingr_names': self.all_ingrs[i]}
            data = {
                'inci_name': self.all_incis[i].inci_name,
                'synonyms': ingr_names
            }
            ingrs.append(data)
        return IngrListSerializer(data={'ingredients': ingrs})

    def get_list(self):
        self.get_all_ingredients()
        ingrs = []
        effects = []
        for i in range(0, len(self.all_incis)):
            # ingr_names = {'ingr_names': self.all_ingrs[i]}
            data = {
                'inci_id': self.all_incis[i].id,
                'inci_name': self.all_incis[i].inci_name,
                'synonyms': self.all_ingrs[i],
                'effects': self.all_effects[i]
            }
            ingrs.append(data)

        return IngrListSerializer(data={'ingredients': ingrs})



