from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = 'categories'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Tag(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Blogger(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(help_text="Enter your biographical information")
    profile_picture = models.ImageField(upload_to='blogger_profiles/', blank=True, null=True)
    website = models.URLField(blank=True)
    # Add social media fields
    twitter_handle = models.CharField(max_length=50, blank=True, help_text="Your Twitter handle without @")
    linkedin_profile = models.URLField(blank=True, help_text="Your LinkedIn profile URL")
    github_profile = models.URLField(blank=True, help_text="Your GitHub profile URL")
    instagram_handle = models.CharField(max_length=50, blank=True, help_text="Your Instagram handle without @")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username}"

    def get_absolute_url(self):
        return reverse('blog:blogger-detail', args=[str(self.id)])

    def get_twitter_url(self):
        if self.twitter_handle:
            return f"https://twitter.com/{self.twitter_handle}"
        return None

    def get_instagram_url(self):
        if self.instagram_handle:
            return f"https://instagram.com/{self.instagram_handle}"
        return None

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    author = models.ForeignKey(Blogger, on_delete=models.CASCADE, related_name='posts')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='posts')
    tags = models.ManyToManyField(Tag, related_name='posts')
    status = models.CharField(max_length=10, choices=[
        ('draft', 'Draft'),
        ('published', 'Published')
    ], default='draft')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:blog-detail', args=[str(self.slug)])

    def get_reading_time(self):
        """Calculate estimated reading time in minutes."""
        # Average reading speed (words per minute)
        WORDS_PER_MINUTE = 200
        
        # Count words in content
        words = len(self.content.split())
        
        # Calculate reading time
        reading_time = round(words / WORDS_PER_MINUTE)
        
        # Return at least 1 minute
        return max(1, reading_time)

class Comment(models.Model):
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']  # Oldest to newest as per requirements

    def __str__(self):
        return f"{self.content[:75]}..."  # Truncate to 75 chars as per requirements

    def get_absolute_url(self):
        return reverse('blog:blog-detail', kwargs={'slug': self.post.slug}) + f'#comment-{self.id}'

class Reaction(models.Model):
    """Model for handling like/dislike reactions on blog posts."""
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='reactions')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reaction_type = models.CharField(max_length=10, choices=[
        ('like', 'Like'),
        ('dislike', 'Dislike')
    ])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['post', 'user']  # One reaction per user per post
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} {self.reaction_type}d {self.post.title}"
