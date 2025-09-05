from django.shortcuts import render, redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from blog.models.post import Post
from tag.models import Tag
from tag.forms import TagForm

@login_required
def tag_view(request, tag_slug):
    posts = Post.objects.filter(tag__slug=tag_slug)
    try:
        tag = Tag.objects.get(slug=tag_slug)
    except:
        messages.error(request,f"{tag_slug} is not a valid tag")
        return redirect('home')
    paginator = Paginator(posts, 4)
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    context = {"page_obj": page_obj, "tag_name": tag.name}
    return render(request, ("blog/post_list.html"), context)
    
@login_required
def create_tag(request):
    if request.user.user_role not in ['W', 'A']:
        messages.error(request, "You cannot create a tag since you are not a writer or an admin")
        return redirect('home')
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Tag created successfully")
            return redirect('home')
        else:
            messages.error(request, "Error creating tag. Please check the form.")
            return redirect('home')
    form = TagForm()
    context = {'form': form}
    return render(request, 'create_tag.html', context)

