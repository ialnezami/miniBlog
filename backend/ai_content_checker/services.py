import openai
from django.conf import settings
from django.core.exceptions import ValidationError
import logging

logger = logging.getLogger(__name__)


class AIContentChecker:
    """Service pour vérifier le contenu des articles avec l'IA"""
    
    def __init__(self):
        self.api_key = settings.OPENAI_API_KEY
        self.model = settings.OPENAI_MODEL
        openai.api_key = self.api_key
    
    def check_article_content(self, title, content, excerpt=""):
        """
        Vérifie le contenu d'un article avec l'IA
        
        Returns:
            dict: Résultats de la vérification
        """
        try:
            # Préparer le prompt pour l'IA
            prompt = self._create_content_check_prompt(title, content, excerpt)
            
            # Appel à l'API OpenAI
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Tu es un expert en rédaction web et SEO qui analyse la qualité du contenu."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.3
            )
            
            # Analyser la réponse
            ai_feedback = response.choices[0].message.content
            score = self._extract_score(ai_feedback)
            
            return {
                'score': score,
                'feedback': ai_feedback,
                'checked': True,
                'success': True
            }
            
        except Exception as e:
            logger.error(f"Erreur lors de la vérification IA: {str(e)}")
            return {
                'score': None,
                'feedback': f"Erreur lors de la vérification: {str(e)}",
                'checked': False,
                'success': False
            }
    
    def _create_content_check_prompt(self, title, content, excerpt):
        """Crée le prompt pour l'analyse du contenu"""
        return f"""
        Analyse la qualité du contenu suivant et donne un score sur 10 avec des recommandations détaillées.
        
        Titre: {title}
        Extrait: {excerpt}
        Contenu: {content[:2000]}...
        
        Évalue les aspects suivants:
        1. Qualité du titre (clarté, attractivité, SEO)
        2. Structure et lisibilité du contenu
        3. Pertinence et valeur informative
        4. Grammaire et orthographe
        5. Optimisation SEO (mots-clés, structure)
        6. Engagement et style d'écriture
        
        Donne un score global sur 10 et des recommandations spécifiques pour améliorer chaque aspect.
        Format de réponse:
        SCORE: [score]/10
        
        [Analyse détaillée avec recommandations]
        """
    
    def _extract_score(self, feedback):
        """Extrait le score numérique du feedback de l'IA"""
        try:
            # Chercher le pattern "SCORE: X/10"
            if "SCORE:" in feedback:
                score_line = [line for line in feedback.split('\n') if 'SCORE:' in line][0]
                score = float(score_line.split(':')[1].split('/')[0].strip())
                return min(10, max(0, score))  # Limiter entre 0 et 10
            return None
        except:
            return None
    
    def check_for_inappropriate_content(self, content):
        """
        Vérifie si le contenu contient du contenu inapproprié
        """
        try:
            prompt = f"""
            Analyse ce contenu et détermine s'il contient du contenu inapproprié, offensant ou non conforme aux standards éthiques.
            
            Contenu: {content[:1500]}
            
            Réponds uniquement par:
            APPROPRIATE: OUI/NON
            RAISON: [explication si NON]
            """
            
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Tu es un modérateur de contenu qui vérifie la conformité éthique."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=200,
                temperature=0.1
            )
            
            result = response.choices[0].message.content
            
            if "APPROPRIATE: NON" in result:
                reason = result.split("RAISON:")[1].strip() if "RAISON:" in result else "Contenu inapproprié détecté"
                return {
                    'appropriate': False,
                    'reason': reason
                }
            
            return {
                'appropriate': True,
                'reason': None
            }
            
        except Exception as e:
            logger.error(f"Erreur lors de la vérification de contenu inapproprié: {str(e)}")
            return {
                'appropriate': True,  # En cas d'erreur, on considère comme approprié
                'reason': None
            }
    
    def suggest_improvements(self, content, aspect="general"):
        """
        Suggère des améliorations pour un aspect spécifique du contenu
        """
        try:
            prompts = {
                "seo": "Suggère des améliorations SEO pour ce contenu (mots-clés, structure, meta-description)",
                "style": "Suggère des améliorations de style et d'écriture pour ce contenu",
                "structure": "Suggère des améliorations de structure et d'organisation pour ce contenu",
                "general": "Suggère des améliorations générales pour ce contenu"
            }
            
            prompt = f"""
            {prompts.get(aspect, prompts["general"])}
            
            Contenu: {content[:1500]}
            
            Donne des suggestions concrètes et actionnables.
            """
            
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Tu es un expert en rédaction web qui donne des conseils pratiques."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.3
            )
            
            return {
                'suggestions': response.choices[0].message.content,
                'success': True
            }
            
        except Exception as e:
            logger.error(f"Erreur lors de la génération de suggestions: {str(e)}")
            return {
                'suggestions': "Impossible de générer des suggestions pour le moment.",
                'success': False
            }
