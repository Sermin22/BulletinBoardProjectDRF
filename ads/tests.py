from rest_framework import status
from rest_framework.test import APITestCase
from users.models import CustomUser
from django.urls import reverse
from ads.models import Advertisement, Comment
from rest_framework.fields import DateTimeField


class AdvertisementTestCase(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(email="test@mail.ru")
        self.advertisement = Advertisement.objects.create(
            author=self.user,
            title="Делаю ремонты",
            price=50000,
            description="Ремонты качественные и недорого"
        )
        self.client.force_authenticate(user=self.user)

    def test_advertisement_retrieve(self):
        '''Проверяем вывод объявления'''
        url = reverse("ads:ads_retrieve", args=[self.advertisement.pk])
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data.get("title"), "Делаю ремонты"
        )

    def test_advertisement_create(self):
        '''Проверяем создание объявления'''
        url = reverse("ads:ads_create")
        data = {
            "author": self.user,
            "title": "Lada Vesta",
            "price": 900000,
            "description": "Автомобиль почти новый в отличном состоянии"
        }
        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED
        )
        self.assertEqual(
            Advertisement.objects.all().count(), 2
        )
        result = response.json()
        self.assertEqual(
            result.get("description"), "Автомобиль почти новый в отличном состоянии"
        )

    def test_advertisement_update(self):
        '''Проверяем изменение объявления'''
        url = reverse("ads:ads_update", args=[self.advertisement.pk])
        data = {
            "description": "Ремонты быстро, качественно и недорого"
        }
        response = self.client.patch(url, data)
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        result = response.json()
        self.assertEqual(
            result.get("description"), "Ремонты быстро, качественно и недорого"
        )

    def test_advertisement_delete(self):
        '''Проверяем удаление объявления'''
        url = reverse("ads:ads_delete", args=[self.advertisement.pk])
        response = self.client.delete(url)
        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT
        )
        self.assertEqual(
            Advertisement.objects.all().count(), 0
        )

    def test_advertisement_list(self):
        '''Проверяем вывод списка объявлений'''
        url = reverse("ads:ads_list")
        response = self.client.get(url)
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        data = response.json()
        expected = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.advertisement.id,
                    "title": self.advertisement.title,
                    "price": self.advertisement.price,
                    "description": self.advertisement.description,
                    "image": None,
                    "author": {
                        "id": self.user.id,
                        "username": self.user.username,
                        "first_name": "",
                        "last_name": "",
                        "is_superuser": False,
                        "is_staff": False,
                        "is_active": True,
                        "date_joined": DateTimeField().to_representation(self.user.date_joined),
                        "email": self.user.email,
                        "phone": None,
                        "role": "user",
                        "image": None
                    },
                    "created_at": DateTimeField().to_representation(self.advertisement.created_at),
                    "comments": [],
                }
            ]
        }
        self.assertEqual(data, expected)


class CommentTestCase(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(email="test@mail.ru")
        self.advertisement = Advertisement.objects.create(
            author=self.user,
            title="Делаю ремонты",
            price=50000,
            description="Ремонты качественные и недорого"
        )
        self.comment = Comment.objects.create(
            author=self.user,
            text="Сегодня делали проемы, все сделали супер!",
            advertisement=self.advertisement
        )
        self.client.force_authenticate(user=self.user)

    def test_comment_detail(self):
        '''Проверяем вывод комментария'''
        url = reverse("ads:comment_detail", args=[self.comment.pk])
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data.get("text"), "Сегодня делали проемы, все сделали супер!"
        )

    def test_comment_create(self):
        '''Проверяем создание комментария'''
        url = reverse("ads:comment_create")
        data = {
            "text": "Каменщик молодец! Ровно новую стенку выложил",
            "advertisement": self.advertisement.id
        }
        response = self.client.post(url, data=data)
        # response = self.client.post("/ads/comments/create/", data=data)
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED
        )
        self.assertEqual(
            Comment.objects.all().count(), 2
        )
        result = response.json()
        self.assertEqual(
            result.get("text"), "Каменщик молодец! Ровно новую стенку выложил"
        )

    def test_advertisement_comment_create(self):
        '''Проверяем создание комментария к конкретному объявлению по вложенному пути'''
        url = reverse("ads:ads_comment_create", args=[self.advertisement.id])
        data = {
            "text": "Каменщик молодец! Ровно новую стенку выложил"
        }
        response = self.client.post(url, data=data)
        # response = self.client.post("/ads/ads/1/comments/create/", data=data)  # вариант вложенного урла - работает
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED
        )
        self.assertEqual(
            Comment.objects.all().count(), 2
        )
        result = response.json()
        self.assertEqual(
            result.get("text"), "Каменщик молодец! Ровно новую стенку выложил"
        )

    def test_comment_update(self):
        '''Проверяем изменение комментария'''
        url = reverse("ads:comment_update", args=[self.comment.pk])
        data = {
            "text": "Ремонты любой сложности"
        }
        response = self.client.patch(url, data)
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        result = response.json()
        self.assertEqual(
            result.get("text"), "Ремонты любой сложности"
        )

    def test_comment_delete(self):
        '''Проверяем удаление комментария'''
        url = reverse("ads:comment_delete", args=[self.comment.pk])
        response = self.client.delete(url)
        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT
        )
        self.assertEqual(
            Comment.objects.all().count(), 0
        )

    def test_comment_list(self):
        '''Проверяем вывод списка комментариев'''
        url = reverse("ads:comment_list")
        response = self.client.get(url)
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        data = response.json()
        expected = [
            {
                "id": self.comment.id,
                "text": self.comment.text,
                "author": {
                    "id": self.user.id,
                    "username": self.user.username,
                    "first_name": "",
                    "last_name": "",
                    "is_superuser": False,
                    "is_staff": False,
                    "is_active": True,
                    "date_joined": DateTimeField().to_representation(self.user.date_joined),
                    "email": self.user.email,
                    "phone": None,
                    "role": "user",
                    "image": None
                },
                "advertisement": self.advertisement.id,
                "created_at": DateTimeField().to_representation(self.comment.created_at)
            },
        ]
        self.assertEqual(data, expected)

    def test_advertisement_comment_list(self):
        '''Проверяем вывод списка комментариев конкретного объявления'''
        # response = self.client.get("/ads/ads/1/comments/")  # вариант вложенного урла - работает
        url = reverse("ads:ads_comments", args=[self.advertisement.id])
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        expected = [
            {
                "id": self.comment.id,
                "text": self.comment.text,
                "author": {
                    "id": self.user.id,
                    "username": self.user.username,
                    "first_name": "",
                    "last_name": "",
                    "is_superuser": False,
                    "is_staff": False,
                    "is_active": True,
                    "date_joined": DateTimeField().to_representation(self.user.date_joined),
                    "email": self.user.email,
                    "phone": None,
                    "role": "user",
                    "image": None
                },
                "advertisement": self.advertisement.id,
                "created_at": DateTimeField().to_representation(self.comment.created_at)
            },
        ]
        self.assertEqual(data, expected)
