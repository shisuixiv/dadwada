from django.urls import path

from rest_framework.routers import DefaultRouter
from apps.settings.views import BookAPI, BookAPIList, BorrowingViewSet, BookViewSet

router = DefaultRouter()
router.register('book-list', BookAPIList, basename='book-list')
router.register('book', BookAPI, basename='book')
router.register(r'books', BookViewSet, basename='book-lists')
router.register(r'borrowing', BorrowingViewSet, basename='borrowing')


urlpatterns = [   
]
urlpatterns += router.urls



# from apps.settings.views import LibraryAPIView, BookAPIView, BookCreateAPIView, BookRetrieveAPIVIEW, BookUdateAPIView, BookDeleteAPIView

# urlpatterns = [
#     path("list-library", LibraryAPIView.as_view(), name='list-library'),
#     path("book-list", BookAPIView.as_view(), name='book-list'),
#     path("book-create/", BookCreateAPIView.as_view(), name='book-create'),
#     path("book-detail/<int:pk>/", BookRetrieveAPIVIEW.as_view(), name='detail-book'),
#     path("book-update/<int:pk>/", BookUdateAPIView.as_view(), name='book-update'),
#     path("book-delete/<int:pk>/", BookDeleteAPIView.as_view(), name='book-delete')
# ]