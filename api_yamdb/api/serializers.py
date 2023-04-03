from datetime import date

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from reviews.models import (Category, Comment, Genre, Review, Title,
                            TitleGenre, User)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role',
        )
        model = User


class UserOwnerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role',
        )
        model = User
        read_only_fields = ('role',)


class RegistrationDataSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('username', 'email',)
        model = User

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(f'{value} isn\'t valid username')
        return value


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Category


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'title', 'text', 'author', 'score', 'pub_date',
        )
        model = Review

    def validate(self, data):
        self.get_queryset()


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'id', 'text', 'author', 'pub_date',
        )
        model = Comment


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitleGETSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(source='average_rating', read_only=True)
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)

    class Meta:
        fields = ('id', 'name', 'year', 'rating', 'description', 'category',
                  'genre')
        model = Title


class TitlePOSTSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(source='average_rating', read_only=True)
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug',
        read_only=False
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        read_only=False,
        many=True
    )

    class Meta:
        fields = ('id', 'name', 'year', 'rating', 'description', 'category',
                  'genre')
        model = Title

    def validate_year(self, value):
        year = date.today().year
        if value > year:
            raise serializers.ValidationError(
                'Field "year" is required or field "year" can\'t be greater '
                f'than current year: {year}'
            )
        return value

    def create(self, validated_data):
        category = validated_data.pop('category')
        genres = validated_data.pop('genre')
        title = Title.objects.create(category=category,
                                     **validated_data)
        for genre in genres:
            title.genre.add(genre)
            TitleGenre.objects.get_or_create(title=title, genre=genre)
        return title

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.year = validated_data.get('year', instance.year)
        instance.description = validated_data.get('description',
                                                  instance.description)
        instance.category = validated_data.get('category', instance.category)
        if validated_data.get('genre') is not None:
            instance.genre.add(validated_data.get('genre'))
        instance.save()
        return instance
