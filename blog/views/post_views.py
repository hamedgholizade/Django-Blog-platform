from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib import messages

from blog.forms.blog_post_form import BlogPostForm
from blog.forms.comments_form import CommentForm
from blog.models.comment import Comment
from blog.models.post import Post



@login_required
def create_post(request):
    if request.user.user_role not in ['W', 'A']:
        messages.error(request, "You cannot create a blogpost since you are not a writer or an admin")
        return redirect('home')
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()
            form.save_m2m()

            # To keep the last five posts created by the user in session
            recent_user_posts = request.session.get('recent_user_posts', [])
            recent_user_posts.insert(0, new_post.id)
            request.session['recent_user_posts'] = recent_user_posts[:5]
            request.session.modified = True

            return redirect('post_details', post_slug=new_post.slug)
    else:
        form = BlogPostForm()

    return render(request, 'blog/blog_post.html', {'form': form})


@permission_required('blog.approve_post')
def approve_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.status = Post.POST_STATUS_CONFIRMED
    post.save()
    return redirect('post_list')


@permission_required('blog.approve_comment')
def approve_comments(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    comment.approve_comment()
    return redirect('pending_comments')


@permission_required('blog.hide_comment')
def hide_comments(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    comment.hide_comment()
    return redirect('pending_comments')


@login_required
def pending_posts(request):
    if request.user.user_role not in ['W', 'A']:
        messages.error(request, "You cannot access this url since you are not a writer or an admin")
        return redirect('home')
    posts = Post.objects.filter(status="P")
    context = {"posts": posts}
    return render(request, "blog/pending_posts.html", context)


@login_required
def pending_comments(request):
    if request.user.user_role not in ['W', 'A']:
        messages.error(request, "You cannot access this url since you are not a writer or an admin")
        return redirect('home')
    hidden_comments = Comment.objects.filter(is_shown=False).order_by('-created_at')
    approved_comments = Comment.objects.filter(is_shown=False).order_by('-created_at')
    context = {
        "approved_comments": approved_comments,
        "hidden_comments": hidden_comments,
        }
    return render(request, "blog/pending_comments.html", context)


@login_required
def post_details(request, post_slug):
    post = get_object_or_404(Post, slug=post_slug)
    user = request.user

    # Increment visit count
    post.visit_count += 1
    post.save()

    # Update session history
    recent_posts = request.session.get('history', [])
    if post_slug not in recent_posts:
        recent_posts.append(post_slug)
    recent = recent_posts[:5]
    request.session['history'] = recent

    # Handle comment form
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = user
            comment.save()
            messages.success(request, 'Comment added successfully')
            return redirect('post_details', post_slug=post_slug)
        else:
            messages.error(request, 'Invalid comment')
            return redirect('post_details', post_slug=post_slug)
    else:
        form = CommentForm()

    # return tags of the post
    tags = post.tag.all()
    tag_names = []
    for tag in tags:
        tag_names.append(tag)

    comments = Comment.objects.filter(post=post).order_by('-created_at').show_approved()
    context = {"post": post, "comments": comments, "form": form, "tag_names": tag_names}
    response = render(request, 'blog/post_details.html', context)
    response.set_cookie('last_viewed_post', post_slug, max_age=60*60*24*5)
    return response


@login_required
def post_list(request):
    posts = Post.objects.filter(status="C").order_by('-created_at')
    paginator = Paginator(posts, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        "page_obj": page_obj,
    }
    return render(request, 'blog/post_list.html', context)


@login_required
def post_search(request):
    posts = Post.objects.filter(status="C")
    if request.method == 'GET':
        search_query = request.GET.get("q")
        if search_query:
            posts = posts.filter(
                Q(content__icontains=search_query) |
                Q(title__icontains=search_query)
            )
    paginator = Paginator(posts, 4)
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    context = {"page_obj": page_obj, "search_query": search_query}
    return render(request, ("blog/post_list.html"), context)


@login_required
def post_like(request, post_slug):
    post = get_object_or_404(Post, slug=post_slug)
    user = request.user
    if user in post.likes.all():  
        post.likes.remove(user)
        post.like_count -= 1
        messages.success(request, 'Post unliked successfully')
    else:
        post.likes.add(user)
        post.like_count += 1
        messages.success(request, 'Post liked successfully')
    post.save()
    return redirect('post_details', post_slug=post_slug)
