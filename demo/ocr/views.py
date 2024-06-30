import asyncio

import cv2
import numpy as np
from PIL.ImageDraw import ImageDraw
from PIL.ImageFont import ImageFont
from django.http import HttpResponse
from django.shortcuts import render
from erniebot_agent.memory import HumanMessage
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from paddleocr import PPStructure, PaddleOCR, draw_ocr, draw_structure_result, save_structure_res
from PIL import Image

from ocr.models import OCRModel, OCRSerializer
from server.settings import PATH_TYPE, OCRMachine, FONT_PATH, SAVE_DIR
from util.img import transPath
from aibot.views import talk
from util.prompts import ANSWER, mkAnswerPrompt


class OCRViewSet(viewsets.ModelViewSet):
    queryset = OCRModel.objects.all()
    serializer_class = OCRSerializer

    @action(methods=['put'], detail=False, url_path='simple')
    def simpleOCR(self, request):
        """执行基本的识别功能，只补充 res"""
        # 获取数据
        data = request.data.copy()
        headers = self.get_success_headers(data)

        if data['img'] is None:
            return Response('NO IMAGE', status=status.HTTP_400_BAD_REQUEST)

        # 获取图片URL
        path = str(data['img'])

        # ocr
        res_str = read(path, PATH_TYPE['URL'])
        data['res'] = res_str

        # TODO: 生成展示图
        # shw = mkShwImg(result, local_path)
        data['shw'] = 'NULL'

        # 插入数据库
        ser = self.get_serializer(data=data)
        ser.is_valid(raise_exception=False)
        self.create(ser)

        # 返回信息
        print(">>> ocr data:", data)
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)

    @action(methods=['put'], detail=False, url_path='ques')
    def scanQues(self, request):
        """ 扫描题目,提供题目扫描结果和 AI 推荐答案 """
        info = request.data.copy()
        img = info.get('img')
        if img is None:
            return Response('BAD IMAGE', status=status.HTTP_400_BAD_REQUEST)
        res_str = read(img, PATH_TYPE['URL'])

        msgs = [HumanMessage(mkAnswerPrompt(res_str))]
        resp = asyncio.run(talk(msgs, ANSWER.content, []))
        data = {
            'scan': res_str,
            'ans': str(resp.content)
        }
        return Response(data, status=status.HTTP_200_OK)


def read(path, path_type):
    """核心识别功能"""
    # 查表
    if path_type == PATH_TYPE['URL']:
        sql = f"select * from ocr_ocrmodel where img = '{path}'"
        records = list(OCRModel.objects.raw(sql))
        if len(records) != 0:  # record exist
            res = str(records[0].__dict__['res'])
            return res

    # 转换成本地路径
    if path_type == PATH_TYPE['URL']:
        path = transPath(path, path_type)
    # 识别内容
    # pp ocr
    res_str = ''
    result = OCRMachine.ocr(path, cls=True)
    if result is None:
        return ""

    for idx in range(len(result)):
        res = result[idx]
        if res is None:
            continue
        for line in res:
            if line is not None:
                res_str += ' ' + line[1][0]
    return res_str


# TODO: 自定义文字位置
def mkShwImg(result, path) -> str:
    """制作展示图片"""
    result = result[0]

    # 位置
    boxes = [line[0] for line in result]
    # 识别文本
    txts = [line[1][0] for line in result]
    # 置信度
    scores = [line[1][1] for line in result]
    print(f">>> mkShwImg:\n>>> BOXES::{boxes}\n>>> TXTS::{txts}\n>>> SCS::{scores}")

    # 绘制文字信息
    image = Image.open(path).convert('RGB')
    im_show = draw_ocr(image, boxes, txts, scores, font_path=FONT_PATH)
    im_show = Image.fromarray(im_show)

    # 导出图片
    save_path = SAVE_DIR + 'res_' + path.split('/')[-1]
    im_show.save(save_path)

    return transPath(save_path, PATH_TYPE['LOCAL'])
