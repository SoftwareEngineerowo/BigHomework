# views.py
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import FileUploadParser
from server.settings import SAVE_DIR, PATH_TYPE
from util.img import transPath
from util.name import mkOriginImgName


class FileUploadView(APIView):
    """文件上传"""
    parser_classes = [FileUploadParser, ]

    def put(self, request, filename, format=None):
        file_obj = request.data['file']
        filename = mkOriginImgName(file_obj.name)
        local_path = SAVE_DIR + filename
        with open(local_path, 'wb') as f:
            for chunk in file_obj.chunks():
                f.write(chunk)

        url = transPath(local_path, PATH_TYPE['LOCAL'])
        return HttpResponse(url, status=200)


class FileDownloadView(APIView):
    """文件下载"""
    parser_classes = [FileUploadParser, ]

    def get(self, request, filename, format=None):
        image_path = SAVE_DIR + filename
        image_data = open(image_path, "rb").read()
        file_type = str(filename).split('.')[-1]
        if file_type in ['jpg', 'jpeg', 'png', 'gif']:
            return HttpResponse(image_data, content_type="image/"+file_type)
        else:
            return HttpResponse(image_data, content_type="application/octet-stream")
