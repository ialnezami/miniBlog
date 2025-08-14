from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.db import IntegrityError
from .serializers import UserSerializer


@api_view(['POST'])
def register(request):
    """Inscription d'un nouvel utilisateur"""
    try:
        data = request.data
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        first_name = data.get('first_name', '')
        last_name = data.get('last_name', '')
        
        # Validation des données
        if not all([username, email, password]):
            return Response({
                'error': 'Tous les champs sont requis'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if len(password) < 8:
            return Response({
                'error': 'Le mot de passe doit contenir au moins 8 caractères'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Créer l'utilisateur
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        
        serializer = UserSerializer(user)
        return Response({
            'message': 'Utilisateur créé avec succès',
            'user': serializer.data
        }, status=status.HTTP_201_CREATED)
        
    except IntegrityError:
        return Response({
            'error': 'Nom d\'utilisateur ou email déjà utilisé'
        }, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({
            'error': f'Erreur lors de la création: {str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile(request):
    """Récupère le profil de l'utilisateur connecté"""
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    """Déconnexion de l'utilisateur"""
    # Avec JWT, la déconnexion se fait côté client en supprimant le token
    # Cette vue peut être utilisée pour la journalisation ou d'autres actions
    return Response({
        'message': 'Déconnexion réussie'
    })
