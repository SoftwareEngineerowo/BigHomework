import cv2
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from seg.models import SegIMG, IMGSerializer
from server.settings import SAVE_DIR, PATH_TYPE, SERVER_PATH, IMG_DOWNLOAD_PATH, TWIST_SERVER_PATH, TWIST_SERVER_PORT
from util.db import updateSQL
from util.img import transPath
import pandas as pd


class SegViewSet(ModelViewSet):
    queryset = SegIMG.objects.all()
    serializer_class = IMGSerializer

    @action(methods=['get'], detail=False)
    def test(self, request, *args, **kwargs):
        return Response('test')

    @action(methods=['post'], detail=False, url_path='save')
    def startSeg(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        print(">>> seg_view_set::startSeg")
        print(">>> seg_img: ", serializer.data)
        img = serializer.data
        save_path = segImg(seg_img=img)

        img['path'] = str(save_path)
        headers = self.get_success_headers(serializer.data)

        if save_path == 'BAD DATA':
            return Response(save_path, status=status.HTTP_400_BAD_REQUEST, headers=headers)

        save_path = transPath(save_path, PATH_TYPE['LOCAL'])
        img['url'] = save_path
        img['quesId'] = 'unknown'
        img['paper'] = 'unknown'
        ser = self.get_serializer(data=img)
        ser.is_valid(raise_exception=False)
        self.create(ser)
        return HttpResponse(save_path, status=status.HTTP_201_CREATED, headers=headers)

    @action(methods=['put'], detail=False, url_path='structure')
    def createStructure(self, request, *args, **kwargs):
        """
        接收试卷结构
        """
        blocks = request.data['structure']
        for block in blocks:
            ser = self.get_serializer(data=block)
            ser.is_valid(raise_exception=False)
            self.create(ser)
        return Response(blocks, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=False, url_path='do')
    def segAll(self, request, *args, **kwargs):
        data = request.data
        # 试卷ID
        paperId = str(data['paperId'])
        imgs = data['imgs']
        cert = data['cert']

        # 解析文件`
        cert_file = transPath(cert, PATH_TYPE['URL'])
        df = pd.read_excel(cert_file)
        df.columns = ["certId", "stuId", "stuName"]
        cert_dict = df.to_dict('records')
        certs = cert_dict

        # 查询
        sql = f"select * from seg_segimg where paper = '{paperId}' and img = 'STRUCTURE';"
        blocks = SegIMG.objects.raw(sql)
        print(blocks)

        # 切割
        pt = 0
        resp = []
        for img in imgs:
            for block in blocks:
                data = block.__dict__
                task = {
                    'img': str(img),
                    'num': int(data['num']),
                    'x1': int(data['x1']),
                    'x2': int(data['x2']),
                    'y1': int(data['y1']),
                    'y2': int(data['y2']),
                    'quesId': str(data['quesId']),
                    'paper': str(paperId),
                    'typ': str(data['typ']),
                    'certId': str(cert_dict[pt]['certId']),
                    'stuId': str(cert_dict[pt]['stuId']),
                    'stuName': str(cert_dict[pt]['stuName'])
                }
                local_path = segImg(task)
                url = transPath(local_path, PATH_TYPE['LOCAL'])
                task['url'] = url
                resp.append(task)
                ser = self.get_serializer(data=task)
                ser.is_valid(raise_exception=False)
                self.create(ser)
            pt += 1

        # 转发
        import http.client
        import json

        load = {
            "cert": certs,
            "ans": resp
        }
        data = json.dumps(load, ensure_ascii=False)

        return HttpResponse(data, status=status.HTTP_200_OK)

    @action(methods=['patch'], detail=False, url_path='update')
    def updateID(self, request):
        data = request.data
        old = str(data['old'])
        update = data['update']
        paper = str(update['paper'])
        ques = update['ques']
        resp = []
        for q in ques:
            update_sql = f"update seg_segimg set paper = '{paper}' , quesId = '{q}' where (  paper = '{old}' or quesId = '{old}' ) and  num in (select min(num) from seg_segimg where img = 'STRUCTURE' and paper = '{old}' or quesId = '{old}');"
            select_sql = f"select * from seg_segimg where quesId = '{q}';"
            resp.append(updateSQL(update_sql, select_sql))
        print(resp)
        return Response("Done", status=status.HTTP_200_OK)


def checkPos(x1, x2, y1, y2) -> bool:
    if x1 > x2 or y1 > y2:
        return False
    if x1 < 0 or y1 < 0 or x2 < 0 or y2 < 0:
        return False
    return True


def mkSavePath(seg_img) -> str:
    """拼接保存位置"""
    img_name = str(seg_img['img']).split('/')[-1]
    img_num = str(seg_img['num'])
    x1 = str(int(seg_img['x1']))
    y1 = str(int(seg_img['y1']))
    path = SAVE_DIR + img_name.split('.')[0] + '_' + img_num + '_' + x1 + '_' + y1 + '.' + img_name.split('.')[1]
    return path


def segImg(seg_img) -> str:
    img_path = transPath(seg_img['img'], PATH_TYPE['URL'])
    x1 = (int(seg_img['x1']))
    y1 = (int(seg_img['y1']))
    x2 = (int(seg_img['x2']))
    y2 = (int(seg_img['y2']))

    print(">>> seg_img: ", img_path)

    if not checkPos(x1, x2, y1, y2):
        return 'BAD DATA'

    # read img
    do_img = cv2.imread(img_path)
    # cut
    cropped = do_img[y1:y2, x1:x2]
    # make save path
    save_path = mkSavePath(seg_img)

    # save img
    cv2.imwrite(save_path, cropped)
    return save_path
