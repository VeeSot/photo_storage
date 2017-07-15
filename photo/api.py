# coding=utf-8
from rest_framework.decorators import detail_route
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, \
    CreateModelMixin
from rest_framework.serializers import HyperlinkedModelSerializer
from rest_framework.viewsets import ModelViewSet

from photo.models import Photo
from tasks.models import Task
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


class PhotoDetail(ModelViewSet):
    lookup_value_regex = '[0-9]'
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer

    # GET
    def retrieve(self, request, *args, **kwargs):
        idx = kwargs.get('pk')
        photo = Photo.objects.get(id=idx)
        serializer = PhotoSerializer(photo)
        return JSONResponse(serializer.data)

    def update(self, request, *args, **kwargs):
        photo = Photo.objects.get(id=kwargs.get('pk'))
        public_props = ['name']

        for name in public_props:
            setattr(photo, name, request.data.pop(name))

        photo.save()

        return photo

    def put(self, request, *args, **kwargs):
        """Обновление фото"""
        photo = self.update(request, *args, **kwargs)
        serializer = PhotoSerializer(photo)
        return JSONResponse(serializer.data)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    @detail_route(methods=['PATCH'])
    def serve(self, request, *args, **kwargs):
        """Выполняет абстрактныю задачу над фото"""
        idx = kwargs.get('pk')
        photo = Photo.objects.get(id=idx)
        task = Task.objects.create(photo=photo)
        task.serve()
        return JSONResponse({'status': 'task running'}, status=202)
