from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Category, Tag, Blogger, BlogPost, Comment

class ModelTests(TestCase):
    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        # Create test blogger
        self.blogger = Blogger.objects.create(
            user=self.user,
            bio='Test bio'
        )
        
        # Create test category
        self.category = Category.objects.create(
            name='Test Category',
            slug='test-category'
        )
        
        # Create test tag
        self.tag = Tag.objects.create(
            name='Test Tag',
            slug='test-tag'
        )
        
        # Create test blog post
        self.blog_post = BlogPost.objects.create(
            title='Test Blog Post',
            slug='test-blog-post',
            author=self.blogger,
            content='Test content',
            category=self.category,
            status='published'
        )
        self.blog_post.tags.add(self.tag)
        
        # Create test comment
        self.comment = Comment.objects.create(
            post=self.blog_post,
            author=self.user,
            content='Test comment'
        )

    def test_model_fields(self):
        """Test model field labels and lengths"""
        # Category fields
        category = Category.objects.get(id=self.category.id)
        self.assertEqual(category._meta.get_field('name').max_length, 100)
        self.assertTrue(category._meta.get_field('slug').unique)
        
        # BlogPost fields
        blog_post = BlogPost.objects.get(id=self.blog_post.id)
        self.assertEqual(blog_post._meta.get_field('title').max_length, 200)
        self.assertTrue(blog_post._meta.get_field('slug').unique)
        
        # Comment ordering
        self.assertEqual(Comment._meta.ordering, ['created_at'])

    def test_object_name_is_correct(self):
        """Test that objects are correctly named"""
        self.assertEqual(str(self.category), 'Test Category')
        self.assertEqual(str(self.tag), 'Test Tag')
        self.assertEqual(str(self.blogger), self.user.username)
        self.assertEqual(str(self.blog_post), 'Test Blog Post')
        self.assertEqual(str(self.comment), 'Test comment...')

    def test_get_absolute_url(self):
        """Test get_absolute_url() returns correct URL"""
        self.assertEqual(
            self.blog_post.get_absolute_url(),
            reverse('blog:blog-detail', kwargs={'slug': 'test-blog-post'})
        )
        self.assertEqual(
            self.blogger.get_absolute_url(),
            reverse('blog:blogger-detail', args=[str(self.blogger.id)])
        )

class BlogListViewTests(TestCase):
    def setUp(self):
        # Create test user and blogger
        user = User.objects.create_user(username='testuser', password='testpass123')
        blogger = Blogger.objects.create(user=user, bio='Test bio')
        category = Category.objects.create(name='Test Category', slug='test-category')
        
        # Create 6 blog posts for pagination tests
        for i in range(6):
            BlogPost.objects.create(
                title=f'Test Blog Post {i}',
                slug=f'test-blog-post-{i}',
                author=blogger,
                content=f'Test content {i}',
                category=category,
                status='published'
            )

    def test_view_url_exists_at_desired_location(self):
        """Test that the blog list view exists at the expected location"""
        response = self.client.get('/blog/blogs/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        """Test that the blog list view is accessible by its name"""
        response = self.client.get(reverse('blog:blog-list'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        """Test that the blog list view uses the correct template"""
        response = self.client.get(reverse('blog:blog-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/blog_list.html')

    def test_pagination_is_five(self):
        """Test that the blog list view paginates by 5"""
        response = self.client.get(reverse('blog:blog-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'])
        self.assertEqual(len(response.context['posts']), 5)
