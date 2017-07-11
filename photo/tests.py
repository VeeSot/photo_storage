import json
import tempfile

import pytest
from PIL import Image
from rest_framework import status
from rest_framework.test import APITestCase

from catalogs.models import Catalog
from main.variables import api_path
from photo.models import Photo
from utils.common_services import CommonTestMethods


@pytest.mark.django_db
class PhotoTestCase(APITestCase):
    postfix = '/photo/'
    base_url = '{prefix}{postfix}'.format(prefix=api_path, postfix=postfix)

    def setUp(self):
        self.user = CommonTestMethods.create_superuser()
        self.client = CommonTestMethods.get_client_with_csrf_token()

    def test_create_photo(self):
        # Make stub
        image = Image.new('RGB', (100, 100))
        tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
        image.save(tmp_file)

        data = {
            'file': tmp_file,
        }

        # Additional fields
        catalog = Catalog.objects.create(name="Test catalog")
        catalog.save()
        data.update({"name": "Test photo",
                     "catalog_id": catalog.id})

        response = self.client.post(PhotoTestCase.base_url, data, format='multipart')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Photo.objects.count(), 1)  # Only one photo
        self.assertEqual(Photo.objects.get(pk=1).name, data['name'])
        self.assertEqual(Photo.objects.get(pk=1).catalog_id, catalog.id)

    def test_get_catalog(self):
        catalog = Catalog.objects.create(name="Catalog")
        catalog.save()

        photo = Photo.objects.create(name="Photo", file="...", catalog=catalog)
        photo.save()

        url = PhotoTestCase.base_url + '{idx}/'.format(idx=catalog.id)
        response = self.client.get(url)
        json_response = json.loads(response.content.decode())

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json_response.pop('name'), photo.name, "Photo name not correct")

    def test_delete_photo(self):
        catalog = Catalog.objects.create(name="Catalog")
        catalog.save()

        photo = Photo.objects.create(name="Photo", file="...", catalog=catalog)
        photo.save()

        url = PhotoTestCase.base_url + '{idx}/'.format(idx=photo.id)
        req = self.client.delete(url, content_type='application/json')

        self.assertEqual(req.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Photo.objects.count(), 0, "Photo not delete")
