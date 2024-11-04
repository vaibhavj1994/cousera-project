from django.test import TestCase
from rest_framework.test import APIClient #class from test module to make API calls 
from rest_framework import status
from django.contrib.auth.models import User

from restaurant_api.serializers import MenuSerializer
from restaurant.models import Menu

class MenuViewTest(TestCase):
    
    def setUp(self):
        # Create a test user for authenticated calls
        self.user = User.objects.create_user(username='testuser', password='password123')
        
        # Create an APIClient instance
        self.client = APIClient()
        
        # Authenticate using Djoser’s token endpoint
        response = self.client.post('/auth/token/login/', {
            'username': 'testuser',
            'password': 'password123'
        })
        self.token = response.data['auth_token']
        
        # Set the authentication header for the client
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        
        # creating menu instances for test purposes
        self.menu1 = Menu.objects.create(title='Test Dish 1', price=10.00)
        self.menu2 = Menu.objects.create(title='Test Dish 2', price=15.00)
        self.menu3 = Menu.objects.create(title='Test Dish 3', price=20.00)

    def test_getall(self):
        # GET call to Menu API
        response = self.client.get('/api/menu/')
        
        # Retrieving and Serializing
        menus = Menu.objects.all()
        serializer = MenuSerializer(menus, many=True)
        
        # Assert that the response status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Assert that the serialized data matches the response data
        self.assertEqual(response.data, serializer.data)
