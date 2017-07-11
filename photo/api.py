from rest_framework.generics import GenericAPIView
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, ListModelMixin, \
    CreateModelMixin
from rest_framework.serializers import HyperlinkedModelSerializer

from photo.models import Photo
from utils.functions import JSONResponse


class PhotoSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Photo
        fields = ('name', 'catalog_id', 'id')


class PhotoList(ListModelMixin, CreateModelMixin, GenericAPIView):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def create(self, validated_data, **kwargs):
        important_fields = PhotoSerializer.Meta.fields
        params = {}
        for k in validated_data.data:
            if k in important_fields:
                params[k] = validated_data.data[k]
        photo = Photo.objects.create(**params)
        return photo

    def post(self, request, *args, **kwargs):
        photo = self.create(request)
        serializer = PhotoSerializer(photo)
        return JSONResponse(serializer.data, status=201)


class PhotoDetail(RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, GenericAPIView):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer

    # GET

    def get(self, request, *args, **kwargs):
        photo = self.retrieve(request, *args, **kwargs)
        serializer = PhotoSerializer(photo, context={'request': request})
        return JSONResponse(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        idx = int(kwargs.get('pk'))
        catalog = Photo.objects.get(id=idx)
        return catalog

        # PUT

    def update(self, request, *args, **kwargs):
        photo = Photo.objects.get(id=kwargs.get('pk'))
        public_props = ['name']

        for name in public_props:
            setattr(photo, name, request.data.pop(name))

        photo.save()

        return photo

    def put(self, request, *args, **kwargs):
        catalog = self.update(request, *args, **kwargs)
        serializer = PhotoSerializer(catalog)
        return JSONResponse(serializer.data)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
