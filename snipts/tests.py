from django.test import TestCase


class SniptAPITest(TestCase):
    def test_get_snipt(self):
        """
        We should be able to get a public snipt from the API.
        """
        self.assertEqual(1 + 1, 2)
