from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.db.models import Q
from django.contrib.auth import login
from django.utils.text import slugify
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .models import BlogPost, Blogger, Category, Tag, Comment, Reaction
from .forms import CommentForm, UserRegistrationForm, BlogPostForm

def index(request):
    """Home page view introducing the blog site."""
    latest_posts = BlogPost.objects.filter(status='published').select_related('author', 'category')[:3]
    return render(request, 'blog/index.html', {'latest_posts': latest_posts})

class BlogListView(ListView):
    """View for displaying a list of blog posts with search and filtering."""
    model = BlogPost
    template_name = 'blog/blog_list.html'
    context_object_name = 'blog_posts'
    paginate_by = 5

    def get_queryset(self):
        queryset = BlogPost.objects.filter(status='published').select_related('author', 'category')
        
        # Search by title or content
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(content__icontains=search_query)
            )
        
        # Filter by category
        category_slug = self.request.GET.get('category')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        
        # Filter by tag
        tag_slug = self.request.GET.get('tag')
        if tag_slug:
            queryset = queryset.filter(tags__slug=tag_slug)
        
        # Filter by author
        author_id = self.request.GET.get('author')
        if author_id:
            queryset = queryset.filter(author_id=author_id)
        
        # Sort by date (newest/oldest)
        sort_by = self.request.GET.get('sort', '-created_at')
        if sort_by in ['created_at', '-created_at']:
            queryset = queryset.order_by(sort_by)
        
        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['tags'] = Tag.objects.all()
        context['bloggers'] = Blogger.objects.all()
        
        # Get current filters
        context['current_search'] = self.request.GET.get('search', '')
        context['current_category'] = self.request.GET.get('category', '')
        context['current_tag'] = self.request.GET.get('tag', '')
        context['current_author'] = self.request.GET.get('author', '')
        context['current_sort'] = self.request.GET.get('sort', '-created_at')
        
        return context

class BloggerListView(ListView):
    """View for listing all bloggers."""
    model = Blogger
    template_name = 'blog/blogger_list.html'
    context_object_name = 'bloggers'
    paginate_by = 9  # Show 9 bloggers per page (3x3 grid)

    def get_queryset(self):
        return Blogger.objects.select_related('user').order_by('user__first_name', 'user__last_name')

class BloggerDetailView(DetailView):
    """View for displaying blogger details and their posts."""
    model = Blogger
    template_name = 'blog/blogger_detail.html'
    context_object_name = 'blogger'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posts = BlogPost.objects.filter(
            author=self.object,
            status='published'
        ).select_related('category').order_by('-created_at')
        
        paginator = Paginator(posts, 5)
        page = self.request.GET.get('page')
        context['posts'] = paginator.get_page(page)
        return context

class BlogPostDetailView(DetailView):
    """View for displaying a single blog post."""
    model = BlogPost
    template_name = 'blog/blog_detail.html'
    context_object_name = 'blog_post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        
        # Get reaction counts
        post = self.get_object()
        context['likes_count'] = post.reactions.filter(reaction_type='like').count()
        context['dislikes_count'] = post.reactions.filter(reaction_type='dislike').count()
        
        # Get user's reaction if authenticated
        if self.request.user.is_authenticated:
            user_reaction = post.reactions.filter(user=self.request.user).first()
            context['user_reaction'] = user_reaction.reaction_type if user_reaction else None
        
        # Get related posts
        context['related_posts'] = BlogPost.objects.filter(
            category=post.category,
            status='published'
        ).exclude(id=post.id)[:3]
        
        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        
        self.object = self.get_object()
        comment_form = CommentForm(request.POST)
        
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = self.object
            comment.author = request.user
            comment.save()
            messages.success(request, 'Your comment has been added successfully!')
            return redirect(self.object.get_absolute_url())
        
        context = self.get_context_data(object=self.object)
        context['comment_form'] = comment_form
        return render(request, self.template_name, context)

@login_required
def add_comment(request, slug):
    """View for adding a comment to a blog post."""
    post = get_object_or_404(BlogPost, slug=slug, status='published')
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, 'Your comment has been added successfully!')
            return redirect('blog:blog-detail', slug=slug)
    else:
        form = CommentForm()
    
    return render(request, 'blog/add_comment.html', {
        'post': post,
        'comment_form': form,
    })

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create a blogger profile for the new user
            Blogger.objects.create(user=user, bio='')
            login(request, user)
            messages.success(request, 'Registration successful! Welcome to our blog.')
            return redirect('blog:index')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def create_blog_post(request):
    """View for creating a new blog post."""
    if request.method == 'POST':
        form = BlogPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user.blogger
            post.slug = slugify(post.title)
            post.save()
            # Save tags
            form.save_m2m()
            messages.success(request, 'Your blog post has been created successfully!')
            return redirect('blog:blog-detail', slug=post.slug)
    else:
        form = BlogPostForm()
    
    return render(request, 'blog/blog_form.html', {'form': form})

@login_required
def edit_blog_post(request, slug):
    """View for editing an existing blog post."""
    post = get_object_or_404(BlogPost, slug=slug, author=request.user.blogger)
    
    if request.method == 'POST':
        form = BlogPostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.slug = slugify(post.title)
            post.save()
            # Save tags
            form.save_m2m()
            messages.success(request, 'Your blog post has been updated successfully!')
            return redirect('blog:blog-detail', slug=post.slug)
    else:
        form = BlogPostForm(instance=post)
    
    return render(request, 'blog/blog_form.html', {'form': form})

@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.user == comment.author:
        post = comment.post
        comment.delete()
        messages.success(request, 'Your comment has been deleted successfully.')
    else:
        messages.error(request, 'You can only delete your own comments.')
    return redirect('blog:blog-detail', slug=post.slug)

@require_POST
@login_required
def react_to_post(request, slug):
    try:
        post = get_object_or_404(BlogPost, slug=slug)
        reaction_type = request.POST.get('reaction_type')
        
        if reaction_type not in ['like', 'dislike']:
            return JsonResponse({'error': 'Invalid reaction type'}, status=400)
        
        # Get or create the reaction
        reaction, created = Reaction.objects.get_or_create(
            post=post,
            user=request.user,
            defaults={'reaction_type': reaction_type}
        )
        
        if not created:
            # If user is clicking the same button, remove the reaction
            if reaction.reaction_type == reaction_type:
                reaction.delete()
                likes_count = post.reactions.filter(reaction_type='like').count()
                dislikes_count = post.reactions.filter(reaction_type='dislike').count()
                return JsonResponse({
                    'likes': likes_count,
                    'dislikes': dislikes_count,
                    'user_reaction': None
                })
            # If user is changing their reaction
            reaction.reaction_type = reaction_type
            reaction.save()
        
        # Get updated counts
        likes_count = post.reactions.filter(reaction_type='like').count()
        dislikes_count = post.reactions.filter(reaction_type='dislike').count()
        
        return JsonResponse({
            'likes': likes_count,
            'dislikes': dislikes_count,
            'user_reaction': reaction_type
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
