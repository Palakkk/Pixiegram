from django.urls import path
from social.views import *
urlpatterns = [
    path("",index,name='index'),
    path("index/",index,name='index'),
    path("login/",login,name='login1'),
    path("register/",register,name='register1'),
    path('forgot-Password',forgot,name='forgot'),
    path("profile/<int:user_id>/",profile,name='profile1'),
    path("edit-profile",edit_profile,name='edit_profile1'),
    path("edit-about",edit_about,name='edit_about1'),
    path("message/",message,name='message1'),
    # path('search/',searchview,name="search"),
    path('search-profile/',searchview,name="search_profile"),
    path("logout/",logout,name='logout1'),
    # path('like-post', like_post, name='like-post'),
    path('like_post/<int:post_id>', like_post, name='like_post'),
    path('follow', follow, name='follow1'),
    path('add_comment', add_comment, name='add_comment'),
]