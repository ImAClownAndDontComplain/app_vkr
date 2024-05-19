from ..serializers import *
# from ..models import *
from .repository_service import *
from .product_analyzer import ProductAnalyzer

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

