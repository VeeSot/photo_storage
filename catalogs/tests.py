import json

import pytest
from rest_framework import status
from rest_framework.test import APITestCase

from catalogs.models import Catalog
from main.variables import api_path
from photo.models import Photo
from utils.common_services import CommonTestMethods


@pytest.mark.django_db
class CatalogTestCase(APITestCase):
    postfix = '/catalogs/'
    base_url = '{prefix}{postfix}'.format(prefix=api_path, postfix=postfix)

    def setUp(self):
        self.user = CommonTestMethods.create_superuser()
        self.client = CommonTestMethods.get_client_with_csrf_token()

    def test_create_catalog(self):
        data = {"name": "Catalog"}
        response = self.client.post(CatalogTestCase.base_url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Catalog.objects.count(), 1)  # Only one catalog

    def test_get_catalog(self):
        catalog_name = 'Catalog'
        catalog = Catalog.objects.create(name=catalog_name)
        catalog.save()
        idx = catalog.id

        url = CatalogTestCase.base_url + '{idx}/'.format(idx=idx)
        response = self.client.get(url)
        json_response = json.loads(response.content.decode())  # JSON-rerp response

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json_response.pop('name'), catalog_name, "Catalog name not correct")

    def test_catalog_list(self):
        Catalog.objects.create(name="Catalog1").save()
        Catalog.objects.create(name="Catalog2").save()
        response = self.client.get(CatalogTestCase.base_url)
        json_response = json.loads(response.content.decode())

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(json_response), 2)  # We get 2 catalogs

    def test_update_catalog(self):
        catalog_name = 'Catalog'
        new_catalog_name = 'New_Catalog'
        catalog = Catalog.objects.create(name=catalog_name)
        catalog.save()
        idx = catalog.id
        url = CatalogTestCase.base_url + '{idx}/'.format(idx=idx)

        req = self.client.put(url, json.dumps({'name': new_catalog_name}), content_type='application/json')
        json_response = json.loads(req.content.decode())

        self.assertEqual(req.status_code, status.HTTP_200_OK)
        self.assertEqual(Catalog.objects.count(), 1)  # Not new catalogs
        self.assertEqual(idx, json_response.pop('id'))
        self.assertEqual(json_response.get('name'), new_catalog_name)

    def test_delete_catalog(self):
        catalog = Catalog.objects.create(name="Catalog")
        catalog.save()
        idx = catalog.id

        url = CatalogTestCase.base_url + '{idx}/'.format(idx=idx)
        req = self.client.delete(url, content_type='application/json')

        self.assertEqual(req.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Catalog.objects.count(), 0, "Catalog not delete")

    def test_photo_in_catalog(self):
        catalog = Catalog.objects.create(name="Catalog")
        catalog.save()

        for idx in xrange(3):  # 3 photo
            Photo.objects.create(name="Photo {}".format(idx), file="...", catalog=catalog)

        url = CatalogTestCase.base_url + '{idx}/photos/'.format(idx=catalog.id)
        req = self.client.get(url)

        self.assertEqual(req.status_code, status.HTTP_200_OK)
        json_response = json.loads(req.content.decode())
        self.assertEqual(Photo.objects.count(), len(json_response), "Photos not found")
