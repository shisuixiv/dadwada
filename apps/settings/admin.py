from django.contrib import admin
from apps.settings.models import Library, Book, Author
# Register your models here.

admin.site.register(Library)
admin.site.register(Author)
admin.site.register(Book)