from rest_framework.decorators import action


from rest_framework.views import APIView
from rest_framework.response import Response
from ext import Code
from api import models

from api.serializers.testSerializers import QuesKindSerializer,QuesSerializer,AnswerSerializer,CertifySerializer,PaperSerializer,ExamSerializer



code=Code.SUCCESS_CODE
msg=''


#根据题型id删除题型
class DeleteQuesKindByQuesKindIdView(APIView):
    def delete(self, request):
        qkId=request.query_params.dict().get("quesKindId")
        qkid_obj=models.Ques_Kind.objects.filter(quesKindId=qkId).first()
        if not qkid_obj:
            code=Code.ERROR_CODE
            msg='该试题类型不存在，请检查quesKindId'
            data={}
        else:
            ser=QuesKindSerializer(instance=qkid_obj)
            qkid_obj.delete()
            code=Code.SUCCESS_CODE
            msg='删除成功'
            data=ser.data
        context = {'code': code, 'msg': msg, 'data': data}
        return Response(context)



#根据试题id删除试题
class DeleteQuesByQuesIdView(APIView):
    def delete(self, request):
        qId = request.query_params.dict().get("quesId")
        qid_obj = models.Ques.objects.filter(quesId=qId).first()
        if not qid_obj:
            code = Code.ERROR_CODE
            msg = '该试题不存在，请检查quesId'
            data = {}
        else:
            ser = QuesSerializer(instance=qid_obj)
            qid_obj.delete()
            code = Code.SUCCESS_CODE
            msg = '删除成功'
            data = ser.data
        context = {'code': code, 'msg': msg, 'data': data}
        return Response(context)


#根据试卷id删除试卷
class DeletePaperByPaperIdView(APIView):
    def delete(self, request):
        papId = request.query_params.dict().get("paperId")
        pap_obj = models.Paper.objects.filter(paperId=papId).first()
        if not pap_obj:
            code = Code.ERROR_CODE
            msg = '该试卷不存在，请检查paperId'
            data = {}
        else:
            ser = PaperSerializer(instance=pap_obj)
            pap_obj.delete()
            code = Code.SUCCESS_CODE
            msg = '删除成功'
            data = ser.data
        context = {'code': code, 'msg': msg, 'data': data}
        return Response(context)

#根据考试id删除考试
class DeleteExamByExamIdView(APIView):
    def delete(self, request):
        exId = request.query_params.dict().get("examId")
        ex_obj = models.Exam.objects.filter(examId=exId).first()
        if not ex_obj:
            code = Code.ERROR_CODE
            msg = '该考试不存在，请检查examId'
            data = {}
        else:
            ser = ExamSerializer(instance=ex_obj)
            ex_obj.delete()
            code = Code.SUCCESS_CODE
            msg = '删除成功'
            data = ser.data
        context = {'code': code, 'msg': msg, 'data': data}
        return Response(context)


#根据答题id删除答题模型
class DeleteAnswerByAnswerIdView(APIView):
    def delete(self, request):
        asId = request.query_params.dict().get("answerId")
        as_obj = models.Answer.objects.filter(answerId=asId).first()
        if not as_obj:
            code = Code.ERROR_CODE
            msg = '该答题不存在，请检查answerId'
            data = {}
        else:
            ser = AnswerSerializer(instance=as_obj)
            as_obj.delete()
            code = Code.SUCCESS_CODE
            msg = '删除成功'
            data = ser.data
        context = {'code': code, 'msg': msg, 'data': data}
        return Response(context)
