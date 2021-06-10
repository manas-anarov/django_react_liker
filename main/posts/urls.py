from . import views
from django.urls import path

urlpatterns = [
    path('like/', views.LikePost.as_view(), name='post-like'),
    path('list/', views.PostListAPIView.as_view(), name='post-list'),
    path('add/', views.AddPost.as_view(), name='post-add'),
    path('<id>/', views.ShowPost.as_view(), name='post-show'),
    path('delete/<id>/', views.DeletePost.as_view(), name='post-delete'),
    path('edit/<id>/', views.UpdatePost.as_view(), name='post-update'),
]
