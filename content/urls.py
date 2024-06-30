from django.urls import path
from .views import PostListCreateAPIView, PostDetailAPIView, LikePostAPIView, CommentPostAPIView, UserProfileAPIView, SearchAPIView

urlpatterns = [
    path('posts/', PostListCreateAPIView.as_view(), name='post_list_create'),
    path('posts/<int:pk>', PostDetailAPIView.as_view(), name='post_detail'),
    path('posts/like/<int:pk>', LikePostAPIView.as_view(), name='post_like'),
    path('posts/comment/<int:pk>', CommentPostAPIView.as_view(), name='post_comment'),
    path('profile/<int:pk>', UserProfileAPIView.as_view(), name='user_profile'),
    path('search', SearchAPIView.as_view(), name='post_search'),
]
