from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils.text import slugify
from blog.models import Blogger, Category, Tag, BlogPost
from django.core.files.base import ContentFile
from django.conf import settings
import os

class Command(BaseCommand):
    help = 'Creates sample data for the blog including bloggers, categories, tags, and posts'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creating sample data...')

        # Create categories
        categories = {
            'Technology': 'Articles about technology, programming, and digital trends',
            'Travel': 'Travel experiences, tips, and destination guides',
            'Food & Cooking': 'Recipes, cooking tips, and food reviews',
            'Science': 'Scientific discoveries, research, and explanations',
            'Lifestyle': 'Personal development, health, and daily life tips',
            'Business': 'Business insights, entrepreneurship, and market trends'
        }

        for name, description in categories.items():
            Category.objects.get_or_create(
                name=name,
                defaults={'description': description}
            )
            self.stdout.write(f'Created category: {name}')

        # Create tags
        tags = [
            'Python', 'Django', 'Web Development', 'Programming',
            'Travel Tips', 'Adventure', 'Food', 'Recipes',
            'Science', 'Research', 'Technology', 'Innovation',
            'Lifestyle', 'Health', 'Business', 'Entrepreneurship'
        ]

        for tag_name in tags:
            Tag.objects.get_or_create(name=tag_name)
            self.stdout.write(f'Created tag: {tag_name}')

        # Create sample bloggers
        bloggers = [
            {
                'username': 'tech_enthusiast',
                'email': 'john@example.com',
                'password': 'testpass123',
                'first_name': 'John',
                'last_name': 'Smith',
                'bio': 'Tech enthusiast and software developer passionate about creating innovative solutions.'
            },
            {
                'username': 'travel_lover',
                'email': 'sarah@example.com',
                'password': 'testpass123',
                'first_name': 'Sarah',
                'last_name': 'Johnson',
                'bio': 'Travel blogger exploring the world one destination at a time.'
            },
            {
                'username': 'foodie_chef',
                'email': 'maria@example.com',
                'password': 'testpass123',
                'first_name': 'Maria',
                'last_name': 'Garcia',
                'bio': 'Professional chef sharing recipes and cooking tips.'
            },
            {
                'username': 'science_geek',
                'email': 'david@example.com',
                'password': 'testpass123',
                'first_name': 'David',
                'last_name': 'Wilson',
                'bio': 'Science writer making complex topics accessible to everyone.'
            }
        ]

        for blogger_data in bloggers:
            user, created = User.objects.get_or_create(
                username=blogger_data['username'],
                defaults={
                    'email': blogger_data['email'],
                    'first_name': blogger_data['first_name'],
                    'last_name': blogger_data['last_name']
                }
            )
            if created:
                user.set_password(blogger_data['password'])
                user.save()
                Blogger.objects.create(
                    user=user,
                    bio=blogger_data['bio']
                )
                self.stdout.write(f'Created blogger: {blogger_data["username"]}')

        # Create sample blog posts
        blog_posts = [
            {
                'title': 'Getting Started with Django: A Beginner\'s Guide',
                'content': '''
# Getting Started with Django: A Beginner's Guide

Django is a high-level Python web framework that enables rapid development of secure and maintainable websites. In this comprehensive guide, we'll explore the basics of Django and how to get started with your first project.

## Why Choose Django?

Django follows the "batteries included" philosophy, providing everything you need to build a web application. Here are some key benefits:

- Built-in admin interface
- Robust security features
- Scalable architecture
- Extensive documentation
- Large community support

## Setting Up Your First Project

1. Create a virtual environment
2. Install Django
3. Create a new project
4. Set up your first app

## Next Steps

Stay tuned for more detailed tutorials on Django development!
                ''',
                'category': 'Technology',
                'tags': ['Python', 'Django', 'Web Development'],
                'author': 'tech_enthusiast',
                'status': 'published'
            },
            {
                'title': 'Exploring the Hidden Gems of Southeast Asia',
                'content': '''
# Exploring the Hidden Gems of Southeast Asia

Southeast Asia is a treasure trove of unique experiences, from pristine beaches to ancient temples. Let's explore some of the region's lesser-known destinations.

## Off-the-Beaten-Path Destinations

1. Koh Rong, Cambodia
2. Luang Prabang, Laos
3. Banaue Rice Terraces, Philippines

## Travel Tips

- Best time to visit
- Local customs and etiquette
- Budget-friendly accommodations
- Transportation options

## Personal Experiences

Share your own experiences and tips in the comments below!
                ''',
                'category': 'Travel',
                'tags': ['Travel Tips', 'Adventure'],
                'author': 'travel_lover',
                'status': 'published'
            },
            {
                'title': 'The Art of Making Perfect Sushi at Home',
                'content': '''
# The Art of Making Perfect Sushi at Home

Making sushi at home might seem daunting, but with the right techniques and ingredients, you can create restaurant-quality rolls in your own kitchen.

## Essential Ingredients

- Sushi rice
- Nori sheets
- Fresh fish
- Vegetables
- Rice vinegar

## Step-by-Step Guide

1. Prepare the rice
2. Cut the fish
3. Roll the sushi
4. Slice and serve

## Tips for Success

- Keep your hands wet
- Use a sharp knife
- Maintain consistent pressure
- Practice makes perfect

Enjoy your homemade sushi!
                ''',
                'category': 'Food & Cooking',
                'tags': ['Food', 'Recipes'],
                'author': 'foodie_chef',
                'status': 'published'
            },
            {
                'title': 'The Future of Quantum Computing',
                'content': '''
# The Future of Quantum Computing

Quantum computing represents a paradigm shift in how we process information. Let's explore the potential impact and current developments in this fascinating field.

## Understanding Quantum Computing

- Quantum bits (qubits)
- Superposition
- Entanglement
- Quantum algorithms

## Current Applications

1. Cryptography
2. Drug discovery
3. Climate modeling
4. Financial modeling

## Future Prospects

The potential applications of quantum computing are vast and exciting. Stay tuned for more developments in this field!
                ''',
                'category': 'Science',
                'tags': ['Science', 'Technology', 'Innovation'],
                'author': 'science_geek',
                'status': 'published'
            }
        ]

        for post_data in blog_posts:
            author = Blogger.objects.get(user__username=post_data['author'])
            category = Category.objects.get(name=post_data['category'])
            
            post, created = BlogPost.objects.get_or_create(
                title=post_data['title'],
                defaults={
                    'content': post_data['content'],
                    'author': author,
                    'category': category,
                    'status': post_data['status'],
                    'slug': slugify(post_data['title'])
                }
            )
            
            if created:
                for tag_name in post_data['tags']:
                    tag = Tag.objects.get(name=tag_name)
                    post.tags.add(tag)
                self.stdout.write(f'Created blog post: {post_data["title"]}')

        self.stdout.write(self.style.SUCCESS('Successfully created sample data!')) 