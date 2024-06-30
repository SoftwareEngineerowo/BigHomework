from django.db import models
from rest_framework import serializers

from server.settings import OCR_TYPE


class SegIMG(models.Model):
    img = models.CharField(max_length=512, verbose_name='img', help_text='待分割的图片')
    paper = models.CharField(max_length=128,default='unknown', verbose_name='paper', help_text='所属试卷ID', blank=True)
    num = models.IntegerField(default=0, verbose_name='num', help_text='切片序列')
    x1 = models.IntegerField(default=0, verbose_name='x1', help_text='坐标x1')
    x2 = models.IntegerField(default=0, verbose_name='x2', help_text='坐标x2')
    y1 = models.IntegerField(default=0, verbose_name='y1', help_text='坐标y1')
    y2 = models.IntegerField(default=0, verbose_name='y2', help_text='坐标y2')
    url = models.CharField(max_length=128, verbose_name='name', help_text='切片地址', blank=True)
    quesId = models.CharField(max_length=128,default='unknown', verbose_name='quesId', help_text='对应题目编号', blank=True)
    typ = models.CharField(max_length=512, verbose_name='type', help_text="文本类型（标题/信息/题目/手写）",
                           choices=tuple(OCR_TYPE), blank=True, default=OCR_TYPE[0][0])
    certId = models.CharField(max_length=32, verbose_name='certId', help_text='所属学生准考证号', blank=True)
    stuName = models.CharField(max_length=16, verbose_name='stuName', help_text='学生姓名', blank=True)
    seg_time = models.DateTimeField(auto_now_add=True, verbose_name='time', help_text='分割时间')



class IMGSerializer(serializers.ModelSerializer):
    class Meta:
        model = SegIMG
        fields = '__all__'
