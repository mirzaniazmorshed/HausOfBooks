from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class CreateCategory(models.Model):
    category_name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, null=True, blank=True, unique=True)

    def __str__(self) -> str:
        return self.category_name

class CreateBook(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='books/media/uploads/', blank=True, null=True)
    price = models.DecimalField(max_digits=12,decimal_places=2)
    categories = models.ManyToManyField(CreateCategory, related_name='book')
   
    def __str__(self) -> str:
        return self.title

class CreateBookReview(models.Model):
    book = models.ForeignKey(CreateBook, on_delete=models.CASCADE, related_name='reviews')
    name = models.CharField(max_length=50)
    email = models.EmailField()
    body  = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.book.title}-{self.email}'
    

class CreateBookBorrowedHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='history')
    book_name = models.CharField(max_length=100)
    book_price = models.IntegerField()
    after_balance = models.DecimalField(max_digits=12, decimal_places=2)
    book_return = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    

