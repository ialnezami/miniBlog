from django.contrib import admin
from .models import Article, Category, Tag, Comment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'status', 'created_at', 'published_at', 'ai_checked', 'ai_score']
    list_filter = ['status', 'created_at', 'published_at', 'category', 'ai_checked']
    search_fields = ['title', 'content', 'excerpt']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    
    fieldsets = (
        ('Contenu', {
            'fields': ('title', 'slug', 'content', 'excerpt', 'status')
        }),
        ('Métadonnées', {
            'fields': ('author', 'category', 'tags', 'featured_image', 'meta_description')
        }),
        ('IA Content Check', {
            'fields': ('ai_checked', 'ai_score', 'ai_feedback'),
            'classes': ('collapse',)
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at', 'published_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at', 'published_at']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author_name', 'article', 'created_at', 'is_approved']
    list_filter = ['is_approved', 'created_at']
    search_fields = ['author_name', 'content']
    actions = ['approve_comments', 'disapprove_comments']
    
    def approve_comments(self, request, queryset):
        queryset.update(is_approved=True)
    approve_comments.short_description = "Approuver les commentaires sélectionnés"
    
    def disapprove_comments(self, request, queryset):
        queryset.update(is_approved=False)
    disapprove_comments.short_description = "Désapprouver les commentaires sélectionnés"
