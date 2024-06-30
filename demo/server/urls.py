from django.urls import path, include

from rest_framework import routers

from aibot.views import AIBotViewSet
from ocr.views import OCRViewSet
from seg.seg_view_set import SegViewSet
from django.urls import re_path
from upload.views import FileUploadView, FileDownloadView

router = routers.DefaultRouter()
router.register(r'/seg', SegViewSet, basename='seg')
router.register(r'/ocr', OCRViewSet, basename='ocr')
router.register(r'/ai', AIBotViewSet, basename='ai')
urlpatterns = [
    path('api', include(router.urls)),
    re_path(r'^files/upload/(?P<filename>[^/]+)$', FileUploadView.as_view()),
    re_path(r'^files/download/(?P<filename>[^/]+)$', FileDownloadView.as_view()),
]
