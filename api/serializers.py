from django.core.validators import MinValueValidator, MaxValueValidator
from rest_framework import serializers

from .models import (
    Categories,
    Genres,
    Titles,
    GenreTitle,
    Review,
    Comment,
)


class CategoriesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Categories
        fields = ['name', 'slug']


class GenresSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genres
        fields = ['name', 'slug']


class TitlesSerializer(serializers.ModelSerializer):
    category = CategoriesSerializer(read_only=True)
    genre = GenresSerializer(many=True, read_only=True)
    rating = serializers.ReadOnlyField()

    class Meta:
        model = Titles
        fields = (
            'id',
            'name',
            'year',
            'category',
            'genre',
            'description',
            'rating',
        )


class TitlesCreateSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        required=False,
        slug_field='slug',
        queryset=Categories.objects.all()
    )
    genre = serializers.SlugRelatedField(
        required=False,
        many=True,
        slug_field='slug',
        queryset=Genres.objects.all()
    )

    class Meta:
        model = Titles
        fields = '__all__'

    def create(self, validated_data):
        genre = validated_data.pop('genre')
        title = self.Meta.model.objects.create(**validated_data)
        print('hello')

        data_list = []

        for gn in genre:
            obj, _ = Genres.objects.get_or_create(name=gn)
            data_list.append(GenreTitle(genre=obj, title=title))

        GenreTitle.objects.bulk_create(data_list)
        title.save()

        return title


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
    )
    title = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name'
    )
    score = serializers.IntegerField(
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1)
        ],
    )

    def validate(self, data):
        method = self.context.get('request').method
        author = self.context.get('request').user
        title_id = self.context.get('view').kwargs.get('title_id')

        review_result = Review.objects.filter(
            title=title_id,
            author=author
        ).exists()

        if method == 'POST' and review_result:
            raise serializers.ValidationError(
                'This user has already added review for this product'
            )
        return data

    class Meta:
        model = Review
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    review = serializers.SlugRelatedField(
        read_only=True,
        slug_field='text'
    )

    class Meta:
        model = Comment
        fields = '__all__'
