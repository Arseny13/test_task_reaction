from blog.models import Blog
from django.test import Client, TestCase
from users.models import User


class PostsPagesTests(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        """Создание фикстур для тестов."""
        super().setUpClass()
        cls.user = User.objects.create_user(
            username='admin',
            is_superuser=True
        )
        cls.blog = Blog.objects.create(
            user=cls.user,
            name='Тест',
            text='Тестовый пост',
        )

    def setUp(self):
        """Создание клиентов."""
        self.author_client = Client()
        self.author_client.force_login(PostsPagesTests.user)
        self.user = User.objects.create_user(username='Test')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_get_list_blogs(self):
        response = self.author_client.get(
            '/blogs/'
        )
        self.assertEqual(
            len(response.data),
            1,
            'Не правильное количество блогов'
        )
        self.assertEqual(
            response.data[0].get('name'),
            self.blog.name,
            'Возвращает не то название блога'
        )
