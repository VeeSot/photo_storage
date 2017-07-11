from django.conf.urls import url


from catalogs.api import CatalogList, CatalogDetail


urlpatterns = [
    url(r'^$', CatalogList.as_view()),
    url(r'^(?P<pk>[0-9]+)/$', CatalogDetail.as_view()),

]
