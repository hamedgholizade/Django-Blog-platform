from django.urls import path
from tag.views import tag_view, create_tag

app_name = 'tag'

urlpatterns = [
    path('create_tag/', create_tag, name='create_tag'),
    path('<slug:tag_slug>/', tag_view, name='tag_view'),
    
]

