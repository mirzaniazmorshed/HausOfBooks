from django.contrib import admin
from .models import CreateBook,CreateBookReview, CreateCategory, CreateBookBorrowedHistory

# Register your models here.
admin.site.register(CreateBook)
admin.site.register(CreateBookReview)
admin.site.register(CreateBookBorrowedHistory)


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('category_name',)}
    list_display = ['category_name', 'slug']
admin.site.register(CreateCategory, CategoryAdmin)