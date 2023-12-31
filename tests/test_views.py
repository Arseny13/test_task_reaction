from http import HTTPStatus

import pytest
from blog.models import Blog


class TestBlogAPI:
    VALID_DATA = {
        'name': 'Поменяли название',
        'text': 'Поменяли текст',
        'publish': False
    }

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

    def check_blog_data(
        self,
        response_data,
        request_method_and_url,
        db_blog=None
    ):
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

    def check_blog_data_without_user(
        self, response_data,
        request_method_and_url,
        db_blog=None
    ):
        expected_fields = ('id', 'name', 'text', 'create_date')
        for field in expected_fields:
            assert field in response_data, (
                'Проверьте, что для авторизованного пользователя ответ на '
                f'{request_method_and_url} содержит поле `{field}` блогов.'
            )

    @pytest.mark.django_db(transaction=True)
    def test_blogs_auth_get(self, user_client, blog, another_blog):
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
        self.check_blog_data(
            test_blog,
            'GET-запрос к `/blogs/`',
            db_blog
        )

    @pytest.mark.django_db(transaction=True)
    def test_blog_create_auth_with_invalid_data(self, user_client):
        posts_count = Blog.objects.count()
        response = user_client.post('/blogs/', data={})
        assert response.status_code == HTTPStatus.BAD_REQUEST, (
            'Проверьте, что для авторизованного пользователя POST-запрос с '
            'некорректными данными к `/blogs/` возвращает ответ со '
            'статусом 400.'
        )
        assert posts_count == Blog.objects.count(), (
            'Проверьте, что POST-запрос к `/blogs/` с некорректными '
            'данными не создает новый blog.'
        )

    @pytest.mark.django_db(transaction=True)
    def test_blog_create_auth_with_valid_data(self, user_client, user):
        post_count = Blog.objects.count()

        data = {
            'name': 'Blog номер 3',
            'text': 'Blog номер 3',
            'publish': False
        }
        response = user_client.post('/blogs/', data=data)
        assert response.status_code == HTTPStatus.CREATED, (
            'Проверьте, что для авторизованного пользователя  POST-запрос с '
            'корректными данными к `/blogs/` возвращает ответ со '
            'статусом 201.'
        )

        test_data = response.json()
        assert isinstance(test_data, dict), (
            'Проверьте, что для авторизованного пользователя POST-запрос к '
            '`/blogs/` возвращает ответ, содержащий данные нового '
            'поста в виде словаря.'
        )
        self.check_blog_data_without_user(test_data, 'POST-запрос к `/blogs/`')
        assert test_data.get('text') == data['text'], (
            'Проверьте, что для авторизованного пользователя POST-запрос к '
            '`/blogs/` возвращает ответ, содержащий текст нового '
            'поста в неизменном виде.'
        )
        assert test_data.get('user') is None, (
            'Проверьте, что для авторизованного пользователя при создании '
            'поста через POST-запрос к `/blogs/` ответ не содержит поле '
            '`user` с именем пользователя, отправившего запрос.'
        )
        assert post_count + 1 == Blog.objects.count(), (
            'Проверьте, что POST-запрос с корректными данными от '
            'авторизованного пользователя к `/blogs/` создает новый '
            'пост.'
        )

    @pytest.mark.django_db(transaction=True)
    def test_blog_unauth_create(self, client, user, another_user):
        posts_conut = Blog.objects.count()

        data = {
            'name': 'Blog номер 3',
            'text': 'Blog номер 3',
            'publish': False
        }
        response = client.post('/blogs/', data=data)
        assert response.status_code == HTTPStatus.UNAUTHORIZED, (
            'Проверьте, что POST-запрос неавторизованного пользователя к '
            '`/blogs/` возвращает ответ со статусом 401.'
        )

        assert posts_conut == Blog.objects.count(), (
            'Проверьте, что POST-запрос неавторизованного пользователя к '
            '`/blogs/` не создает новый пост.'
        )

    @pytest.mark.django_db(transaction=True)
    @pytest.mark.parametrize('http_method', ('put', 'patch'))
    def test_blog_change_auth_with_valid_data(self, user_client, blog,
                                              http_method):
        request_func = getattr(user_client, http_method)
        response = request_func(f'/blogs/{blog.id}/',
                                data=self.VALID_DATA)
        http_method = http_method.upper()
        assert response.status_code == HTTPStatus.OK, (
            f'Проверьте, что для авторизованного пользователя {http_method}'
            '-запрос к `/blogs/{id}/` вернётся ответ со статусом '
            '200.'
        )

        test_blog = Blog.objects.filter(id=blog.id).first()
        assert test_blog, (
            f'Проверьте, что {http_method}-запрос авторизованного '
            'пользователя к `/blogs/{id}/` не удаляет редактируемый '
            'пост.'
        )
        assert test_blog.text == self.VALID_DATA['text'], (
            f'Проверьте, что {http_method}-запрос авторизованного '
            'пользователя к `/api/v1/posts/{id}/` вносит изменения в блог.'
        )

    @pytest.mark.django_db(transaction=True)
    @pytest.mark.parametrize('http_method', ('put', 'patch'))
    def test_blog_change_not_author_with_valid_data(self, user_client,
                                                    another_blog, http_method):
        request_func = getattr(user_client, http_method)
        response = request_func(f'/blogs/{another_blog.id}/',
                                data=self.VALID_DATA)
        http_method = http_method.upper()
        assert response.status_code == HTTPStatus.FORBIDDEN, (
            f'Проверьте, что {http_method}'
            '-запрос авторизованного пользователя к `/blogs/{id}/` '
            'для чужого поста возвращает ответ со статусом 403.'
        )

        db_blog = Blog.objects.filter(id=another_blog.id).first()
        assert db_blog.text != self.VALID_DATA['text'], (
            f'Проверьте, что {http_method}'
            '-запрос авторизованного пользователя к `/blogs/{id}/` '
            'для чужого поста не вносит изменения в пост.'
        )

    @pytest.mark.django_db(transaction=True)
    def test_blog_delete_by_author(self, user_client, blog):
        response = user_client.delete(f'/blogs/{blog.id}/')
        assert response.status_code == HTTPStatus.NO_CONTENT, (
            'Проверьте, что для автора поста DELETE-запрос к '
            ' `/blogs/` возвращает ответ со статусом 204.'
        )

        test_blog = Blog.objects.filter(id=blog.id).first()
        assert not test_blog, (
            'Проверьте, что DELETE-запрос автора поста к '
            ' `blogs/{id}/` удаляет этот пост.'
        )

    @pytest.mark.django_db(transaction=True)
    def test_blog_delete_not_author(self, user_client, another_blog):
        response = user_client.delete(f'/blogs/{another_blog.id}/')
        assert response.status_code == HTTPStatus.FORBIDDEN, (
            'Проверьте, что DELETE-запрос авторизованного пользователя к '
            '`/blogs/{id}/` чужого поста '
            'вернёт ответ со статусом 403.'
        )

        test_blog = Blog.objects.filter(id=another_blog.id).first()
        assert test_blog, (
            'Проверьте, что авторизованный пользователь не может удалить '
            'чужой пост.'
        )
