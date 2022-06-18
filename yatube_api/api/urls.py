from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken import views

from api.views import CommentViewSet, GroupViewSet, PostViewSet

app_name = "api"

router = routers.DefaultRouter()
router.register(r"v1/posts", PostViewSet)
router.register(
    r"v1/posts/(?P<post_id>\d+)/comments",
    CommentViewSet,
    basename="CommentView",
)
router.register(r"v1/groups", GroupViewSet)


urlpatterns = [
    path("v1/api-token-auth/", views.obtain_auth_token),
    path("", include(router.urls)),
]