from django.contrib import admin
from .models import Category, Tag, Blogger, BlogPost, Comment

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

@admin.register(Blogger)
class BloggerAdmin(admin.ModelAdmin):
    list_display = ('user', 'website', 'created_at')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'bio')
    raw_id_fields = ('user',)

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    readonly_fields = ('created_at',)
    fields = ('author', 'content', 'created_at')
    raw_id_fields = ('author',)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('author')

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'status', 'created_at')
    list_filter = ('status', 'category', 'created_at', 'author')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    inlines = [CommentInline]
    date_hierarchy = 'created_at'

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('author', 'category')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('truncated_content', 'post', 'author', 'created_at')
    list_filter = ('created_at', 'post')
    search_fields = ('content', 'author__username', 'post__title')
    raw_id_fields = ('author', 'post')
    date_hierarchy = 'created_at'

    def truncated_content(self, obj):
        return str(obj)  # Uses the model's __str__ method which already truncates to 75 chars
    truncated_content.short_description = 'Comment'
