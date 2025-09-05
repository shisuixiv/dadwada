from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class Library(models.Model):
    title = models.CharField(
        max_length=155,
        verbose_name='Заголовка'
    )
    description = models.TextField(
        verbose_name='Описание'
    )
    image = models.ImageField(
        upload_to='settings',
        verbose_name='Фото'
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Библиотека'
        verbose_name_plural = 'Библиотеки'




from django.db import models
from apps.users.models import User   # 👈 связь с User


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="author_profile")
    bio = models.TextField(blank=True, null=True, verbose_name="Биография")

    def __str__(self):
        return self.user.name


    

class Book(models.Model):
    title = models.CharField(max_length=155)
    desscription = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='author')
    published_year = models.PositiveIntegerField(blank=True, null=True, verbose_name='Год Публикаций')
    genre = models.CharField(
        max_length=155,
        verbose_name='Жанр',
        blank=True, null=True
    )
    pages = models.CharField(
        max_length=155,
        verbose_name='Кол-во Страниц',
        blank=True, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    update_at = models.DateTimeField(auto_now_add=True, verbose_name='Обновленр')

    def __str__(self):
        return self.title
        
    class Meta:
        verbose_name = ''
        verbose_name_plural = 'Книги'
        ordering = ['-created_at']

class Reader(models.Model):
    user = models.CharField(
        max_length=155,verbose_name='ПОльзователь'
    )



class Borrowing(models.Model):
    reader = models.ForeignKey(Reader, on_delete=models.CASCADE, verbose_name="Reader")
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrowed_at = models.DateTimeField(verbose_name='Date Borrowed', auto_now_add=True)
    urn_date = models.DateTimeField(verbose_name='Дата возврата')
    returned = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.pk:
            if self.book.available_copies <= 0:
                raise ValueError("Нет доступныйх копий книги!")
            self.book.available_copies -= 1
            self.book.save()
            self.save()

    def mark_as_returned(self):
        if not self.returned:
            self.returned = True
            self.book.available_copies += 1
            self.book.save()
            self.save()

    def __str__(self):
        return self.reader
    