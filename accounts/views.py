from django.shortcuts import render,redirect
from django.views.generic import FormView,CreateView,View,TemplateView
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView,LogoutView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate,login
from . import forms
from django.urls import reverse_lazy
from books.models import CreateBookBorrowedHistory
from django.core.mail import EmailMessage,EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

# Create your views here.

class UserSignupView(UserPassesTestMixin,FormView):
    template_name = 'signup.html'
    model = User
    form_class = forms.UserSignUpForm
    success_url = reverse_lazy('home')
    def test_func(self):
        return not self.request.user.is_authenticated

    def handle_no_permission(self):
        return redirect('profile') 
    def form_valid(self, form):
        form.save()
        username = form.cleaned_data.get('username') 
        password = form.cleaned_data.get('password1') 
        authuser = authenticate(username=username, password=password) 
        if authuser is not None:
            login(self.request, authuser)
        return super().form_valid(form)

class UserLoginView(UserPassesTestMixin,LoginView):
    template_name = 'login.html'
    form_class = AuthenticationForm
    success_url = reverse_lazy('home')

    def test_func(self):
        return not self.request.user.is_authenticated

    def handle_no_permission(self):
        return redirect('profile') 
    
    def get_success_url(self) -> str:
        return self.success_url
    def form_valid(self, form):
        username = form.cleaned_data.get('username') 
        password = form.cleaned_data.get('password1') 
        authuser = authenticate(username=username, password=password) 
        if authuser is not None:
            login(self.request, authuser)
        return super().form_valid(form)

class UserLogoutView(LoginRequiredMixin,LogoutView):
    next_page = 'home'


class UserDepositView(LoginRequiredMixin,FormView):
    template_name = 'deposit.html'
    form_class = forms.UserDepositForm
    success_url = reverse_lazy('home')

    def send_transaction_email(self, msg, amount, type):
        mail_subject=msg
        message = render_to_string('deposit_email.html', {'user':self.request.user, 'amount':amount, 'type': type})
        to_email = self.request.user.email
        send_email = EmailMultiAlternatives(mail_subject,'',to=[to_email])
        send_email.attach_alternative(message, 'text/html')
        send_email.send()

    def form_valid(self, form):
        amount = form.cleaned_data['deposit_amount']
        account = self.request.user.account
        account.balance += amount
        account.save(
            update_fields = ['balance']
        )
        self.send_transaction_email('Deposit Message', amount, 'Deposite')
        return super().form_valid(form)

class UserProfileView(LoginRequiredMixin,TemplateView):
    template_name = 'profile.html'
    def get_context_data(self,*args,**kwargs):
        context = super().get_context_data(*args,**kwargs)
        context['histories'] = CreateBookBorrowedHistory.objects.filter(user=self.request.user)
        return context

class UserBookReturn(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        borrowed_book_id = kwargs.get('id')
        borrowed_book = CreateBookBorrowedHistory.objects.get(pk=borrowed_book_id)
        account = request.user.account
        account.balance += borrowed_book.book_price
        borrowed_book.book_return = True
        borrowed_book.save(
            update_fields= ['book_return']
        )
        account.save(
            update_fields=['balance']
        )
        return redirect('profile')