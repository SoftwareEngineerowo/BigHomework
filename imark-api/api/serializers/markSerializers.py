from api import models
from rest_framework import serializers



#任务信息表序列化器
class MarkSerializer(serializers.ModelSerializer):
    markId = serializers.CharField(required=False)
    class Meta:
        model=models.Mark
        fields="__all__"



#按题打分结果模型表序列化器
class MarkResultSerializer(serializers.ModelSerializer):
    id = serializers.CharField(required=False)
    class Meta:
        model=models.Mark_result
        fields="__all__"


#单卷分数表序列化器
class PaperScoreSheetSerializer(serializers.ModelSerializer):
    id=serializers.CharField(required=False)
    class Meta:
        model=models.Paper_Score_Sheet
        fields="__all__"