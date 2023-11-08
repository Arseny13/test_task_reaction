import pytest


@pytest.fixture
def blog(user):
    from blog.models import Blog
    return Blog.objects.create(
        name='Блог 1',
        text='Тестовый блог 1',
        user=user
    )


@pytest.fixture
def another_blog(another_user):
    from blog.models import Blog
    return Blog.objects.create(
        name='Блог 2',
        text='Тестовый блог 2',
        user=another_user
    )
