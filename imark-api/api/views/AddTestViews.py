import uuid

from api import models
from rest_framework.views import APIView
from rest_framework.response import Response
from ext import Code
import  time

from api.serializers.testSerializers import QuesKindSerializer,QuesSerializer,AnswerSerializer,CertifySerializer,PaperSerializer,ExamSerializer


#添加试题类型
class AddQuesKindView(APIView):
    def post(self,request):
        ser=QuesKindSerializer(data=request.data)
        if ser.is_valid():
            #序列化验证通过，数据类型正确
            after_data = ser.validated_data  #将通过验证的json数据转化为字典
            fid_quesKindName=models.Ques_Kind.objects.filter(quesKindName=after_data.get("quesKindName")).first()#查询数据库中相同的quesKindName
            if not fid_quesKindName:
                newQuesKind=models.Ques_Kind()
                newQuesKind.quesKindName=after_data.get("quesKindName")
                newQuesKind.save()
                msg='试题类型添加成功'
                code=Code.SUCCESS_CODE
            else:
                msg='该题目类型已经存在'
                code=Code.ERROR_CODE
            f_qs = models.Ques_Kind.objects.filter(quesKindName=after_data.get("quesKindName")).first()
            after_data["quesKindId"] = f_qs.quesKindId
            context={'code':code,'msg':msg,'data':after_data}
        else:
            #序列化验证失败，数据不正确
            msg= ser.errors
            code=Code.ERROR_CODE
            data={}
            context={'code':code,'msg':msg,'data':data}
        return Response(context)
        

        
#添加试题
class AddQuesView(APIView):
    def post(self,request):
        ser=QuesSerializer(data=request.data)
        if ser.is_valid():
            #序列化验证通过，数据类型正确
            after_data = ser.validated_data  #将通过验证的json数据转化为字典
             #获取参数
            quesId=uuid.uuid1()
            quesKindId=after_data.get("quesKindId")
            quesKindName=models.Ques_Kind.objects.filter(quesKindId=quesKindId).first().quesKindName
            new_object=models.Ques()
            new_object.quesId=quesId
            new_object.quesKindId=quesKindId
            new_object.quesContent=after_data.get("quesContent")
            new_object.quesAnswer=after_data.get("quesAnswer")
            new_object.quesDefaultScore=after_data.get("quesDefaultScore")
            new_object.quesLevel=after_data.get("quesLevel")
            new_object.save() #保存到数据库
            n_qesId=models.Ques.objects.filter(quesId=quesId).first().quesId
            after_data["quesKindName"]=quesKindName
            after_data["quesId"] = n_qesId

            msg = '试题添加成功'
            code = Code.SUCCESS_CODE
            data=after_data
            context = {'code': code, 'msg': msg, 'data': data}
        else:
            #序列化验证失败，数据不正确
            msg= ser.errors
            code=Code.ERROR_CODE
            data={}
            context={'code':code,'msg':msg,'data':data}
        return Response(context)



#添加准考证
class AddCertifyView(APIView):
    def post(self,request):
        examId=request.data["examId"]
        ex_obj=models.Exam.objects.filter(examId=examId).first()
        if not ex_obj:
            code=Code.ERROR_CODE
            msg="该examId对应的考试不存在，请检查examId"
            data={}
        else:
            certs = request.data["certs"]
            for cer in certs:
                obj = models.Certify()
                obj.examId = examId
                obj.certId = cer["certId"]
                obj.stuId = cer["stuId"]
                obj.stuName = cer["stuName"]
                obj.save()
            code = Code.SUCCESS_CODE
            msg = '准考证添加成功'
            data=request.data
        context = {'code': code, 'msg': msg, 'data': data}
        return Response(context)




