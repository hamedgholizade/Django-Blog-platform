__all__ = [
    'login',
    'logout',
    'post_list',
    'post_details',
    'post_search',
    'home_view',
    'create_post',
    'post_like',
    'user_registration'
]

from blog.views.user_authentication import user_registration, login, logout
from blog.views.post_views import post_list, post_details, post_search, create_post, post_like
from blog.views.index_view import home_view
