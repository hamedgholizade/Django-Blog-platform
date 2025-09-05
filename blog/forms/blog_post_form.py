from django import forms
from blog.models.post import Post
from tag.models import Tag



class BlogPostForm(forms.ModelForm):
    tag = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    class Meta:
        model = Post
        fields = ['title', 'content', 'image', 'tag']