#添加试卷
class AddPaperView(APIView):
    def post(self,request):
        ser=PaperSerializer(data=request.data)
        if ser.is_valid():
            #序列化验证通过，数据类型正确
            after_data = ser.validated_data  #将通过验证的json数据转化为字典
            new_paperName=after_data.get("paperName")
            new_quesIds=after_data["quesIds"].replace('[','').replace(']','').split(',')
            new_quesKindIds = after_data["quesKindIds"].replace('[', '').replace(']', '').split(',')
            new_obj = models.Paper.objects.filter(paperName=new_paperName).first()
            if not new_obj : #若该试卷不存在
                new_paperId = uuid.uuid1()
                #获取试卷题型结构
                quesKindName=[]   #试卷题型list
                for quesKindId_paper in new_quesKindIds:
                    if models.Ques_Kind.objects.filter(quesKindId=quesKindId_paper).first().quesKindName not in quesKindName:
                        quesKindName.append(models.Ques_Kind.objects.filter(quesKindId=quesKindId_paper).first().quesKindName)
                #获取试卷包含试题
                flag=True
                erro_ques=""
                for quesId_paper in new_quesIds:
                        if not models.Ques.objects.filter(quesId=quesId_paper).first():
                            erro_ques = quesId_paper
                            flag=False
                if flag==False:
                    code=Code.ERROR_CODE
                    msg="ID为:--"+erro_ques+"--的试题不存在"
                    data=after_data
                else:
                    after_data["paperId"] = str(new_paperId)
                    after_data["paperStasus"]=0
                    n_ser=PaperSerializer(data=after_data)
                    if n_ser.is_valid():
                        n_ser.save() #保存到数据库
                        msg='试卷添加成功'
                        code=Code.SUCCESS_CODE
                        after_data["quesKindNames"]=quesKindName
                        after_data["quesKindIds"]=new_quesKindIds
                        after_data["quesIds"]=new_quesIds
                        data=after_data
                    else:
                        msg=n_ser.errors
                        code=Code.ERROR_CODE
                        data=after_data
                context = {'code': code, 'msg': msg, 'data': data}
            else:
                after_data["paperId"] = new_obj.paperId
                msg='该试卷已存在'
                code=Code.ERROR_CODE
                data=after_data
                context = {'code': code, 'msg': msg, 'data': data}
        else:
            #序列化验证失败，数据不正确
            msg= ser.errors
            code=Code.ERROR_CODE
            data={}
            context = {'code': code, 'msg': msg, 'data': data}
        return Response(context)


#根据试卷id修改试卷状态
class UpdatePaperStatus(APIView):
    def get(self, request):
        paperId = request.query_params.dict().get("paperId")
        paperStasus = request.query_params.dict().get("paperStasus")
        pap_obj=models.Paper.objects.filter(paperId=paperId).first()
        if not pap_obj:
            code = Code.ERROR_CODE
            msg = '该paperId对应的试卷不存在，请检查paperId'
            data = {}
        else:
            models.Paper.objects.filter(paperId=paperId).update(paperStasus=paperStasus)
            ser=PaperSerializer(instance=models.Paper.objects.filter(paperId=paperId).first())
            code = Code.SUCCESS_CODE
            msg='修改试卷状态成功'
            data=ser.data
        context = {'code': code, 'msg': msg, 'data': data}
        return Response(context)




        
#添加答题
class AddAnswerView(APIView):
    def post(self,request):
        ser=AnswerSerializer(data=request.data)
        if ser.is_valid():
            #序列化验证通过，数据类型正确
            after_data = ser.validated_data  #将通过验证的json数据转化为字典
            new_certId=after_data.get("certId")
            new_quesId=after_data.get("quesId")
            new_obj=models.Answer.objects.filter(certId=new_certId,quesId=new_quesId).first()
            if not new_obj :
                new_answerId= str(uuid.uuid1())
                new_paperId = after_data.get("paperId")
                new_examId=after_data.get("examId")
                data={}
                if not models.Exam.objects.filter(examId=new_examId).first():
                    msg="该考试不存在,请检查考试id"
                    code=Code.ERROR_CODE
                elif not models.Paper.objects.filter(paperId=new_paperId).first():
                    msg="该试卷不存在,请检查试卷id"
                    code=Code.ERROR_CODE
                elif not models.Certify.objects.filter(certId=new_certId).first():
                    msg="该答题考生不存在,请检查准考证号"
                    code=Code.ERROR_CODE
                elif not models.Ques.objects.filter(quesId=new_quesId).first():
                    msg="该题目不存在,请检查试题id"
                    code=Code.ERROR_CODE
                else:
                    after_data['answerId']=new_answerId
                    after_ser=AnswerSerializer(data=after_data)
                    if after_ser.is_valid():
                        models.Exam.objects.filter(examId=new_examId).update(hasAnswers=1)
                        after_ser.save()
                        paperName=models.Paper.objects.filter(paperId=new_paperId).first().paperName
                        after_ser.validated_data["paperName"]=paperName
                        msg = '答题添加成功'
                        code = Code.SUCCESS_CODE
                        data=after_ser.validated_data
                    else:
                        msg=after_ser.errors
                        code=Code.ERROR_CODE
                        data=after_ser.data
                context = {'code': code, 'msg': msg, 'data': data}

            else:
                o_answerId=new_obj.answerId
                msg='该学号对应问题的答题记录已经存在'
                code=Code.ERROR_CODE
                after_data["answerId"]=o_answerId
                paperName = models.Paper.objects.filter(paperId=after_data.get("paperId")).first().paperName
                after_data["paperName"] = paperName
                data=after_data
                context={'code':code,'msg':msg,'data':data}
        else:
            #序列化验证失败，数据不正确
            msg= ser.errors
            code=Code.ERROR_CODE
            data={}
            context={'code':code,'msg':msg,'data':data}
        return Response(context)  


