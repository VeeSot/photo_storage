import json
import os
import tempfile
from time import sleep

import pytest
from PIL import Image
from rest_framework import status
from rest_framework.test import APITestCase

from catalogs.models import Catalog
from main.variables import api_path
from photo.models import Photo
from tasks.models import Task
from utils.common_services import CommonTestMethods


@pytest.mark.django_db
class PhotoTestCase(APITestCase):
    postfix = '/photo/'
    base_url = '{prefix}{postfix}'.format(prefix=api_path, postfix=postfix)

    def setUp(self):
        self.user = CommonTestMethods.create_superuser()
        self.client = CommonTestMethods.get_client_with_csrf_token()
        self.catalog = Catalog.objects.create(name="Test catalog")

    def test_create_photo(self):
        # Make stub
        image = Image.new('RGB', (100, 100))
        tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
        image.save(tmp_file)

        data = {
            'file': tmp_file,
        }

        # Additional fields

        data.update({"name": "Test photo",
                     "catalog_id": self.catalog.id})

        response = self.client.post(PhotoTestCase.base_url, data, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Photo.objects.count(), 1)  # Only one photo
        self.assertEqual(Photo.objects.get(pk=1).name, data['name'])
        self.assertEqual(Photo.objects.get(pk=1).catalog_id, self.catalog.id)

    def test_get_photo(self):
        photo = Photo.objects.create(name="Photo", file="...", catalog=self.catalog)

        url = PhotoTestCase.base_url + '{idx}/'.format(idx=self.catalog.id)
        response = self.client.get(url)
        json_response = json.loads(response.content.decode())

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json_response.pop('name'), photo.name, "Photo name not correct")

    def test_delete_photo(self):
        photo = Photo.objects.create(name="Photo", file="...", catalog=self.catalog)

        url = PhotoTestCase.base_url + '{idx}/'.format(idx=photo.id)
        req = self.client.delete(url, content_type='application/json')

        self.assertEqual(req.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Photo.objects.count(), 0, "Photo not delete")

    def test_serve_photo(self):
        photo = Photo.objects.create(name="Photo", file="...", catalog=self.catalog)

        url = PhotoTestCase.base_url + '{idx}/serve/'.format(idx=photo.id)
        req = self.client.patch(url, content_type='application/json')

        self.assertEqual(req.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(Task.objects.count(), 1, "Task not created")
        task = Task.objects.get(photo=photo)

        self.assertEqual(task.complete, False, "Task shouldn't finished")

