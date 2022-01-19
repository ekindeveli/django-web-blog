from django.urls import path
from .views import PostListView, PostDetailView, PostCreateView, \
    PostUpdateView, PostDeleteView, UserPostListView, UserCommentListView, \
    CommentDeleteView, CommentUpdateView
from . import views

urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('user/<str:username>/posts', UserPostListView.as_view(), name='user-posts'),
    path('user/<str:username>/comments', UserCommentListView.as_view(), name='user-comments'),
    path('user/<str:username>/comments/<int:pk>/update', CommentUpdateView.as_view(), name='comment-update'),
    path('user/<str:username>/comments/<int:pk>/delete', CommentDeleteView.as_view(), name='comment-delete'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete', PostDeleteView.as_view(), name='post-delete'),
    path('about/', views.about, name='blog-about'),
]
