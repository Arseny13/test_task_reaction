from django.urls import path, re_path

from .views import BlogDetail, BlogList


urlpatterns = [
    path('', BlogList.as_view()),
    re_path(r'(?P<blog_id>\d+)', BlogDetail.as_view()),
]
