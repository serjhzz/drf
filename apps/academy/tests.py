from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.users.models import User


class TestCourseEndPoints(APITestCase):
    def setUp(self):
        user = User.objects.create(email='test@gmail.com')
        user.set_password('test')
        user.save()

        token_url = reverse('user:token_obtain_pair')
        resp_token = self.client.post(
            path=token_url, data={'email': 'test@gmail.com', 'password': 'test'})
        token = resp_token.json().get('access')

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        self.client.post(
            reverse('course:create'), {'name': 'Course Test', 'description': 'test', 'price': 100})

    def test_course_create_endpoint(self):
        course_create_url = reverse('course:create')
        course_data = {'name': 'Course Test1', 'description': 'test1', 'price': 200}
        response = self.client.post(course_create_url, course_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_course_list_endpoint(self):
        url = reverse('course:list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json().get('results')), 1)

    def test_course_retrieve_endpoint(self):
        list_response = self.client.get(reverse('course:list'))

        pk = list_response.json()['results'][0]['id']
        url = reverse('course:retrieve', kwargs={'pk': pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_course_update_endpoint(self):
        list_response = self.client.get(reverse('course:list'))

        pk = list_response.json()['results'][0]['id']
        url = reverse('course:update', kwargs={'pk': pk})
        response = self.client.put(path=url, data={'name': 'Course Test2', 'description': 'test2'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['description'], 'test2')

    def test_course_delete_endpoint(self):
        list_response = self.client.get(reverse('course:list'))

        pk = list_response.json()['results'][0]['id']
        url = reverse('course:delete', kwargs={'pk': pk})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
