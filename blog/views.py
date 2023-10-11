from django.shortcuts import render,get_object_or_404, redirect
from .models import Post, Comment, Auther,Category
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .forms import CommentForm,PostForm
from django.views.decorators.http import require_POST
from taggit.models import Tag
from django.db.models import Count
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
# Create your views here.
def post_list(request, tag_slug=None):
    posts = Post.objects.filter(active=True)
    tag = None
    if tag_slug:
            tag = get_object_or_404(Tag, slug=tag_slug)
            posts = posts.filter(tags__in=[tag])
    tags =Tag.objects.all()
    categories = Category.objects.all()
    paginator = Paginator(posts, 2)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    new_posts = Post.objects.all().order_by('-date')[:2]
    return render(request, 'post_list.html', {'posts':posts,
                                              'categories':categories,
                                              'tag': tag,
                                              'tags': tags,
                                              'new_posts':new_posts})

def post_detail(request, slug ):    
    post = get_object_or_404(Post, slug= slug)
    comments = post.comments.all()
    form = CommentForm()
    
    # List of similar posts
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.objects.filter(tags__in=post_tags_ids)\
                                  .exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags'))\
                                 .order_by('-same_tags',)[:4]
    return render(request, 'post_detail.html', {'post':post,
                                                'comments':comments,
                                                'similar_posts': similar_posts,
                                                })
    
def category_list(request ,id):
    category = get_object_or_404(Category, id=id)
    return render(request, 'category_list.html', {'category':category})



@login_required
def comment_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comment = None
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.created_by = request.user
        comment.save()

    return render(request, 'comment_post.html',{'post':post,
                                               'form':form,
                                               'comment':comment})

    
@login_required
def add_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.auther = request.user
            return redirect(reverse('blog:post_list'))
    else:
        form = PostForm()
    return render(request, 'post_form.html', {'form': form})




class CreatePost(LoginRequiredMixin,CreateView):
  model = Post
  form_class = PostForm()
  template_name = 'post_form.html'
  success_url = reverse_lazy('post_list')

