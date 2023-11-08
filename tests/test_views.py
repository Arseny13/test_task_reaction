from http import HTTPStatus

import pytest
from blog.models import Blog


class TestBlogAPI:
    VALID_DATA = {'text': 'Поменяли текст статьи'}

    def test_blog_not_found(self, client, blog):
        response = client.get('/blogs/')

        assert response.status_code != HTTPStatus.NOT_FOUND, (
            'Страница `/blogs/` не найдена, проверьте этот адрес в '
            '*urls.py*.'
        )

    def test_blog_not_auth(self, client, blog):
        response = client.get('/blogs/')

        assert response.status_code == HTTPStatus.OK, (
            'Проверьте, что при GET-запросе неавторизованного пользователя к '
            '`/blogs/` возвращается ответ со статусом 200.'
        )

    def check_post_data(self,
                        response_data,
                        request_method_and_url,
                        db_blog=None):
        expected_fields = ('id', 'name', 'text', 'user', 'create_date')
        for field in expected_fields:
            assert field in response_data, (
                'Проверьте, что для авторизованного пользователя ответ на '
                f'{request_method_and_url} содержит поле `{field}` блогов.'
            )
        if db_blog:
            assert response_data['id'] == db_blog.id, (
                'Проверьте, что при запросе авторизованного пользователя к '
                f'{request_method_and_url} в ответе содержится корректный '
                '`id` блога.'
            )

    @pytest.mark.django_db(transaction=True)
    def test_posts_auth_get(self, user_client, blog, another_blog):
        response = user_client.get('/blogs/')
        assert response.status_code == HTTPStatus.OK, (
            'Проверьте, что для авторизованного пользователя GET-запрос к '
            '`/blogs/` возвращает статус 200.'
        )

        test_data = response.json()
        assert isinstance(test_data, list), (
            'Проверьте, что для авторизованного пользователя GET-запрос к '
            '`/blogs//` возвращает список.'
        )

        assert len(test_data) == Blog.objects.count(), (
            'Проверьте, что для авторизованного пользователя GET-запрос к '
            '`/blogs/` возвращает список всех постов.'
        )

        db_blog = Blog.objects.first()
        test_blog = test_data[0]
        self.check_post_data(
            test_blog,
            'GET-запрос к `/blogs/`',
            db_blog
        )
