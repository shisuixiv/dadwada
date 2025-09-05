from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.settings.views import BookAPI, BookAPIList, BorrowingViewSet, BookViewSet

router = DefaultRouter()
router.register('book-list', BookAPIList, basename='book-list')
router.register('book', BookAPI, basename='book')
router.register(r'books', BookViewSet, basename='book-lists')
router.register(r'borrowing', BorrowingViewSet, basename='borrowing')

urlpatterns = []
urlpatterns += router.urls
