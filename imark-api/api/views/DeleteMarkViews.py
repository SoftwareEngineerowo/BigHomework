from api import models
from rest_framework.views import APIView
from rest_framework.response import Response
from ext import Code

from api.serializers.markSerializers import MarkSerializer,MarkResultSerializer,PaperScoreSheetSerializer

code=Code.SUCCESS_CODE
msg=''

#根据id删除单题打分结果
class DeleteMarkResultByIdView(APIView):
    def delete(self,request):
        id = request.query_params.dict().get("id")
        mr_obj = models.Mark_result.objects.filter(id=id).first()
        if not mr_obj:
            code = Code.ERROR_CODE
            msg = '该id对应打分结果不存在，请检查id'
            data = {}
        else:
            ser = MarkResultSerializer(instance=mr_obj)
            data=ser.data
            mr_obj.delete()
            code = Code.SUCCESS_CODE
            msg = '删除成功'
        context = {'code': code, 'msg': msg, 'data': data}
        return Response(context)



#根据markId删除阅卷任务
class DeleteMarkByMarkId(APIView):
    def delete(self,request):
        markId=request.query_params.dict().get("markId")
        m_obj=models.Mark.objects.filter(markId=markId).first()
        if not m_obj:
            code = Code.ERROR_CODE
            msg = '该markId对应阅卷任务不存在，请检查markId'
            data = {}
        else:
            ser = MarkSerializer(instance=m_obj)
            data=ser.data
            m_obj.delete()
            code = Code.SUCCESS_CODE
            msg = '删除成功'
        context = {'code': code, 'msg': msg, 'data': data}
        return Response(context)


