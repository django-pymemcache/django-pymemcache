import time
import unittest

import django
from django.core.cache import cache, caches
from django.test import TestCase

from .models import Poll, expensive_calculation

try:
    from unittest import mock
except ImportError:
    import mock


# functions/classes for complex data type tests
def f():
    return 42


class C:
    def m(n):
        return 24


def fail_set_multi(mapping, *args, **kwargs):
    return mapping.keys()


class CacheTestCase(TestCase):
    def tearDown(self):
        cache.clear()

    def test_set_and_get(self):
        cache.set('spam', 'egg')
        self.assertEqual(cache.get('spam'), 'egg')

    def test_non_existent(self):
        self.assertIsNone(cache.get('spam'))
        self.assertEqual(cache.get('spam', 'egg'), 'egg')

    def test_set_many(self):
        # Multiple keys can be set using set_many
        cache.set_many({'key1': 'spam', 'key2': 'eggs'})
        self.assertEqual(cache.get('key1'), 'spam')
        self.assertEqual(cache.get('key2'), 'eggs')

    def test_get_many(self):
        cache.set('a', 'a')
        cache.set('b', 'b')
        cache.set('c', 'c')
        cache.set('d', 'd')
        self.assertEqual(
            cache.get_many(['a', 'c', 'd']),
            {'a': 'a', 'c': 'c', 'd': 'd'},
        )
        self.assertEqual(
            cache.get_many(['a', 'b', 'e']),
            {'a': 'a', 'b': 'b'},
        )

    def test_delete_many(self):
        cache.set('key1', 'spam')
        cache.set('key2', 'eggs')
        cache.set('key3', 'ham')
        cache.delete_many(['key1', 'key2'])
        self.assertIsNone(cache.get('key1'))
        self.assertIsNone(cache.get('key2'))
        self.assertEqual(cache.get('key3'), 'ham')

    def test_clear(self):
        cache.set('key1', 'spam')
        cache.set('key2', 'eggs')
        cache.clear()
        self.assertIsNone(cache.get('key1'))
        self.assertIsNone(cache.get('key2'))

    def test_delete(self):
        cache.set('key1', 'spam')
        cache.set('key2', 'eggs')
        self.assertEqual(cache.get('key1'), 'spam')
        cache.delete('key1')
        self.assertIsNone(cache.get('key1'))
        self.assertEqual(cache.get('key2'), 'eggs')

    def test_in(self):
        cache.set('spam', 'egg')
        self.assertIn('spam', cache)
        self.assertNotIn('egg', cache)

    def test_incr(self):
        cache.set('calc', 41)
        self.assertEqual(cache.incr('calc'), 42)
        self.assertEqual(cache.get('calc'), 42)
        self.assertEqual(cache.incr('calc', 10), 52)
        self.assertEqual(cache.get('calc'), 52)
        self.assertEqual(cache.incr('calc', -10), 42)
        with self.assertRaises(ValueError):
            cache.incr('does_not_exist')

    def test_decr(self):
        cache.set('calc', 43)
        self.assertEqual(cache.decr('calc'), 42)
        self.assertEqual(cache.get('calc'), 42)
        self.assertEqual(cache.decr('calc', 10), 32)
        self.assertEqual(cache.get('calc'), 32)
        self.assertEqual(cache.decr('calc', -10), 42)
        with self.assertRaises(ValueError):
            cache.decr('does_not_exist')

    def test_close(self):
        self.assertTrue(hasattr(cache, 'close'))
        cache.close()

    def test_data_types(self):
        data_types = {
            'string': 'this is a string',
            'int': 42,
            'list': [1, 2, 3, 4],
            'tuple': (1, 2, 3, 4),
            'dict': {'A': 1, 'B': 2},
            'function': f,
            'class': C,
        }
        cache.set('data_types', data_types)
        self.assertEqual(cache.get('data_types'), data_types)

    def test_cache_read_for_model_instance(self):
        expensive_calculation.num_runs = 0
        Poll.objects.all().delete()
        my_poll = Poll.objects.create(question='Well?')
        self.assertEqual(Poll.objects.count(), 1)
        pub_date = my_poll.pub_date
        cache.set('question', my_poll)
        cached_poll = cache.get('question')
        self.assertEqual(cached_poll.pub_date, pub_date)
        # We only want the default expensive calculation run once
        self.assertEqual(expensive_calculation.num_runs, 1)

    def test_expiration(self):
        # Cache values can be set to expire
        cache.set('expire1', 'very quickly', 1)
        cache.set('expire2', 'very quickly', 1)
        cache.set('expire3', 'very quickly', 1)

        time.sleep(2)
        self.assertIsNone(cache.get('expire1'))

        cache.add('expire2', 'newvalue')
        self.assertEqual(cache.get('expire2'), 'newvalue')
        self.assertNotIn('expire3', cache)

    def test_cache_versioning(self):
        # set, using default version = 1
        cache.set('answer1', 42)
        self.assertEqual(cache.get('answer1'), 42)
        self.assertEqual(cache.get('answer1', version=1), 42)
        self.assertIsNone(cache.get('answer1', version=2))

        self.assertIsNone(caches['v2'].get('answer1'))
        self.assertEqual(caches['v2'].get('answer1', version=1), 42)
        self.assertIsNone(caches['v2'].get('answer1', version=2))

        # set, default version = 1, but manually override version = 2
        cache.set('answer2', 42, version=2)
        self.assertIsNone(cache.get('answer2'))
        self.assertIsNone(cache.get('answer2', version=1))
        self.assertEqual(cache.get('answer2', version=2), 42)

        self.assertEqual(caches['v2'].get('answer2'), 42)
        self.assertIsNone(caches['v2'].get('answer2', version=1))
        self.assertEqual(caches['v2'].get('answer2', version=2), 42)

        # v2 set, using default version = 2
        caches['v2'].set('answer3', 42)
        self.assertIsNone(cache.get('answer3'))
        self.assertIsNone(cache.get('answer3', version=1))
        self.assertEqual(cache.get('answer3', version=2), 42)

        self.assertEqual(caches['v2'].get('answer3'), 42)
        self.assertIsNone(caches['v2'].get('answer3', version=1))
        self.assertEqual(caches['v2'].get('answer3', version=2), 42)

        # v2 set, default version = 2, but manually override version = 1
        caches['v2'].set('answer4', 42, version=1)
        self.assertEqual(cache.get('answer4'), 42)
        self.assertEqual(cache.get('answer4', version=1), 42)
        self.assertIsNone(cache.get('answer4', version=2))

        self.assertIsNone(caches['v2'].get('answer4'))
        self.assertEqual(caches['v2'].get('answer4', version=1), 42)
        self.assertIsNone(caches['v2'].get('answer4', version=2))

    def test_invalid_key_characters(self):
        # memcached does not allow whitespace or control characters in keys
        # when using the ascii protocol.
        with self.assertRaises(Exception):
            cache.set('key with spaces', 'value')

    def test_invalid_key_length(self):
        # memcached limits key length to 250
        with self.assertRaises(Exception):
            cache.set('a' * 251, 'value')

    @unittest.skipIf(django.VERSION < (2, 0), 'Returning failing list >=2.0')
    def test_set_many_returns_failing_keys(self):
        # https://docs.djangoproject.com/en/2.1/releases/2.0/#cache
        with mock.patch(
            'djpymemcache.client.Client.set_multi',
            side_effect=fail_set_multi,
        ):
            failing_keys = cache.set_many({'key': 'value'})
            self.assertEqual(failing_keys, ['key'])

    @unittest.skipIf(django.VERSION >= (2, 0), 'Returning NOne <2.0')
    def test_set_many_returns_none(self):
        with mock.patch(
            'djpymemcache.client.Client.set_multi',
            side_effect=fail_set_multi,
        ):
            failing_keys = cache.set_many({'key': 'value'})
            self.assertEqual(failing_keys, None)
