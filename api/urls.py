from django.urls import include, path
from rest_framework.routers import SimpleRouter

from users.views import UserRegistrations, UserRegistrationsToken, UserViewSet

from .views import (CategoriesViewSet, CommentViewSet, GenresViewSet,
                    ReviewViewSet, TitlesViewSet)

router = SimpleRouter()

router.register(
    'users',
    UserViewSet, basename='users'
)
router.register('categories', CategoriesViewSet)
router.register('genres', GenresViewSet)
router.register('titles', TitlesViewSet)
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet
)


urlpatterns = [
    path('v1/email/', UserRegistrations.as_view()),
    path('v1/auth/token/', UserRegistrationsToken.as_view()),
    path('v1/', include(router.urls)),
]
