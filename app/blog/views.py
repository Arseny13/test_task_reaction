from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Blog
from .permissions import IsReadOnly
from .serializers import (
    BlogBaseSerializer, BlogPostSerializer, BlogUpdateSerializer,
)


class BlogList(APIView):
    permission_classes = (IsReadOnly,)
    serializer_class = BlogBaseSerializer

    def get(self, request):
        """Получение всех блогов."""
        blogs = Blog.objects.all().select_related('user')
        serializer = BlogBaseSerializer(blogs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """Cоздание блога блога."""
        context = {
            'request': self.request,
        }
        serializer = BlogPostSerializer(data=request.data, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class BlogDetail(APIView):
    permission_classes = (IsReadOnly,)
    serializer_class = BlogBaseSerializer

    def get_object(self, blog_id: int):
        return get_object_or_404(Blog, id=blog_id)

    def get(self, request, blog_id: int):
        """Получение блога."""
        blog = self.get_object(blog_id)
        serializer = BlogBaseSerializer(blog)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, blog_id: int):
        """Изменение блога."""
        blog = self.get_object(blog_id)
        serializer = BlogUpdateSerializer(blog, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.check_object_permissions(request, blog)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, blog_id: int):
        """Частичное изменение блога."""
        blog = self.get_object(blog_id)
        serializer = BlogUpdateSerializer(
            blog, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        self.check_object_permissions(request, blog)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, blog_id: int):
        """Удаление блога"""
        blog = self.get_object(blog_id)
        self.check_object_permissions(request, blog)
        blog.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
