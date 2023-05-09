from django.test import TestCase, Client


class CsrfMiddlewareTestCase(TestCase):
    def setUp(self):
        self.client = Client(enforce_csrf_checks=True)

    def test_csrf_middleware(self):
        response = self.client.post(
            'http://127.0.0.1:8000', {'key': 'value'}, follow=True)

        self.assertEqual(response.status_code, 403)
        self.assertIn(b"CSRF verification failed", response.content)
        # pretty print the response

        # Use the CSRF token to make a valid POST request

        csrf_token = response.cookies['csrftoken'].value
        response = self.client.post(
            'http://127.0.0.1:8000', {'key': 'value', 'csrfmiddlewaretoken': csrf_token}, follow=True)
        self.assertEqual(response.status_code, 200)
