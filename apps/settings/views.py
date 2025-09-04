from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import generics, viewsets, filters, permissions
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from .models import Library, Book, Borrowing, Reader, Author
from .serializers import (
    LibrarySerilizer, BookSerializer, BookDetailSerializer,
    ReaderSerializer, AuthorSerializer, RegisterAuthorSerializer,
    LoginAuthorSerializer
)
from .pagination import SettingsPagination
from .filters import BookFilter


# ================== Автор ==================
class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAuthenticated]


class RegisterAuthorAPI(generics.CreateAPIView):
    queryset = Author.objects.all()
    serializer_class = RegisterAuthorSerializer


class LoginAuthorAPI(generics.GenericAPIView):
    serializer_class = LoginAuthorSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        author = serializer.validated_data["author"]
        return Response({
            "id": author.id,
            "email": author.email,
            "name": author.name
        })


# ================== Книги ==================
@method_decorator(cache_page(60), name='dispatch')
class BookAPIList(GenericViewSet, ListModelMixin):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    pagination_class = SettingsPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_class = BookFilter
    search_fields = ['title', 'description']
    ordering_fields = ['price', 'published_year', 'created_at']


class BookAPI(GenericViewSet,
              CreateModelMixin,
              RetrieveModelMixin,
              UpdateModelMixin,
              DestroyModelMixin):
    queryset = Book.objects.all()
    serializer_class = BookDetailSerializer


class BookViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


# ================== Заимствования ==================
class BorrowingViewSet(viewsets.ModelViewSet):
    queryset = Borrowing.objects.all()
    serializer_class = ReaderSerializer

    def get_queryset(self):
        user = self.request.user
        return Borrowing.objects.filter(reader__user=user)

    @action(detail=True, methods=['post'])
    def return_book(self, request, pk=None):
        borrowing = get_object_or_404(Borrowing, pk=pk, reader__user=request.user)
        if borrowing.returned:
            return Response({"detail": "Книга уже возвращена"}, status=400)
        borrowing.mark_as_returned()
        return Response({"detail": "Книга успешно возвращена"})
