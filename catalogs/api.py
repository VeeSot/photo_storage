from rest_framework.decorators import detail_route
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, \
    CreateModelMixin
from rest_framework.serializers import HyperlinkedModelSerializer
from rest_framework.viewsets import ModelViewSet

from catalogs.models import Catalog
from photo.api import PhotoSerializer
from utils.functions import JSONResponse


class CatalogSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Catalog
        fields = ('name', 'id')


class CatalogList(ListModelMixin, CreateModelMixin, GenericAPIView):
    queryset = Catalog.objects.all()
    serializer_class = CatalogSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def create(self, validated_data, **kwargs):
        catalog = Catalog.objects.create(**validated_data.data)
        return catalog

    def post(self, request, *args, **kwargs):
        catalog = self.create(request)
        serializer = CatalogSerializer(catalog)
        return JSONResponse(serializer.data, status=201)


class CatalogDetail(ModelViewSet):
    lookup_value_regex = '[0-9]'
    queryset = Catalog.objects.all()
    serializer_class = CatalogSerializer

    @detail_route(methods=['get'])
    def photos(self, request, *args, **kwargs):
        catalog = Catalog.objects.get(**kwargs)
        photos = catalog.photo_set.all()
        serializers = map(PhotoSerializer, photos)
        return JSONResponse([serializer.data for serializer in serializers])
        # PUT

    def retrieve(self, request, *args, **kwargs):
        idx = int(kwargs.get('pk'))
        catalog = Catalog.objects.get(id=idx)
        serializer = CatalogSerializer(catalog, context={'request': request})
        return JSONResponse(serializer.data)

        # PUT

    def update(self, request, *args, **kwargs):
        catalog = Catalog.objects.get(id=kwargs.get('pk'))
        public_props = ['name']

        for name in public_props:
            setattr(catalog, name, request.data.pop(name))

        catalog.save()

        serializer = CatalogSerializer(catalog)
        return JSONResponse(serializer.data)

    def put(self, request, *args, **kwargs):
        catalog = self.update(request, *args, **kwargs)


    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
