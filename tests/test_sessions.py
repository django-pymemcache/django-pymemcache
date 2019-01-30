from django.contrib.sessions.backends.cache import SessionStore
from django.test import TestCase


class SessionTestCase(TestCase):
    def setUp(self):
        self.session = SessionStore()

    def tearDown(self):
        self.session.delete()

    def test_set_and_get(self):
        self.session['spam'] = 'egg'
        self.assertEqual(self.session.get('spam'), 'egg')

    def test_set_and_pop(self):
        self.session['spam'] = 'egg'
        self.assertEqual(self.session.pop('spam'), 'egg')
        self.assertIsNone(self.session.get('spam'))

    def test_pop_no_default_keyerror_raised(self):
        with self.assertRaises(KeyError):
            self.session.pop('spam')

    def test_update(self):
        self.session.update({'update key': 1})
        self.assertEqual(self.session.get('update key', None), 1)

    def test_has_key(self):
        self.session['spam'] = 'egg'
        self.assertIn('spam', self.session)

    def test_values(self):
        self.assertEqual(list(self.session.values()), [])
        self.session['spam'] = 'egg'
        self.assertEqual(list(self.session.values()), ['egg'])

    def test_keys(self):
        self.assertEqual(list(self.session.values()), [])
        self.session['spam'] = 'egg'
        self.assertEqual(list(self.session.keys()), ['spam'])

    def test_items(self):
        self.session['spam'] = 'egg'
        self.assertEqual(list(self.session.items()), [('spam', 'egg')])

    def test_clear(self):
        self.session['spam'] = 'egg'
        self.session.clear()
        self.assertEqual(list(self.session.items()), [])

    def test_save(self):
        self.session.save()
        self.assertIs(self.session.exists(self.session.session_key), True)

    def test_delete(self):
        self.session.save()
        self.session.delete(self.session.session_key)
        self.assertIs(self.session.exists(self.session.session_key), False)

    def test_flush(self):
        self.session['spam'] = 'egg'
        self.session.save()
        prev_key = self.session.session_key
        self.session.flush()
        self.assertNotEqual(self.session.session_key, prev_key)
        self.assertIsNone(self.session.session_key)
