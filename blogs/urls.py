from django.urls import path
from .views import CreatePostView, DisplayPostView, DeletePostView , UpdatePostView ,DetailPostView, UserDetailView

app_name = 'blogs'

urlpatterns=[
    path('',DisplayPostView.as_view(),name='display'),
    path('create/',CreatePostView.as_view(), name='create'),
    path('update/<int:blog_id>/',UpdatePostView.as_view(),name='update'),
    path('detail/<int:blog_id>/',DetailPostView.as_view(),name='detail'),
    path('delete/<int:blog_id>/',DeletePostView.as_view(),name='delete'),
    path('<str:author>/<int:author_id>/',UserDetailView.as_view(),name ='profile'),

]