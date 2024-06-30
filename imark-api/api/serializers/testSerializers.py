from api import models
from rest_framework import serializers


#试题类型表序列化器
class QuesKindSerializer(serializers.ModelSerializer):
    quesKindId=serializers.IntegerField(required=False)
    class Meta:
        model=models.Ques_Kind
        fields="__all__"
            

            
#试题表序列化器
class QuesSerializer(serializers.ModelSerializer):
    quesId=serializers.CharField(required=False)
    class Meta:
        model=models.Ques
        fields="__all__"

    
#答题表序列化器
class AnswerSerializer(serializers.ModelSerializer):
    answerId=serializers.CharField(required=False)
    class Meta:
        model=models.Answer
        fields="__all__"  
        
        
#准考证-学号表序列化器
class CertifySerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Certify
        fields="__all__"  
        
#试卷表序列化器
class PaperSerializer(serializers.ModelSerializer):
    paperId = serializers.CharField(required=False)
    paperStasus=serializers.IntegerField(required=False)
    class Meta:
        model=models.Paper
        fields="__all__"  
        
#考试表序列化器
class ExamSerializer(serializers.ModelSerializer):
    examId = serializers.CharField(required=False)
    hasAnswers = serializers.CharField(required=False)
    class Meta:
        model=models.Exam
        fields="__all__"  