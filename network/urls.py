
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("profile/<id>",views.view_profile,name="view-profile"),
    path('follow/<pro_id>', views.follow_check, name='follow-check'),
    path('followingPosts/', views.view_following_posts, name='following-posts'),
    path('likePost/<post_id>',views.likePost,name='likePost'),
    path('EditPost/<id>',views.edit_post, name='Edit-post'),
    path('paginator/',views.testPaginator,name='test-paginator'),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
]
