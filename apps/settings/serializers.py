from rest_framework import serializers
from apps.settings.models import Library, Book, Author, Reader, Borrowing

from rest_framework import serializers
from .models import Author  


# ------------------ Автор ------------------
class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name', 'email']
        read_only_fields = ['id']


class RegisterAuthorSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = Author
        fields = ['id', 'name', 'email', 'password']

    def create(self, validated_data):
        author = Author.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            name=validated_data['name']
        )
        return author


class LoginAuthorSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            from django.contrib.auth import authenticate
            author = authenticate(username=email, password=password)
            if not author:
                raise serializers.ValidationError("Неверный email или пароль")
        else:
            raise serializers.ValidationError("Введите email и пароль")

        attrs['author'] = author
        return attrs

class LibrarySerilizer(serializers.ModelSerializer):
    class Meta:
        model = Library
        fields = ['id', 'title', 'description', 'image']


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ["id", 'title', 'desscription', 'author']

class BookDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ["id", 'title', 'desscription', 'price', 'author']

class ReaderSerializer(serializers.ModelSerializer):
    reader = serializers.PrimaryKeyRelatedField(read_only=True)
    book = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all())

    class Meta:
        model = Borrowing
        fields = ['id', 'reader', 'book', 'borrowed_at', 'return_date', 'returned']

    def create(self, validated_data):
        user = self.context['request'].user
        reader = Reader.objects.get(user=user)
        validated_data['reader'] = reader

        book = validated_data['book']
        if book.available_copies <= 0:
            raise serializers.ValidationError("Нет книг")

        borrowing = Borrowing.objects.create(**validated_data)
        return borrowing


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ["id", "email", "name", "bio"]
        read_only_fields = ["id"]
