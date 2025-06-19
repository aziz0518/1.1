from django.test import TestCase
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Author
from rest_framework import status
from datetime import date


class BookAPITestCase(APITestCase):
    def setUp(self):
        # Test user yaratamiz
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        
        # Author yaratamiz
        self.author = Author.objects.create(
            first_name='Abdulla',
            last_name='Qodiriy',
            birth_date=date(1950, 1, 1)
        )

        self.url = '/api/books/'

    def test_invalid_title(self):
        response = self.client.post(self.url, {
            "title": "Bo",  # < 3 ta belgidan iborat
            "author": self.author.id,
            "price": "10.00",
            "published_date": "2000-01-01"
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('title', response.data)

    def test_negative_price(self):
        response = self.client.post(self.url, {
            "title": "To‘g‘ri nom",
            "author": self.author.id,
            "price": "-10.00",  # manfiy narx
            "published_date": "2000-01-01"
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('price', response.data)

    def test_invalid_published_date(self):
        response = self.client.post(self.url, {
            "title": "Yana bir nom",
            "author": self.author.id,
            "price": "30.00",
            "published_date": "1900-01-01"  # muallif tug‘ilganidan oldin
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('published_date', response.data)

    def test_valid_book_create(self):
        response = self.client.post(self.url, {
            "title": "O‘tkan kunlar",
            "description": "Mashhur tarixiy roman",
            "author": self.author.id,
            "price": "50.00",
            "published_date": "2000-01-01"
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], "O‘tkan kunlar")
        self.assertEqual(response.data['created_by'], self.user.username)
