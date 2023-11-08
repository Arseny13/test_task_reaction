from blog.models import Blog
from django.test import TestCase
from users.models import User


class BlogModelTest(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.user = User.objects.create_user(username='test_user')
        cls.blog = Blog.objects.create(
            user=cls.user,
            name='Тест',
            text='Тестовый пост',
        )

    def test_models_have_correct_object_names(self):
        """Проверяем, что у модели корректно работает __str__."""
        blog = BlogModelTest.blog
        self.assertEqual(str(blog), blog.name)

    def test_verbose_name(self):
        """verbose_name в полях совпадает с ожидаемым."""
        blog = BlogModelTest.blog
        field_verboses = {
            'user': 'Пользователь',
            'name': 'Имя записи',
            'text': 'Текст',
            'create_date': 'Дата заказа',
            'publish': 'Опубликована ли запись'
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    blog._meta.get_field(field).verbose_name, expected_value
                )
