from ..serializers import *
# from ..models import *
from .repository_service import *
from .product_analyzer import ProductAnalyzer, IngredientInfo, IngredientFilter, ProductComparison


class VKRService:
    def __init__(self):
        pass

    def make_to_analyze(self, record_id) -> ToAnalyzeSerializer:
        record = get_record_by_id(id=record_id)
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
        return ToAnalyzeSerializer(data=data)

    def make_to_compare(self, record_id1, record_id2):
        to_compare1 = None
        to_compare2 = None
        to_analyze1 = self.make_to_analyze(record_id1)
        if to_analyze1.is_valid():
            to_compare1 = to_analyze1.data
        to_analyze2 = self.make_to_analyze(record_id2)
        if to_analyze2.is_valid():
            to_compare2 = to_analyze2.data
        data = {
            'to_compare1': to_compare1,
            'to_compare2': to_compare2
        }
        return data


    def post_record(self, to_analyze: ToAnalyzeSerializer, user: User = None) -> int:
        ingr_list = ''
        conc_list = ''
        for ingr in to_analyze['ingrs']:
            ingr_list += ingr['ingr_name']
            ingr_list += ', '
            conc_list += ingr['concentration']
            conc_list += ', '
        ingr_list = ingr_list[:-2]
        conc_list = conc_list[:-2]
        return add_record_now(user=user, ingr_list=ingr_list, conc_list=conc_list)

    def get_analysis_by_record_id(self, record_id: int) -> AnalyzedSerializer:
        to_analyze_serializer = self.make_to_analyze(record_id=record_id)
        if to_analyze_serializer.is_valid():
            analyzer = ProductAnalyzer(to_analyze_serializer)
            return analyzer.get_result()

    def delete_record_by_id(self, record_id) -> None:
        delete_record_by_id(record_id)

    def get_all_ingr_names(self) -> AllNamesSerializer:
        all_ingr_names = get_all_ingredient_names()
        return AllNamesSerializer(data={'ingr_names': all_ingr_names})

    def get_records(self, user_id, option) -> AllRecordsSerializer:
        all_records_serializer = []
        all_records = None
        if option == 'history':
            all_records = get_all_records_by_user_id(user_id)
        elif option == 'favorites':
            all_records = get_favorites_by_user_id(user_id)

        for record in all_records:
            record_id = record.id
            to_analyze = self.make_to_analyze(record_id)
            if to_analyze.is_valid():
                pass
                # print(to_analyze.data)
            date_time = record.datetime
            favorite = record.favorite
            # brand_name = record.brand_name
            # product_name = record.product_name
            data = {
                'record_id': record_id,
                'favorite': favorite,
                'ingrs': to_analyze.data,
                'date_time': date_time,
                # 'brand_name': brand_name,
                # 'product_name': product_name,
            }
            all_records_serializer.append(data)
        data = {
            'records': all_records_serializer
        }
        return AllRecordsSerializer(data=data)

    def get_ingredient_info(self, ingr_name: str) -> IngrResSerializerLong:
        ingr_info = IngredientInfo()
        return ingr_info.get_result(ingr_name)

    def filter_ingredients(self, ingr_name: str, ingr_effect: str) -> IngrListSerializer:
        ingr_filter = IngredientFilter()
        return ingr_filter.get_result(ingr_name, ingr_effect)

    def ingredient_search(self) -> IngrListSerializer:
        ingr_filter = IngredientFilter()
        return ingr_filter.get_list()

    def post_two_records(self, to_compare: ToCompareSerializer, user: User = None) -> (int, int):
        record_id1 = self.post_record(to_compare['to_compare1'], user)
        record_id2 = self.post_record(to_compare['to_compare2'], user)
        return record_id1, record_id2

    def get_comparison_by_record_ids(self, record_id1: int, record_id2: int) -> ComparedSerializer:
        to_compare = self.make_to_compare(record_id1, record_id2)
        comparison = ProductComparison(to_compare)
        return comparison.get_result()

    def change_record_status(self, record_id: int):
        change_record_status(record_id)
        return



