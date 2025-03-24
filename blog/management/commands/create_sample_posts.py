from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from blog.models import Blogger, Category, Tag, BlogPost, Comment
from django.utils.text import slugify
import random

class Command(BaseCommand):
    help = 'Creates sample blog posts'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating sample blog posts...')

        # Sample data
        posts_data = [
            {
                'title': 'Getting Started with Django',
                'content': '''
Django is a powerful web framework that makes it easy to build web applications quickly. In this post, we'll explore the basics of Django and how to get started with your first project.

First Steps:
1. Install Django using pip: `pip install django`
2. Create a new project: `django-admin startproject myproject`
3. Create a new app: `python manage.py startapp myapp`
4. Add your app to INSTALLED_APPS
5. Define your models
6. Create and apply migrations
7. Create your views and templates

Django follows the MVT (Model-View-Template) pattern, which is similar to MVC but with Django's own terminology:
- Models define your database structure
- Views handle the business logic
- Templates manage how data is displayed

Stay tuned for more Django tutorials!
                '''.strip(),
                'category': 'Technology',
                'tags': ['Django', 'Python', 'Web Development', 'Tutorial']
            },
            {
                'title': 'Python Tips and Tricks',
                'content': '''
Python is known for its simplicity and readability, but there are many lesser-known features that can make your code even more elegant and efficient.

Here are some useful Python tips:

1. List Comprehensions
Instead of:
```python
squares = []
for i in range(10):
    squares.append(i * i)
```

Use:
```python
squares = [i * i for i in range(10)]
```

2. The Walrus Operator (:=)
New in Python 3.8, it allows assignment within expressions:
```python
if (n := len(data)) > 10:
    print(f"List is too long ({n} elements)")
```

3. F-strings for Debugging
```python
x = 100
print(f"{x=}")  # Output: x=100
```

4. The zip() Function
```python
names = ['Alice', 'Bob']
scores = [85, 92]
for name, score in zip(names, scores):
    print(f"{name}: {score}")
```

These are just a few examples of Python's powerful features. What are your favorite Python tricks?
                '''.strip(),
                'category': 'Programming',
                'tags': ['Python', 'Tips', 'Programming', 'Tutorial']
            },
            {
                'title': 'Web Security Best Practices',
                'content': '''
Security is crucial for any web application. Here are some essential security practices every developer should follow:

1. Input Validation
- Always validate and sanitize user input
- Use parameterized queries to prevent SQL injection
- Escape special characters to prevent XSS attacks

2. Authentication & Authorization
- Implement strong password policies
- Use secure session management
- Apply the principle of least privilege
- Enable two-factor authentication when possible

3. Data Protection
- Use HTTPS everywhere
- Hash passwords with strong algorithms
- Encrypt sensitive data
- Regularly backup your data

4. Security Headers
- Set appropriate security headers
- Enable CSRF protection
- Configure CORS properly

5. Regular Updates
- Keep all dependencies up to date
- Monitor security advisories
- Conduct regular security audits

Remember: Security is not a one-time task but an ongoing process.
                '''.strip(),
                'category': 'Security',
                'tags': ['Security', 'Web Development', 'Best Practices']
            }
        ]

        # Get or create user
        user = User.objects.first()
        if not user:
            user = User.objects.create_user(
                username='tech_blogger',
                password='password123',
                email='tech@example.com',
                first_name='Tech',
                last_name='Blogger'
            )
            self.stdout.write(f'Created user: {user.username}')

        # Get or create blogger
        blogger, created = Blogger.objects.get_or_create(
            user=user,
            defaults={'bio': 'A passionate tech blogger sharing insights about web development and programming.'}
        )
        if created:
            self.stdout.write(f'Created blogger profile for: {user.username}')

        # Create posts
        for post_data in posts_data:
            # Get or create category
            category, created = Category.objects.get_or_create(
                name=post_data['category'],
                slug=slugify(post_data['category'])
            )
            if created:
                self.stdout.write(f'Created category: {category.name}')

            # Create post
            post = BlogPost.objects.create(
                title=post_data['title'],
                slug=slugify(post_data['title']),
                content=post_data['content'],
                author=blogger,
                category=category
            )

            # Add tags
            for tag_name in post_data['tags']:
                tag, created = Tag.objects.get_or_create(
                    name=tag_name,
                    slug=slugify(tag_name)
                )
                if created:
                    self.stdout.write(f'Created tag: {tag_name}')
                post.tags.add(tag)

            # Add some sample comments
            comments = [
                'Great article! Very informative.',
                'Thanks for sharing these insights!',
                'Looking forward to more posts like this.',
                'This helped me understand the topic better.',
                'Could you elaborate more on point #3?'
            ]
            
            for _ in range(random.randint(2, 4)):
                Comment.objects.create(
                    post=post,
                    author=user,
                    content=random.choice(comments)
                )

            self.stdout.write(f'Created blog post: {post.title} with comments')

        self.stdout.write(self.style.SUCCESS('Successfully created sample blog posts')) 