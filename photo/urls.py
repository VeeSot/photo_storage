from django.conf.urls import url

from photo.api import PhotoList, PhotoDetail

urlpatterns = [
    url(r'^$', PhotoList.as_view()),
    url(r'^(?P<pk>[0-9]+)/$', PhotoDetail.as_view()),

]
