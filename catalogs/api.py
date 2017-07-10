from rest_framework.generics import GenericAPIView
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, ListModelMixin, \
    CreateModelMixin
from rest_framework.serializers import HyperlinkedModelSerializer

from catalogs.models import Catalog
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


class CatalogDetail(RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, GenericAPIView):
    queryset = Catalog.objects.all()
    serializer_class = CatalogSerializer

    # GET

    def get(self, request, *args, **kwargs):
        catalog = self.retrieve(request, *args, **kwargs)
        serializer = CatalogSerializer(catalog, context={'request': request})
        return JSONResponse(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        idx = int(kwargs.get('pk'))
        catalog = Catalog.objects.get(id=idx)
        return catalog

        # PUT

    def update(self, request, *args, **kwargs):
        catalog = Catalog.objects.get(id=kwargs.get('pk'))
        public_props = ['name']

        for name in public_props:
            setattr(catalog, name, request.data.pop(name))

        catalog.save()

        return catalog

    def put(self, request, *args, **kwargs):
        catalog = self.update(request, *args, **kwargs)
        serializer = CatalogSerializer(catalog)
        return JSONResponse(serializer.data)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
