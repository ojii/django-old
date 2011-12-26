# -*- coding: utf-8 -*-
from django.db import models
from django.test.testcases import TestCase


class AddLazyRelationsTests(TestCase):
    def test_model_with_split_method(self):
        class Meta:
            order_with_respect_to = 'related'

        attrs = {
            'related': models.ForeignKey('foreign_key.RelatedModel'),
            '__module__': self.__module__,
            'Meta': Meta,
        }
        MainModel = type('MainModel', (models.Model, ), attrs)

