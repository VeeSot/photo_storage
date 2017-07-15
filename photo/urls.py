from django.conf.urls import url
from rest_framework import routers

from photo.api import PhotoList, PhotoDetail

router = routers.SimpleRouter()
router.register(r'', PhotoDetail)

urlpatterns = [
    url(r'^$', PhotoList.as_view()),

]
urlpatterns += router.urls
