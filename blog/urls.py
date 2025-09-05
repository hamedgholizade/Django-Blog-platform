from django.urls import path
from blog.views.user_authentication import user_registration, user_login, user_logout
from blog.views.post_views import post_list, post_details, post_search, pending_posts, approve_post, create_post, pending_comments, approve_comments, hide_comments, post_like
from blog.views.index_view import home_view




# app_name = 'blog'

urlpatterns = [
    path('', home_view, name='home'),

    path('register/', user_registration, name='user_registration'),
    path('login/', user_login, name='user_login'),
    path('logout/', user_logout, name='user_logout'),

    path('blog/', post_list, name='post_list'),
    path('blog/pending-posts/', pending_posts, name='pending_posts'),
    path('blog/approve-post/<int:post_id>/', approve_post, name='approve_post'),
    path('blog/pending-comments/', pending_comments, name='pending_comments'),
    path('blog/approve-comments/<int:comment_id>/', approve_comments, name='approve_comments'),
    path('blog/hide-comments/<int:comment_id>/', hide_comments, name='hide_comments'),
    path('blog/search/', post_search, name='post_search'),
    path('blog/create_post/', create_post, name='create_post'),
    path('blog/<slug:post_slug>/', post_details, name='post_details'),
    path('blog/<slug:post_slug>/like/', post_like, name='post_like'),
]
