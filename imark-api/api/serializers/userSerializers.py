from api import models
from rest_framework import serializers

#用户表序列化器
class UserSerializer(serializers.ModelSerializer):
    sysId=serializers.CharField(required=False)
    avatar=serializers.CharField(required=False)
    class Meta:
        model=models.Role
        fields="__all__"