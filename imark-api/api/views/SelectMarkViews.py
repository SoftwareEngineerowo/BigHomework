from django.core import serializers

from api import models
from rest_framework.views import APIView
from rest_framework.response import Response
from ext import Code
from django.db import connection

from api.serializers.markSerializers import MarkSerializer,MarkResultSerializer,PaperScoreSheetSerializer

code=Code.SUCCESS_CODE
msg=''

#教师查询阅卷题目
class SelectMarkBySysIdView(APIView):
    def get(self, request):
        f_examId = request.query_params.dict().get("examId")
        f_paperId = request.query_params.dict().get("paperId")
        f_obj=models.Mark.objects.filter(examId=f_examId,paperId=f_paperId).first()
        f_sysId = request.query_params.dict().get("sysId")
        if not f_obj:
            code=Code.ERROR_CODE
            msg="该阅卷任务不存在，请检查examId和paperId"
            data={"sysId":f_sysId,"examId":f_examId,"paperId":f_paperId}
        else:
            tasList=[]
            for i in f_obj.taskAllos:
                if (i!='[') and (i!=',') and  (i!=']') :
                    tasList.append(i)

            taNum=[] #保存该老师需要批阅的题目序号
            for index,taId in enumerate(tasList):
                if taId == f_sysId:
                    taNum.append(index+1)

            NeedMarkQuesIds=[]  #保存需要该老师批阅的题目id

            AllquesIds=[] #该试卷所有题目id
            f_quesIds=models.Paper.objects.filter(paperId=f_paperId).first().quesIds
            for queId in f_quesIds:
                if (queId!="[") and (queId!=',') and (queId!=']'):
                    AllquesIds.append(queId)

            for ta in taNum:
                NeedMarkQuesIds.append(AllquesIds[int(ta)-1])

            code = Code.SUCCESS_CODE
            msg = "教师查询阅卷题目成功"
            data={"sysId":f_sysId,
                  "examId":f_examId,
                  "paperId":f_paperId,
                  "NeedMarkQuesIds":NeedMarkQuesIds}
        context = {'code': code, 'msg': msg, 'data': data}
        return Response(context)

#根据answerId查询单题打分结果
class SelectMarkResultByAnswerIdView(APIView):
    def get(self,request):
        answerId = request.query_params.dict().get("answerId")
        ac_obj=models.Mark_result.objects.filter(answerId=answerId)
        ser=MarkResultSerializer(instance=ac_obj,many=True)
        code=Code.SUCCESS_CODE
        msg='查询成功'
        data=ser.data
        context = {'code': code, 'msg': msg, 'data': data}
        return Response(context)



#根据examId查询所有学生成绩
class SelectAllScoreByExamIdView(APIView):
    def get(self,request):
        examId = request.query_params.dict().get("examId")
        ex_obj=models.Certify.objects.filter(examId=examId).first()
        if not ex_obj:
            code=Code.ERROR_CODE
            msg='该examId对应的考试在Certify表中不存在，请检查'
            data={}
        else:
            sql1 = 'SELECT cert.examId,cert.certId,cert.stuId,cert.stuName,pss.paperId,pss.finalScore'
            sql2 = 'FROM `api_certify` as cert,`api_paper_score_sheet` as pss'
            sql3 = 'WHERE cert.examId=pss.examId AND cert.certId=pss.certId'
            sql4 = 'AND cert.examId="{}"'.format(examId)
            sql = sql1 + ' ' + sql2 + ' ' + sql3 + ' ' + sql4

            cursor = connection.cursor()
            cursor.execute(sql)
            rows = list(cursor.fetchall())
            cursor.close()
            data = rows
            msg='多表级联查询成功'
            code=Code.SUCCESS_CODE
        context = {'code': code, 'msg': msg, 'data': data}
        return Response(context)
