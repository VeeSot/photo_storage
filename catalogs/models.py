# coding=utf-8
from django.db import models


class Catalog(models.Model):
    name = models.CharField(max_length=255, blank=False, verbose_name="Название", db_tablespace="indexes")

    class Meta:
        db_table = 'catalogs'
        verbose_name = 'Каталог'
        verbose_name_plural = "Каталоги"

