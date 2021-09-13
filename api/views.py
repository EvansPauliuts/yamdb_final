from django_filters.rest_framework.backends import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets
from rest_framework.decorators import permission_classes
from rest_framework.generics import get_object_or_404

from users.permissions import IsAdminOrReadOnly, ReviewCommentPermission

from .filters import TitleFilter
from .models import Categories, Comment, Genres, Review, Titles
from .serializers import (CategoriesSerializer, CommentSerializer,
                          GenresSerializer, ReviewSerializer,
                          TitlesCreateSerializer, TitlesSerializer)


class ListCreateDestroyViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    pass


@permission_classes((IsAdminOrReadOnly, ))
class CategoriesViewSet(ListCreateDestroyViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', ]
    lookup_field = 'slug'


@permission_classes((IsAdminOrReadOnly, ))
class GenresViewSet(ListCreateDestroyViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', ]
    lookup_field = 'slug'


@permission_classes((IsAdminOrReadOnly, ))
class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitlesSerializer
        return TitlesCreateSerializer


@permission_classes((ReviewCommentPermission, ))
class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    @staticmethod
    def get_title(pk):
        return get_object_or_404(Titles, id=pk)

    def get_queryset(self):
        title = self.get_title(self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Titles, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


@permission_classes((ReviewCommentPermission, ))
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    @staticmethod
    def get_review(pk, title):
        return get_object_or_404(Review, id=pk, title=title)

    def get_queryset(self):
        review = self.get_review(
            self.kwargs.get('review_id'),
            self.kwargs.get('title_id')
        )
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review, pk=self.kwargs.get('review_id')
        )
        serializer.save(author=self.request.user, review=review)
