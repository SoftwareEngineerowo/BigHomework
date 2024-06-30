from django.urls import path

from . import seg_view_set

urlpatterns = [
    path("", seg_view_set.index, name="index"),
]