from api import models
from rest_framework.views import APIView
from rest_framework.response import Response
from ext import Code
import uuid

from api.serializers.markSerializers import MarkSerializer,MarkResultSerializer,PaperScoreSheetSerializer

code=Code.SUCCESS_CODE
msg=''



#添加阅卷任务
class AddMarkView(APIView):
    def post(self,request):
        ser=MarkSerializer(data=request.data)
        if ser.is_valid():
            #序列化验证通过，数据类型正确
            after_data = ser.validated_data  #将通过验证的json数据转化为字典
            fid_paperObj=models.Paper.objects.filter(paperId=after_data.get("paperId")).first() #查询该考试试卷是否存在
            fid_examObj=models.Exam.objects.filter(examId=after_data.get("examId")).first()
            fid_mark=models.Mark.objects.filter(paperId=after_data.get("paperId"),examId=after_data.get("examId")).first()
            taskAllos=after_data.get("taskAllos").replace('[','').replace(']','').split(',')
            if not fid_paperObj:
                code=Code.ERROR_CODE
                msg='添加阅卷任务失败,试卷不存在'
                data=after_data
            elif not fid_examObj:
                code = Code.ERROR_CODE
                msg = '添加阅卷任务失败,考试不存在'
                data = after_data
            elif fid_mark:
                code = Code.ERROR_CODE
                msg = '添加阅卷任务失败,该阅卷任务已经存在，请勿重复添加'
                data = after_data
            else:
                new_mark=models.Mark()
                markId=str(uuid.uuid1())
                new_mark.markId=markId
                new_mark.examId=after_data.get("examId")
                new_mark.paperId=after_data.get("paperId")
                new_mark.taskAllos=after_data.get("taskAllos")
                new_mark.save()
                code=Code.SUCCESS_CODE
                msg="添加阅卷任务成功"
                after_data["markId"]=markId
                after_data["taskAllos"]=taskAllos
                data=after_data
            context={'code':code,'msg':msg,'data':data}
        else:
            #序列化验证失败，数据不正确
            msg= ser.errors
            code=Code.ERROR_CODE
            data={}
            context={'code':code,'msg':msg,'data':data}
        return Response(context)
            
            
            


#添加打分结果
class MarkResultView(APIView):
    def post(self,request):
        ser=MarkResultSerializer(data=request.data)
        if ser.is_valid():
            # 序列化验证通过，数据类型正确
            after_data = ser.validated_data  # 将通过验证的json数据转化为字典
            id=str(uuid.uuid1())
            after_data["id"]=id
            a_ser=MarkResultSerializer(data=after_data)
            if a_ser.is_valid():
                a_ser.save()
                code=Code.SUCCESS_CODE
                msg='添加打分结果成功'
                data=after_data
            else:
                code=Code.ERROR_CODE
                msg="添加打分结果失败"
                data=after_data
        else:
            code=Code.ERROR_CODE
            msg=ser.errors
            data={}
        context = {'code': code, 'msg': msg, 'data': data}
        return Response(context)



#添加单卷分数
class AddSheetScoreView(APIView):
    def post(self,request):
        ser=PaperScoreSheetSerializer(data=request.data)
        if ser.is_valid():
            # 序列化验证通过，数据类型正确
            after_data = ser.validated_data  # 将通过验证的json数据转化为字典
            id=str(uuid.uuid1())
            after_data["id"]=id
            a_ser=PaperScoreSheetSerializer(data=after_data)
            if a_ser.is_valid():
                a_ser.save()
                code=Code.SUCCESS_CODE
                msg='添加单卷分数成功'
                data=after_data
            else:
                code=Code.ERROR_CODE
                msg="添加单卷分数失败"
                data=after_data
        else:
            code=Code.ERROR_CODE
            msg=ser.errors
            data={}
        context = {'code': code, 'msg': msg, 'data': data}
        return Response(context)



