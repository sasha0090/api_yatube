from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from posts.models import Comment, Group, Post

from .serializer import CommentSerializer, GroupSerializer, PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied("Нельзя менять чужой контент!")
        super(PostViewSet, self).perform_create(serializer)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"message": "Пост удален."}, status=status.HTTP_204_NO_CONTENT
        )

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied("Нельзя удалять чужой контент!")
        instance.delete()


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(viewsets.ModelViewSet):

    serializer_class = CommentSerializer

    def get_queryset(self):
        post_id = self.kwargs.get("post_id")
        return Comment.objects.filter(post_id=post_id)

    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs.get("post_id"))

        post_data = {"post": post, "author": self.request.user}

        serializer.save(**post_data)

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied("Нельзя менять чужой комментарий!")
        super(CommentViewSet, self).perform_create(serializer)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"message": "Комментарий удален."},
            status=status.HTTP_204_NO_CONTENT,
        )

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied("Нельзя удалять чужой комментарий!")
        instance.delete()
