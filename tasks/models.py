# coding=utf-8

from multiprocessing import Process
from time import sleep

from django.db import models

from photo.models import Photo


def worker():
    """Abstract function"""
    sleep(10)
    # do something


class Task(models.Model):
    photo = models.ForeignKey(Photo)
    complete = models.BooleanField(default=False, verbose_name="Задача завершена")

    def serve(self):
        p = Process(target=worker)  # Also we can try Thread + daemon when we haven't enough memory
                                    #  or want share data or communicate
        p.start()

    class Meta:
        db_table = 'tasks'
        verbose_name = 'Фоновая задачка'
        verbose_name_plural = "Фоновые задачки"
