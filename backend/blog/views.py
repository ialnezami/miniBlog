from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import Article, Category, Tag, Comment
from .serializers import (
    ArticleListSerializer, ArticleDetailSerializer, ArticleCreateUpdateSerializer,
    CategorySerializer, TagSerializer, CommentSerializer, ArticleSearchSerializer
)
from .permissions import IsAuthorOrReadOnly


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """Vue pour les catégories (lecture seule)"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Vue pour les tags (lecture seule)"""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


class ArticleViewSet(viewsets.ModelViewSet):
    """Vue pour les articles avec toutes les opérations CRUD"""
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'category', 'tags', 'author']
    search_fields = ['title', 'content', 'excerpt']
    ordering_fields = ['created_at', 'published_at', 'title']
    ordering = ['-published_at', '-created_at']
    
    def get_queryset(self):
        """Retourne les articles publiés pour les visiteurs, tous pour les auteurs"""
        if self.action == 'list' and not self.request.user.is_authenticated:
            return Article.objects.filter(status='published')
        elif self.action == 'list' and not self.request.user.is_staff:
            return Article.objects.filter(
                Q(status='published') | Q(author=self.request.user)
            )
        return Article.objects.all()
    
    def get_serializer_class(self):
        """Retourne le bon sérialiseur selon l'action"""
        if self.action in ['create', 'update', 'partial_update']:
            return ArticleCreateUpdateSerializer
        elif self.action == 'retrieve':
            return ArticleDetailSerializer
        return ArticleListSerializer
    
    def perform_create(self, serializer):
        """Assigne automatiquement l'auteur lors de la création"""
        serializer.save(author=self.request.user)
    
    @action(detail=False, methods=['get'])
    def my_articles(self, request):
        """Retourne les articles de l'utilisateur connecté"""
        if not request.user.is_authenticated:
            return Response(
                {'error': 'Authentification requise'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        articles = Article.objects.filter(author=request.user)
        serializer = ArticleListSerializer(articles, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def drafts(self, request):
        """Retourne les brouillons de l'utilisateur connecté"""
        if not request.user.is_authenticated:
            return Response(
                {'error': 'Authentification requise'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        drafts = Article.objects.filter(author=request.user, status='draft')
        serializer = ArticleListSerializer(drafts, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def search(self, request):
        """Recherche avancée d'articles"""
        serializer = ArticleSearchSerializer(data=request.data)
        if serializer.is_valid():
            query = serializer.validated_data['query']
            category = serializer.validated_data.get('category')
            tags = serializer.validated_data.get('tags', [])
            status_filter = serializer.validated_data.get('status')
            
            # Construire la requête de recherche
            q_objects = Q(title__icontains=query) | Q(content__icontains=query) | Q(excerpt__icontains=query)
            
            queryset = Article.objects.filter(q_objects)
            
            if category:
                queryset = queryset.filter(category__name__icontains=category)
            
            if tags:
                queryset = queryset.filter(tags__name__in=tags).distinct()
            
            if status_filter:
                queryset = queryset.filter(status=status_filter)
            
            # Filtrer par statut publié pour les visiteurs
            if not request.user.is_authenticated:
                queryset = queryset.filter(status='published')
            
            serializer_result = ArticleListSerializer(queryset, many=True)
            return Response(serializer_result.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def publish(self, request, pk=None):
        """Publie un article (change le statut de draft à published)"""
        article = self.get_object()
        
        if article.author != request.user and not request.user.is_staff:
            return Response(
                {'error': 'Permission refusée'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        article.status = 'published'
        article.save()
        
        serializer = ArticleDetailSerializer(article)
        return Response({
            'message': 'Article publié avec succès',
            'article': serializer.data
        })
    
    @action(detail=True, methods=['post'])
    def check_with_ai(self, request, pk=None):
        """Vérifie le contenu de l'article avec l'IA"""
        article = self.get_object()
        
        if article.author != request.user and not request.user.is_staff:
            return Response(
                {'error': 'Permission refusée'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Importer le service IA
        from ai_content_checker.services import AIContentChecker
        
        ai_checker = AIContentChecker()
        result = ai_checker.check_article_content(
            article.title, 
            article.content, 
            article.excerpt
        )
        
        if result['success']:
            # Mettre à jour l'article avec les résultats de l'IA
            article.ai_checked = True
            article.ai_score = result.get('score')
            article.ai_feedback = result.get('feedback')
            article.save()
            
            serializer = ArticleDetailSerializer(article)
            return Response({
                'message': 'Article vérifié avec l\'IA',
                'ai_result': result,
                'article': serializer.data
            })
        else:
            return Response({
                'error': 'Erreur lors de la vérification IA',
                'ai_result': result
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CommentViewSet(viewsets.ModelViewSet):
    """Vue pour les commentaires"""
    queryset = Comment.objects.filter(is_approved=True)
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        """Filtre les commentaires par article si spécifié"""
        article_id = self.request.query_params.get('article')
        if article_id:
            return Comment.objects.filter(article_id=article_id, is_approved=True)
        return Comment.objects.filter(is_approved=True)
    
    def perform_create(self, serializer):
        """Assigne automatiquement l'article lors de la création"""
        article_id = self.request.data.get('article')
        if article_id:
            article = get_object_or_404(Article, id=article_id)
            serializer.save(article=article)
