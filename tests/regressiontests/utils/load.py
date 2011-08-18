# -*- coding: utf-8 -*-
from __future__ import with_statement
from django.contrib.auth.models import User, AnonymousUser
from django.test.testcases import TestCase
from django.utils.load import load_object, iterload_objects
    

class LoadTests(TestCase):
        
    def test_load_object(self):
        obj = load_object('django.contrib.auth.models.User')
        self.assertEqual(obj, User)
        
    def test_load_object_fail_type(self):
        self.assertRaises(TypeError, load_object, 'notanimportpath')
        
    def test_load_object_fail_import(self):
        self.assertRaises(ImportError, load_object, 'django.contrib.auth.not_models.User')
        
    def test_load_object_fail_attribute(self):
        self.assertRaises(AttributeError, load_object, 'django.contrib.auth.models.NotAUser')
        
    def test_load_object_exception_handler(self):
        class MyException(Exception): pass
        def exc_handler(*args, **kwargs):
            raise MyException
        self.assertRaises(MyException, load_object, 'django.contrib.auth.models.NotAUser', exc_handler)
        self.assertRaises(MyException, load_object, 'django.contrib.auth.not_models.User', exc_handler)
        self.assertRaises(TypeError, load_object, 'notanimportpath')

    def test_iterload_objects(self):
        import_paths = ['django.contrib.auth.models.User',
                        'django.contrib.auth.models.AnonymousUser']
        objs = list(iterload_objects(import_paths))
        self.assertEqual(len(objs), 2)
        self.assertEqual(objs[0], User)
        self.assertEqual(objs[1], AnonymousUser)
        
    def test_iterload_objects_propagates_exception_handler(self):
        class MyException(Exception): pass
        def exc_handler(*args, **kwargs):
            raise MyException
        gen = iterload_objects(['django.contrib.auth.models.User', 'django.contrib.auth.models.NotAUser'], exc_handler)
        user = gen.next()
        self.assertEqual(user, User)
        self.assertRaises(MyException, gen.next)
    
    def test_iterload_objects_ignore_exceptions(self):
        def exc_handler(*args, **kwargs):
            pass

        import_paths = ['django.contrib.auth.models.User',
                        'django.contrib.auth.models.NotAUser',
                        'django.contrib.auth.models.AnonymousUser']
        objs = list(iterload_objects(import_paths, exc_handler))
        self.assertEqual(len(objs), 2)
        self.assertEqual(objs[0], User)
        self.assertEqual(objs[1], AnonymousUser)
