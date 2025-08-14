from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Permission personnalisée pour permettre aux auteurs de modifier leurs articles
    """
    
    def has_object_permission(self, request, view, obj):
        # Lecture autorisée pour tous
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Écriture autorisée seulement pour l'auteur ou les admins
        return obj.author == request.user or request.user.is_staff


class IsCommentAuthorOrReadOnly(permissions.BasePermission):
    """
    Permission pour les commentaires
    """
    
    def has_object_permission(self, request, view, obj):
        # Lecture autorisée pour tous
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Écriture autorisée seulement pour l'auteur du commentaire ou les admins
        return obj.author_name == request.user.username or request.user.is_staff
