from django.shortcuts import render
from django.urls import path
from django.http import HttpResponse
from rest_framework.generics import CreateAPIView, RetrieveDestroyAPIView, GenericAPIView
from rest_framework.renderers import JSONRenderer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

from .serializers import *
from .services.product_analyzer import *

service = VKRService()

# Create your views here.
def home(request):
  return HttpResponse('TRALALA')


@permission_classes([IsAuthenticated])
def post_record(to_analyze: ToAnalyzeSerializer, user: User) -> dict:
    res = service.post_record(to_analyze, user.id)
    data = {
        'user_id': res[1],
        'record_id': res[0]
    }
    return data

class GetAnalysis(GenericAPIView):
    serializer_class = AnalyzedSerializer
    renderer_classes = [JSONRenderer]

    def get(self, request: Request, record_id: int) -> Response:
        """ Получение одного заказа по идентификатору """
        response = service.get_analysis(record_id)
        if response:
            return Response(data=response.data)
        return Response(response.errors, status=status.HTTP_400_BAD_REQUEST)

# class PostTempRecord(GenericAPIView):
#     serializer_class = ToAnalyzeSerializer
#     renderer_classes = [JSONRenderer]
#
#     def post(self, request: Request) -> Response:
#         """ Создать запись для анализа """
#         return Response(data=request.user.is_authenticated, status=status.HTTP_200_OK)
#         # to_analyze = request.data
#         # try:
#         #     res = post_record(to_analyze, request.user)
#         #     return Response(data=res, status=status.HTTP_200_OK)
#         # # if not bool(request.user.is_authenticated):
#         # #     res = service.post_temp_record(to_analyze)
#         # #     return Response(data=res, status=status.HTTP_200_OK)
#         # # elif bool(request.user.is_authenticated):
#         # #     user_id = request.user.id
#         # #     res = service.post_record(to_analyze, user_id)
#         # #     data = {
#         # #         'user_id': res[1],
#         # #         'record_id': res[0]
#         # #     }
#         # #     return Response(data=data, status=status.HTTP_200_OK)
#         # except Exception as e:
#         #     res = service.post_temp_record(to_analyze)
#         #     return Response(data=res, status=status.HTTP_200_OK)


