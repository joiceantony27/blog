from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.index, name='index'),
    path('blogs/', views.BlogListView.as_view(), name='blog-list'),
    path('blogs/<slug:slug>/', views.BlogPostDetailView.as_view(), name='blog-detail'),
    path('blogs/<slug:slug>/react/', views.react_to_post, name='react-to-post'),
    path('blogs/<slug:slug>/comment/', views.add_comment, name='add-comment'),
    path('comment/<int:pk>/delete/', views.delete_comment, name='delete-comment'),
    path('bloggers/', views.BloggerListView.as_view(), name='blogger-list'),
    path('bloggers/<int:pk>/', views.BloggerDetailView.as_view(), name='blogger-detail'),
    path('blog/create/', views.create_blog_post, name='create-blog'),
    path('blog/<slug:slug>/edit/', views.edit_blog_post, name='edit-blog'),
    path('register/', views.register, name='register'),
] 