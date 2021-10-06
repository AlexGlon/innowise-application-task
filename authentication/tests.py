from rest_framework.test import APITestCase


class UserAuthenticationTestCaseCore(APITestCase):
    def setUp(self):
        # Creating a new user by sending a POST request to Djoser endpoint
        self.user = self.client.post('/auth/users/', data={'username': 'testcaseuser',
                                                           'password': 'justatest'})
        # Obtaining a JSON web token for the newly created user
        response = self.client.post('/auth/jwt/create/', data={'username': 'testcaseuser',
                                                               'password': 'justatest'})
        self.token = response.data['access']
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
