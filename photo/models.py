# coding=utf-8
from django.db import models

from catalogs.models import Catalog


class Photo(models.Model):
    file = models.FileField(blank=False,verbose_name="Ссылка на фото")
    name = models.CharField(max_length=255, blank=False, verbose_name="Название")
    catalog = models.ForeignKey(Catalog)

    class Meta:
        db_table = 'photos'
        verbose_name = 'Фото'
        verbose_name_plural = "Фотогарафии"

