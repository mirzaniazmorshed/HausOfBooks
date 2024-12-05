from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.UserSignupView.as_view(), name='signup'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('deposit/', views.UserDepositView.as_view(), name='deposit'),
    path('profile/', views.UserProfileView.as_view(), name="profile"),
    path('booke_return/<int:id>/',views.UserBookReturn.as_view(), name="book_return")
]
