from django.db.models.functions import Substr
from django.shortcuts import render, redirect
from snsP.my_settings import *
from django.http import HttpResponse
from django.db.models import Q,Subquery
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView, UpdateAPIView, DestroyAPIView

class ServiceViewSet(APIView):
    def get(self, request, **kwargs):
        res_data = {
            "success": True,
            "error": None
        }
        print(request.GET.get('fbclid'))
        return Response(res_data, status=200)


class PrivacyPolicyViewSet(APIView):
    def get(self, request, **kwargs):
        res_data = {
            "success": True,
            "error": None
        }

        return Response(res_data, status=200)