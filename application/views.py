from django.shortcuts import render
from django.urls import path
from django.http import HttpResponse
from django.shortcuts import redirect
from rest_framework.generics import CreateAPIView, RetrieveDestroyAPIView, GenericAPIView
from rest_framework.renderers import JSONRenderer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

from .serializers import *
from .services.vkr_service import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

authentication_classes = (TokenAuthentication,)
# permission_classes = (IsAuthenticated,)

service = VKRService()

# Create your views here.
@api_view(['GET'])
def home(request):
  return HttpResponse('TRALALA')


# @permission_classes([IsAuthenticated])
# def post_record(to_analyze: ToAnalyzeSerializer, user: User) -> dict:
#     res = service.post_record(to_analyze, user.id)
#     data = {
#         'user_id': res[1],
#         'record_id': res[0]
#     }
#     return data

@permission_classes([IsAuthenticated])
@api_view(['GET'])
def get_email(request) -> Response:
    return Response(request.user.email, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_all_ingr_names(request) -> Response:
    serializer = service.get_all_ingr_names()
    if serializer.is_valid():
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class GetAnalysis(GenericAPIView):
#     serializer_class = AnalyzedSerializer
#     renderer_classes = [JSONRenderer]
#
#     def post(self, request: Request, to_analyze: ToAnalyzeSerializer) -> Response:
#         """ Получение одного заказа по идентификатору """
#         response = service.get_analysis(to_analyze)
#         if response:
#             return Response(data=response.data)
#         return Response(response.errors, status=status.HTTP_400_BAD_REQUEST)
@api_view(['POST'])
def analyze(request):
    serializer = request.data
    if serializer.is_valid():
        if request.user.is_authenticated:
            res = service.post_record(serializer.validated_data, request.user)
            # return Response(res, status=status.HTTP_200_OK)
        else:
            res = service.post_record(serializer.validated_data)
            # return Response(res, status=status.HTTP_200_OK)
        return redirect('get_analysis/', record_id=res)
    # return redirect('home/')
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class Analyze(GenericAPIView):
    serializer_class = ToAnalyzeSerializer
    renderer_classes = [JSONRenderer]

    def post(self, request: Request) -> Response:
        """ Создать запись для анализа """
        serializer = ToAnalyzeSerializer(data=request.data)
        if serializer.is_valid():
            if request.user.is_authenticated:
                res = service.post_record(serializer.validated_data, request.user)
                # return Response(res, status=status.HTTP_200_OK)
            else:
                res = service.post_record(serializer.validated_data)
                # return Response(res, status=status.HTTP_200_OK)
            new_url = 'get_analysis/' + str(res)
            return redirect(new_url)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetAnalysis(GenericAPIView):
    serializer_class = AnalyzedSerializer
    renderer_classes = [JSONRenderer]

    def get(self, request: Request, record_id: int) -> Response:
        """ Создать запись для анализа """
        analyzed = service.get_analysis_by_record_id(record_id)
        if not request.user.is_authenticated:
            service.delete_record_by_id(record_id)
        return Response(analyzed.data, status=status.HTTP_200_OK)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PutDelRecord(GenericAPIView):
    serializer_class = RecordSerializer
    permission_classes = [IsAuthenticated]
    renderer_classes = [JSONRenderer]

    # def get(self, request: Request, record_id: int) -> Response:
    #     return redirect('http://127.0.0.1:8000/analyze/get_analysis/' + str(record_id))

    def delete(self, request: Request, option: str, record_id: int) -> Response:
        service.delete_record_by_id(record_id)
        return Response(status=status.HTTP_200_OK)

    def put(self, request: Request, option: str, record_id: int) -> Response:
        service.change_record_status(record_id)
        return Response(status=status.HTTP_200_OK)

# @permission_classes([IsAuthenticated])
# @api_view(['DELETE'])
# def delete_record(request: Request, option: str, record_id: int) -> Response:
#     service.delete_record_by_id(record_id)
#     return Response(status=status.HTTP_200_OK)
#
# @permission_classes([IsAuthenticated])
# @api_view(['PUT'])
# def change_record_status(request: Request, option: str, record_id: int) -> Response:
#     service.change_record_status(record_id)
#     return Response(status=status.HTTP_200_OK)
    # return redirect('http://127.0.01:8000/profile/' + option)


@permission_classes([IsAuthenticated])
@api_view(['GET'])
def get_records(request: Request, option) -> Response:
    user_id = request.user.id
    all_records = service.get_records(user_id, option)
    if all_records.is_valid():
        return Response(all_records.data, status=status.HTTP_200_OK)
    return Response(all_records.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_ingredient_info(request: Request, ingr_name: str) -> Response:
    ingr_info = service.get_ingredient_info(ingr_name)
    if ingr_info.is_valid():
        return Response(ingr_info.data, status=status.HTTP_200_OK)
    return Response(ingr_info.errors, status=status.HTTP_400_BAD_REQUEST)


class IngredientSearch(GenericAPIView):
    serializer_class = IngrListSerializer
    renderer_classes = [JSONRenderer]

    def get(self, request: Request) -> Response:
        ingr_list = service.ingredient_search()
        if ingr_list.is_valid():
            # new_url = 'get_analysis/' + str(res)
            return Response(ingr_list.data, status=status.HTTP_200_OK)
        return Response(ingr_list.errors, status=status.HTTP_400_BAD_REQUEST)

# class FilterResult(GenericAPIView):
#     serializer_class = IngrListSerializer
#     renderer_classes = [JSONRenderer]
#
#     def get(self, request: Request, ingr_name: str, effect: str) -> Response:
#         ingr_list = service.filter_ingredients(ingr_name, effect)
#         if ingr_list.is_valid():
#             # new_url = 'get_analysis/' + str(res)
#             return redirect(ingr_list.data, status=status.HTTP_200_OK)
#         return Response(ingr_list.errors, status=status.HTTP_400_BAD_REQUEST)


class Compare(GenericAPIView):
    serializer_class = ToCompareSerializer
    renderer_classes = [JSONRenderer]

    def post(self, request: Request) -> Response:
        """ Создать записи для сравнения """
        serializer = ToCompareSerializer(data=request.data)
        if serializer.is_valid():
            if request.user.is_authenticated:
                res = service.post_two_records(serializer.validated_data, request.user)
                # return Response(res, status=status.HTTP_200_OK)
            else:
                res = service.post_two_records(serializer.validated_data)
                # return Response(res, status=status.HTTP_200_OK)
            new_url = 'get_comparison/' + str(res[0]) + '/' + str(res[1])
            return redirect(new_url)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetComparison(GenericAPIView):
    serializer_class = ComparedSerializer
    renderer_classes = [JSONRenderer]

    def get(self, request: Request, record_id1: int, record_id2: int) -> Response:
        """ Создать запись для анализа """
        compared = service.get_comparison_by_record_ids(record_id1, record_id2)
        if not request.user.is_authenticated:
            service.delete_record_by_id(record_id1)
            service.delete_record_by_id(record_id2)
        if compared.is_valid():
            return Response(compared.data, status=status.HTTP_200_OK)
        return Response(compared.errors, status=status.HTTP_400_BAD_REQUEST)
