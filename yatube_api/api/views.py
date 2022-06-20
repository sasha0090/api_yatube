from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .permissions import IsAuthorOrReadOnly
from .serializers import CommentSerializer, GroupSerializer, PostSerializer
from posts.models import Group, Post


class PostViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]
    serializer_class = CommentSerializer

    def get_queryset(self):
        post = get_object_or_404(Post, pk=self.kwargs.get("post_id"))
        return post.comments.all()

    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs.get("post_id"))

        post_data = {"post": post, "author": self.request.user}

        serializer.save(**post_data)
