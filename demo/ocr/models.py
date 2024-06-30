from django.db import models
from rest_framework import serializers
from server.settings import OCR_TYPE


class OCRModel(models.Model):
    """文本识别模型"""
    img = models.CharField(max_length=512, verbose_name='img', help_text="识别图片的HTTP地址",blank=False)
    res = models.TextField(verbose_name='res', help_text="识别结果纯文本",blank=True)
    typ = models.CharField(max_length=512, verbose_name='type', help_text="文本类型（标题/信息/题目/手写）",
                           choices=tuple(OCR_TYPE),blank=True,default=OCR_TYPE[0][0])
    shw = models.CharField(max_length=512, verbose_name='shw', help_text="加工后展示的图片HTTP地址",blank=True)


class OCRSerializer(serializers.ModelSerializer):
    class Meta:
        model = OCRModel
        fields = '__all__'
