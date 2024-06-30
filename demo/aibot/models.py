import json
import uuid

from django.db import models
from rest_framework import serializers

from util.encoder import Encoder


class AIBot(models.Model):
    """AI 对话模型"""
    sysId = models.CharField(max_length=256, blank=True, help_text="用户系统ID")
    num = models.IntegerField(default=0, blank=False, help_text="对话历史中的第几条")
    typ = models.IntegerField(default=0, blank=False, help_text="信息类型 0 - AI Message / 1 - Human Message")
    content = models.TextField(blank=False, help_text="对话内容")
    time = models.DateTimeField(auto_now_add=True, help_text="产生时间")

    def __str__(self) -> str:
        return json.dumps(self, cls=Encoder, ensure_ascii=False)

    def __repr__(self):
        return self.__str__()


class AIBotSerializer(serializers.ModelSerializer):
    class Meta:
        model = AIBot
        fields = "__all__"
