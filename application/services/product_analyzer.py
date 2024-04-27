from typing import List
from ..serializers import *
from ..models import *
from .repository_service import *

CONCENTRATIONS = ['High', 'Medium', 'Low']

# 13 pregnant
# 5 allergy
class ProductAnalyzer:
    def __init__(self, to_analyze=ToAnalyzeSerializer):
        self.ingredients = to_analyze.data
        self.quantity = 0
        self.high_conc = 0
        self.medium_conc = 0
        self.ingr_names = []
        self.concs = []
        self.ingr_types = []
        self.incis = []
        self.effects_list = []
        self.inci_effects_list = []
        self.side_effects = []
        self.all_features = []
        self.commons_serializer = None
        pass

    ingredients = List[(str, float)]
    analyzed_serializer = AnalyzedSerializer
    commons_serializer = ProductDataSerializer
    ingr_names = []
    ingr_types = []
    incis = List[Inci]
    concs = List[str]
    # features = List[Feature]
    # inci_features = List[(Inci, Feature)]

    # список эффектов и соответствующих им компонентов
    effects_list = List[Feature]
    inci_effects_list = List[List[Inci]]

    # список побочек и соответствующих им компонентов
    side_effects_list = List[Feature]
    inci_side_effects_list = List[List[Inci]]
    # effects = List[(str, Feature, List[Inci])]
    # effects_res = List[(str, str, str)]
    side_effects = List[(Feature, List[Inci])]
    recoms = List[str]

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
    def get_specific_concentrations(self, inci: Inci, conc: float) -> None:
        if conc is None:
            return

        conc_var = get_conc_by_inci(inci)
        inci_index = self.incis.index(inci)
        if conc_var is None:
            return

        if conc > conc_var[1]:
            if self.concs[inci_index] == CONCENTRATIONS[0]:
                return
            else:
                for i in range(self.medium_conc, inci_index):
                    self.concs[i] = CONCENTRATIONS[0]
                    return

        if conc > conc_var[2]:
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

        if conc <= conc_var[2]:
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
            ingr_name = ingredient[0]
            ingr_conc = ingredient[1]
            self.ingr_names.append(ingr_name)
            inci = get_inci_by_ingredient_name(ingr_name)
            if inci is not None:
                self.incis.append(inci)
                if ingr_conc is not None:
                    self.get_specific_concentrations(inci, ingr_conc)
                else: pass
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
        for side_effect in self.side_effects:
            if side_effect[0].id == feature.id:
                list_incis = side_effect[1]
                list_incis.append(inci)
                side_effect_new = (side_effect[0], list_incis)
                self.side_effects.remove(side_effect)
                self.side_effects.append(side_effect_new)
                return True
        return False


    def get_common_info(self) -> None:
        # vegan, natural, pregnant, hypoal
        commons = [True, True, True, True]

        # характеристики всего средства
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
                    
        common_0 = ''
        common_1 = ''
        common_2 = ''
        common_3 = ''
        
        if commons[0] is True:
            common_0 = 'Веганское (не содержит компонентов животного происхождения)'
        else:
            common_0 = 'Не веганское (содержит компонент(ы) животного происхождения)'

        if commons[1] is True:
            common_1 = 'Натуральное (не содержит компонентов синтетического происхождения)'
        else:
            common_1 = 'Не натуральное (содержит компонент(ы) синтетического происхождения)'

        if commons[2] is True:
            common_2 = 'Безопасно для беременных'
        else:
            common_2 = 'Не безопасно для беременных'

        if commons[3] is True:
            common_3 = 'Гипоаллергенное'
        else:
            common_3 = 'Не гипоаллергенное'
            
        common_data = {
            'vegan': common_0,
            'natural': common_1,
            'pregnant': common_2,
            'hypoallergenic': common_3
        }
        
        self.commons_serializer = ProductDataSerializer(common_data)

    def get_effects(self) -> None:
        conc = ''
        for i in range(0, self.quantity):
            inci = self.incis[i]
            if i <= self.high_conc:
                conc = CONCENTRATIONS[0]
            elif i <= self.medium_conc:
                conc = CONCENTRATIONS[1]
            else:
                conc = CONCENTRATIONS[2]

            features = get_features_by_inci(inci)
            if features is not None:
                for feature in features:
                    if feature.benefit is True:
                        add_new_effect = self.check_effect_duplicating(feature, inci)
                        if add_new_effect
        pass



        
                    
                        



