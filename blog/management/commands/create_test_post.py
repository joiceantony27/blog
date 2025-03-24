from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from blog.models import Blogger, Category, Tag, BlogPost
from django.utils.text import slugify

class Command(BaseCommand):
    help = 'Creates a test blog post'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating test blog post...')

        # Get or create a user
        user = User.objects.first()
        if not user:
            user = User.objects.create_user(
                username='test_user',
                password='password123',
                email='test@example.com'
            )
            self.stdout.write(f'Created user: {user.username}')

        # Get or create blogger
        blogger, created = Blogger.objects.get_or_create(
            user=user,
            defaults={'bio': 'A passionate blogger sharing insights about technology and programming.'}
        )
        if created:
            self.stdout.write(f'Created blogger profile for: {user.username}')

        # Get or create category
        category, created = Category.objects.get_or_create(
            name='Technology',
            slug='technology'
        )
        if created:
            self.stdout.write(f'Created category: Technology')

        # Get or create tag
        tag, created = Tag.objects.get_or_create(
            name='Django',
            slug='django'
        )
        if created:
            self.stdout.write(f'Created tag: Django')

        # Create blog post
        post = BlogPost.objects.create(
            title='Welcome to Django Blog',
            slug='welcome-to-django-blog',
            content='''
Welcome to our Django Blog!

This is a test post to verify that our blog system is working correctly.

Django is a high-level Python web framework that encourages rapid development and clean, pragmatic design. Built by experienced developers, it takes care of much of the hassle of web development, so you can focus on writing your app without needing to reinvent the wheel.

Key Features of Django:
- Ridiculously fast
- Reassuringly secure
- Exceedingly scalable
- Incredibly versatile
- Remarkably maintainable

In this blog, we will explore:
1. Django development tips and tricks
2. Best practices for web development
3. Python programming insights
4. Web security considerations
5. Performance optimization techniques

Stay tuned for more interesting articles!
            '''.strip(),
            author=blogger,
            category=category
        )
        post.tags.add(tag)
        
        self.stdout.write(f'Created blog post: {post.title}')
        self.stdout.write(self.style.SUCCESS('Successfully created test blog post')) 