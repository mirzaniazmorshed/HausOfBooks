from django.urls import path
from . import views
urlpatterns = [
    path('details/<int:id>', views.BookDetailsView.as_view(), name="book_details"),
    path('borrow/<int:id>', views.BookBorrowView.as_view(), name='book_borrow')

]
