from django.contrib.auth.models import User

from rest_framework import serializers

from example.models import (
    AuthorType,
    Author,
    AuthorBio,
    Book,
    Comment
)


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class AuthorTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthorType
        fields = ('name', )


class AuthorBioSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthorBio
        fields = ('body',)


class AuthorSerializer(serializers.ModelSerializer):
    first_book = serializers.SerializerMethodField()
    bio = AuthorBioSerializer()
    author_type = AuthorTypeSerializer()

    def get_first_book(self, obj):
        return str(obj.books.first())

    class Meta:
        model = Author
        fields = ('name', 'email', 'bio', 'first_book', 'comments', 'author_type')


class AuthorNameSerializer(serializers.ModelSerializer):
    author_type = AuthorTypeSerializer()

    class Meta:
        model = Author
        fields = ('name', 'author_type')


class CommentSerializer(serializers.ModelSerializer):
    author = AuthorNameSerializer()

    class Meta:
        model = Comment
        exclude = ('id', 'book', 'created_at', 'updated_at',)


class BookSerializer(serializers.ModelSerializer):
    authors = AuthorNameSerializer(many=True)
    comments = CommentSerializer(many=True)

    def update(self, instance, validated_data):
        Author.objects.filter(books=instance).delete()
        Comment.objects.filter(book=instance).delete()

        authors = validated_data.pop('authors', [])
        comments = validated_data.pop('comments', [])
        new_title = validated_data.pop('title', None)

        if new_title:
            instance.title = new_title

        instance.authors.clear()
        for author in authors:
            instance.authors.add(
                Author.objects.get(name=author['name'])
            )

        for comment in comments:
            Comment.objects.create(book=instance, **comment)
        instance.save()
        return instance

    class Meta:
        model = Book
        fields = ('title', 'authors', 'comments')
