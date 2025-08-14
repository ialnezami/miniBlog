from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .services import AIContentChecker
from django.views.decorators.csrf import csrf_exempt
import json


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def check_article_content(request):
    """
    Vérifie le contenu d'un article avec l'IA
    """
    try:
        data = request.data
        title = data.get('title', '')
        content = data.get('content', '')
        excerpt = data.get('excerpt', '')
        
        if not title or not content:
            return Response(
                {'error': 'Le titre et le contenu sont requis'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Initialiser le service IA
        ai_checker = AIContentChecker()
        
        # Vérifier le contenu
        result = ai_checker.check_article_content(title, content, excerpt)
        
        if result['success']:
            return Response({
                'message': 'Contenu vérifié avec succès',
                'data': result
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'message': 'Erreur lors de la vérification',
                'data': result
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
    except Exception as e:
        return Response({
            'error': f'Erreur serveur: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def check_content_appropriate(request):
    """
    Vérifie si le contenu est approprié
    """
    try:
        data = request.data
        content = data.get('content', '')
        
        if not content:
            return Response(
                {'error': 'Le contenu est requis'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Initialiser le service IA
        ai_checker = AIContentChecker()
        
        # Vérifier l'appropriation du contenu
        result = ai_checker.check_for_inappropriate_content(content)
        
        return Response({
            'message': 'Contenu vérifié',
            'data': result
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'error': f'Erreur serveur: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def suggest_improvements(request):
    """
    Suggère des améliorations pour le contenu
    """
    try:
        data = request.data
        content = data.get('content', '')
        aspect = data.get('aspect', 'general')
        
        if not content:
            return Response(
                {'error': 'Le contenu est requis'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Initialiser le service IA
        ai_checker = AIContentChecker()
        
        # Générer des suggestions
        result = ai_checker.suggest_improvements(content, aspect)
        
        if result['success']:
            return Response({
                'message': 'Suggestions générées avec succès',
                'data': result
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'message': 'Erreur lors de la génération des suggestions',
                'data': result
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
    except Exception as e:
        return Response({
            'error': f'Erreur serveur: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
