from django.urls import path
from . import views
from django.contrib.auth.views import LoginView

app_name='blog'

urlpatterns = [
    path('',views.PostListView.as_view(),name="post_list"),
    path('post/<int:pk>/',views.PostDetailView.as_view(),name="post_detail"),
    path('accounts/login/',views.loginpage,name="login"),
    path('logout/',views.logoutuser,name="logout"),
    path('register/',views.registerpage,name="register"),
    path('drafts/',views.DraftListView.as_view(),name='drafts'),
    
    path('post/new',views.CreatePost.as_view(),name="create_post"),
    path('post/<int:pk>/publish/',views.post_publish,name="post_publish"),
    path('post/<int:pk>/edit/',views.PostUpdateView.as_view(),name="post_edit"),
    path('post/<int:pk>/remove/',views.PostDeleteView.as_view(),name="post_remove"),

    path('post/<int:pk>/comment/',views.add_comment_to_post,name="add_comment_to_post"),
    path('comment/<int:pk>/approve/',views.comment_approve,name="comment_approve"),
    path('comment/<int:pk>/remove/',views.comment_remove,name="comment_remove"),
]
