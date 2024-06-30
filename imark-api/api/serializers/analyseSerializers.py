from api import models
from rest_framework import serializers



##基本分析结果分数表序列化器
class AnalyseSerializer(serializers.ModelSerializer):
    analyseId=serializers.CharField(required=False)
    class Meta:
        model = models.Analyse
        fields = '__all__'




#单卷分数表序列化器
class PaperScoreSheetAnalyseSerializer(serializers.ModelSerializer):
    id=serializers.CharField(required=False)
    certId=serializers.CharField(required=False)
    detailScores=serializers.CharField(required=False)
    finalScore=serializers.FloatField(required=False)
    class Meta:
        model=models.Paper_Score_Sheet
        fields="__all__"