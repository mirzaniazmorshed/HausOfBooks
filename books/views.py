from typing import Any
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,redirect
from django.views.generic import TemplateView, View, FormView
from books.models import CreateBook, CreateBookBorrowedHistory,CreateBookReview
from .forms import CreateBookReviewForm
from django.urls import reverse, reverse_lazy
from django.core.mail import EmailMessage,EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

class BookDetailsView(FormView):
    template_name = 'book_details.html'
    form_class = CreateBookReviewForm
    def get_success_url(self):
        book_id = self.kwargs['id']
        return reverse('book_details', kwargs={'id': book_id})
    def form_valid(self, form):
        instance = form.save(commit=False)
        id = self.kwargs['id']
        book = CreateBook.objects.get(pk=id)
        instance.book = book
        instance.name = self.request.user.first_name + ' ' + self.request.user.last_name
        instance.email = self.request.user.email
        instance.save()
        return HttpResponseRedirect(self.get_success_url())
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        id = self.kwargs['id']
        book = CreateBook.objects.get(pk=id)
        context['details'] = book
        context['reviews'] = CreateBookReview.objects.filter(book=book)
        try:
            search = CreateBookBorrowedHistory.objects.get(book_name=book.title, user=self.request.user, book_return=False)
            if search.user.username == self.request.user.username:
                context['is_borrowed'] = True
            else:
                raise Exception("You are not authorized to buy this item.")
            
        except:
            context['is_borrowed'] = False
        return context

class BookBorrowView(LoginRequiredMixin,View):
    def send_transaction_email(self, msg, amount, type):
        mail_subject=msg
        message = render_to_string('deposit_email.html', {'user':self.request.user, 'amount':amount, 'type': type})
        to_email = self.request.user.email
        send_email = EmailMultiAlternatives(mail_subject,'',to=[to_email])
        send_email.attach_alternative(message, 'text/html')
        send_email.send()

    def get(self, request, *args, **kwargs):
        item_id = self.kwargs['id']
        book = CreateBook.objects.get(pk=item_id)
        account = request.user.account
        account.balance -= book.price
        account.save(
            update_fields = ['balance']
        )
        CreateBookBorrowedHistory.objects.create(
            user = request.user,
            book_name = book.title,
            book_price = book.price,
            after_balance = account.balance,
        )
        self.send_transaction_email('Book Borrowed Message', book.price, 'Book borrowed')
        return redirect('book_details', item_id)