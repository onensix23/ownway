from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from .models import *
from .serializers import *

from posts.models import *
from users.models import *

from users.serializers import *
# Create your views here.

class ReportTemplateViewSet(APIView):
    def get(self, request, **kwargs):
        get_queryset = ReportTemplate.objects.all()
        get_serializer_class = ReportTemplateSerializer(get_queryset, many=True)

        return Response(get_serializer_class.data, status=200)


class ReportViewSet(APIView):
    def get(self, request, **kwargs):
        get_queryset = ReportTemplate.objects.all()
        get_serializer_class = ReportTemplateSerializer(get_queryset, many=True)

        return Response(get_serializer_class.data, status=200)

    @method_decorator(csrf_exempt)
    def post(self, request, **kwargs):
        res_data = {
            'result' : None,
            'success' : True,
            'error' : None,
        }

        request_d = request.data; 

        try:
            from_id = request_d['from_id']
            fromObj = User.objects.get(username=from_id)

            r_type = request_d['type']
            reportTempObj = ReportTemplate.objects.get(rt_id=r_type)

            type_title = request_d['type_title']

            reportObj = Report(r_from=fromObj, r_type=reportTempObj, r_typetitle=type_title, )

            if type_title == 'u':
                to_id = request_d['to_id']
                toObj = User.objects.get(username=to_id)
                reportObj.r_to=toObj

            elif type_title == 'p': #post
                b_id = request.data['id']
                postObj = Posts.objects.get(b_id=b_id)
                reportObj.r_b_id = postObj
                reportObj.r_to = User.objects.get(username=postObj.id)

            elif type_title == 'c': #comment
                pc_id = request.data['id']
                postcommentObj = PostComment.objects.get(pc_id=pc_id)
                reportObj.r_to = User.objects.get(username=postcommentObj.id)
                reportObj.r_pc_id=postcommentObj

            elif type_title == 'i': #image
                p_id = request.data['id']
                photoObj = Photo.objects.get(p_id=p_id)
                reportObj.r_to = User.objects.get(username=postcommentObj.id)
                reportObj.r_p_id=photoObj

            elif type_title == 'pp': #postplace
                # print(request_d)
                pp_id = request.data['id']
                postplaceObj = PostPlace.objects.get(pp_id=pp_id)
                reportObj.r_pp_id=postplaceObj
                
                toObj = User.objects.get(username=postplaceObj.pp_user_id)
                reportObj.r_to=toObj

            if r_type == 11:
                report_text = request_d['report_text']
                reportObj.r_report_text = report_text

            reportObj.save()

        except Exception as e:
            res_data['error'] = e

        return Response(res_data, status=200)

