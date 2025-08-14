from rest_framework import serializers
from .models import Article, Category, Tag, Comment
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'created_at']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'author_name', 'author_email', 'content', 'created_at', 'is_approved']
        read_only_fields = ['created_at', 'is_approved']


class ArticleListSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    
    class Meta:
        model = Article
        fields = [
            'id', 'title', 'slug', 'excerpt', 'status', 'created_at', 
            'published_at', 'author', 'category', 'tags', 'featured_image',
            'ai_checked', 'ai_score', 'reading_time'
        ]


class ArticleDetailSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    
    class Meta:
        model = Article
        fields = [
            'id', 'title', 'slug', 'content', 'excerpt', 'status',
            'created_at', 'updated_at', 'published_at', 'author', 'category',
            'tags', 'featured_image', 'meta_description', 'ai_checked',
            'ai_score', 'ai_feedback', 'reading_time', 'comments'
        ]


class ArticleCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = [
            'title', 'content', 'excerpt', 'status', 'category', 'tags',
            'featured_image', 'meta_description'
        ]
    
    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        # Si l'article passe en statut publié, mettre à jour la date de publication
        if validated_data.get('status') == 'published' and instance.status != 'published':
            from django.utils import timezone
            validated_data['published_at'] = timezone.now()
        
        return super().update(instance, validated_data)


class ArticleSearchSerializer(serializers.Serializer):
    query = serializers.CharField(max_length=200)
    category = serializers.CharField(max_length=100, required=False)
    tags = serializers.ListField(child=serializers.CharField(), required=False)
    status = serializers.ChoiceField(choices=Article.STATUS_CHOICES, required=False)