#更改考试试卷的答卷上传状态
class ExamChangeHasAnswerView(APIView):
    def get(self,request):
        examId = request.query_params.dict().get("examId")
        examStatus = request.query_params.dict().get("status")
        ex_obj = models.Exam.objects.filter(examId=examId).first()
        if not ex_obj:
            code=Code.ERROR_CODE
            msg='该examId对应的考试不存在，请检查examId'
            data={}
        else:
            ex_obj.hasAnswers=examStatus
            ex_obj.save()
            code=Code.SUCCESS_CODE
            msg='修改考试试卷的答卷状态成功'
            ser=ExamSerializer(instance=ex_obj)
            data=ser.data
        context = {'code': code, 'msg': msg, 'data': data}
        return Response(context)






#添加考试(躯壳)
class AddExambeforeView(APIView):
    def get(self,request):
        examId = str(uuid.uuid1())
        exam = models.Exam()
        exam.examId = examId
        exam.examName =''
        exam.paperIds=''
        exam.examTimes=''
        exam.save()
        code=Code.SUCCESS_CODE
        msg='添加考试外壳成功'
        ser=ExamSerializer(instance=exam)
        context={'code':code,'msg':msg,'data':ser.data}
        return Response(context)

#添加考试（内容）
class AddExamView(APIView):
    def post(self,request):
        ser=ExamSerializer(data=request.data)
        if ser.is_valid():
            #序列化验证通过，数据类型正确
            after_data = ser.validated_data  #将通过验证的json数据转化为字典
            new_examName = after_data.get("examName")
            new_obj=models.Exam.objects.filter(examName=new_examName).first()
            new_paperIds = after_data["paperIds"].replace('[', '').replace(']', '').split(',')
            if not new_obj :
                #获取使用的试卷
                paperNames=[]  #使用试卷Name-->list
                for paperId_paper in new_paperIds:
                    paperNames.append(models.Paper.objects.filter(paperId=paperId_paper).first().paperName)
                examId=after_data.get("examId")
                ex_obj=models.Exam.objects.filter(examId=examId).first()
                if not ex_obj:
                    code=Code.ERROR_CODE
                    msg='该examId对应的考试不存在，请检查examId'
                    data={}
                else:
                    ex_obj.examName=new_examName
                    ex_obj.paperIds=after_data.get("paperIds")
                    ex_obj.examTimes=after_data.get("examTimes")
                    ex_obj.hasAnswers=0
                    ex_obj.save()

                    code = Code.SUCCESS_CODE
                    msg = '新增考试成功'
                    after_data["paperNames"] = paperNames
                    after_data["paperIds"]=new_paperIds
                    after_data["hasAnswers"]=ex_obj.hasAnswers
                    data=after_data
                context = {'code': code, 'msg': msg, 'data': data}
            else:
                msg='该考试已存在,请更改考试名称'
                code=Code.ERROR_CODE
                context={'code':code,'msg':msg,'data':after_data}
        else:
            #序列化验证失败，数据不正确
            msg= ser.errors
            code=Code.ERROR_CODE
            context={'code':code,'msg':msg,'data':{}}
        return Response(context)


#添加考试（取消）
class AddExamCancelView(APIView):
    def delete(self,request):
        exId=request.query_params.dict().get("examId")
        ex_obj=models.Exam.objects.filter(examId=exId).first()
        ser = ExamSerializer(instance=ex_obj)
        ex_obj.delete()
        code=Code.SUCCESS_CODE
        msg='取消添加考试成功'
        context = {'code': code, 'msg': msg, 'data': ser.data}
        return Response(context)


