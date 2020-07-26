from django.urls import path
from .views import SignUpView,ProfileUpdateView,LoginView,LogoutView,UserBlogListView

app_name = 'useraccounts'

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('edit/<int:author_id>/', ProfileUpdateView.as_view(), name='edit'),
    path('<str:author>/<int:author_id>/',UserBlogListView.as_view(), name='blog_list'),
    path('logout/', LogoutView.as_view(), name='logout'),
    # path('activate/<uidb64>/<token>/',ActivateView.as_view(), name='activate'),
]
